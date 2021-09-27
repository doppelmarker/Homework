"""
Module provides Singleton class.
"""
import inspect


class PrivateConstructorError(Exception):
    """Raised if a singleton class was explicitly instantiated."""

    pass


class Sun:
    __instance = None

    # As I've explored so far, the best way to create a singleton in Python implies
    # exploiting an idea of using a metaclass. However, the task is to provide a method to initialize class instance.
    # Sun should be considered as a singleton, but the public possibility of calling Sun() doesn't help us to prevent
    # creation of another instance! In Java, there is a way to make our constructor private and implement a
    # get_instance-like method to obtain the only existing instance. In Python though we can't make constructor private,
    # so I have decided to use introspection in order to check whether constructor was called explicitly by the user or
    # implicitly inside inst method. If it is called by the user, then the caller of __new__ was not inst and
    # PrivateConstructorError is raised. Apparently, we have to bear in mind that this approach is dependent on the
    # CPython implementation, that's why it should be considered as a bad idea if talking about production systems.
    def __new__(cls, *args, **kwargs):
        if inspect.stack()[1][3] != "inst":
            raise PrivateConstructorError(f"You can't explicitly create an instance of {cls.__name__}!")
        return super(Sun, cls).__new__(cls)

    def __init__(self):
        pass

    @classmethod
    def inst(cls):
        if not cls.__instance:
            cls.__instance = Sun()
        return cls.__instance


def main():
    p = Sun.inst()
    f = Sun.inst()
    print(p is f)
    obj = Sun()


if __name__ == "__main__":
    main()
