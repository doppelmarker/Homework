from MarkKanaplianik.task7_5.number_check import *


def is_prime(i, primes):
    """Checks whether the number is prime or not."""

    for prime in primes:
        if not (i == prime or i % prime):
            return False
    return i


def get_primes_before_n(n):
    """Returns a sequential set of primes, the last of which is less than a given number."""

    primes = {2}
    i = 2
    while True:
        if is_prime(i, primes):
            if i > n:
                return primes
            primes.add(i)
        i += 1


class GoldbachsConjectureBustedError(Exception):
    """Raised if two prime numbers the sum of which is not equal to a particular even number greater than 2 were not
    found."""

    pass


def find_two_primes_addends(primes, n):
    """Returns a tuple of two primes the sum of which is equal to a given number.

    Raises GoldbachsConjectureBustedError if such number were not found.
    """

    for prime1 in primes:
        for prime2 in primes:
            if prime1 + prime2 == n:
                return prime1, prime2
    raise GoldbachsConjectureBustedError("Goldbach's conjecture is busted!")


def prove_goldbachs_conjecture(num):
    """Prints the given even greater than 2 number and 2 prime numbers the sum of which is equal to a given number.

    Checks for being even and greater than 2 are performed by checker function which raises NotEvenNumberError and
    NumberNotGreaterThan2Error accordingly if number doesn't obey these restrictions.
    """
    try:
        checker(num)
    except NotEvenNumberError:
        print(f"The given number '{num}' is not even!")
    except NumberNotGreaterThan2Error:
        print(f"The given number '{num}' is not greater than 2!")
    else:
        primes = get_primes_before_n(num)
        prime1, prime2 = find_two_primes_addends(primes, num)
        print(f"The given number '{num}' can be represented as the sum of two prime numbers: {prime1}, {prime2}!")


def main():
    while True:
        number = int(input("Input number: "))
        prove_goldbachs_conjecture(number)

        choice = input("Enter Q to quit, anything else to continue: ")
        if choice.lower() == "q":
            break


if __name__ == "__main__":
    main()
