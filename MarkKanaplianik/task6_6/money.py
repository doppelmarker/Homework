"""
Module provides Money class.
"""
import functools
from math import isclose


class UnknownCurrencyError(Exception):
    """Raised when trying to convert to an unknown currency."""

    pass


class MoneyValidator:
    """Validator of operations on Money instances."""

    @staticmethod
    def validate_money(f):
        @functools.wraps(f)
        def wrapper(self, other):
            if isinstance(other, Money):
                return f(self, other)
            else:
                raise ValueError("Other value in addition and subtraction operations must be Money instance.")

        return wrapper

    @staticmethod
    def validate_int_float(f):
        @functools.wraps(f)
        def wrapper(self, other):
            if isinstance(other, int) or isinstance(other, float):
                return f(self, other)
            else:
                raise ValueError("Other value in multiplication operation must be either int or float.")

        return wrapper

    @staticmethod
    def validate_zero_division(f):
        @functools.wraps(f)
        def wrapper(self, other):
            if other != 0:
                return f(self, other)
            else:
                raise ZeroDivisionError("Money division by zero.")

        return wrapper

    @staticmethod
    def validate_currency(f):
        @functools.wraps(f)
        def wrapper(self, currency):
            if currency in Money.exchange_rate:
                return f(self, currency)
            else:
                raise UnknownCurrencyError(f"Unknown currency: {currency}.")

        return wrapper


@functools.total_ordering
class Money:
    exchange_rate = {"USD": 1, "BYN": 2.51, "EUR": 0.85, "JPY": 110.93}

    # there is a small overhead in this implementation: this method is used both as private and public,
    # validation of currency is redundant when using it as private method
    @MoneyValidator.validate_currency
    def convert_to_currency(self, currency):
        return self._value * Money.exchange_rate[currency] / Money.exchange_rate[self._currency]

    def __init__(self, value, currency="USD"):
        if currency not in Money.exchange_rate:
            raise UnknownCurrencyError(f"Unknown currency: {currency}.")
        self._value = value
        self._currency = currency

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def currency(self):
        return self._currency

    # order of decorators here is important!
    @currency.setter
    @MoneyValidator.validate_currency
    def currency(self, currency):
        self._value = self.convert_to_currency(currency)
        self._currency = currency

    @MoneyValidator.validate_money
    def __add__(self, other):
        return Money(self._value + other.convert_to_currency(self._currency), self._currency)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    @MoneyValidator.validate_money
    def __sub__(self, other):
        new_value = self._value - other.convert_to_currency(self._currency)
        return Money(new_value if new_value > 0 else 0, self._currency)

    @MoneyValidator.validate_int_float
    def __mul__(self, other):
        return Money(self._value * other, self._currency)

    def __rmul__(self, other):
        return self.__mul__(other)

    @MoneyValidator.validate_zero_division
    @MoneyValidator.validate_int_float
    def __truediv__(self, other):
        return Money(self._value / other, self._currency)

    @MoneyValidator.validate_money
    def __lt__(self, other):
        return self._value < other.convert_to_currency(self._currency)

    @MoneyValidator.validate_money
    def __eq__(self, other):
        # eliminating floating-point numbers precision problems
        return isclose(self._value, other.convert_to_currency(self._currency))

    def __str__(self):
        return f"{self._value:.2f} {self._currency}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value}, currency={self._currency})"


def main():
    x = Money(10, "BYN")
    y = Money(11, "USD")  # define your own default value, e.g. “USD”
    z = Money(12.34, "EUR")

    print(z + 3.11 * x + y * 0.8)  # result in “EUR”

    lst = [Money(10, "BYN"), Money(11), Money(12.01, "JPY")]
    s = sum(lst)
    print(s)  # result in “BYN”

    m1 = Money(10)
    m2 = Money(25.1, "BYN")
    print(m2 - m1)
    print(m1 == m2)

    m1.currency = "JPY"
    print(m1)


if __name__ == "__main__":
    main()
