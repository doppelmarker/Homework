from types import CodeType, FunctionType

a = "I am global variable!"


def enclosing_function_1():
    a = "I am variable from enclosed function!"

    def inner_function():
        a = "I am local variable!"
        print(a)


def enclosing_function_2():
    a = "I am variable from enclosed function!"

    def inner_function():
        a = "I am local variable!"
        print(a)

    return inner_function()


def call_inner_func(enclosing_func, *, inner_func_name):
    consts = enclosing_func.__code__.co_consts
    function = None
    for item in consts:
        if isinstance(item, CodeType) and item.co_name == inner_func_name:
            function = FunctionType(item, globals())
    try:
        function()
    except TypeError:
        pass


def main():
    call_inner_func(enclosing_function_1, inner_func_name="inner_function")
    enclosing_function_2()


if __name__ == "__main__":
    main()
