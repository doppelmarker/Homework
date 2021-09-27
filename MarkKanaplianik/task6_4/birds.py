"""
Module contains birds hierarchy.
"""


class Bird:
    def __init__(self, name):
        self.name = name

    def fly(self):
        print(f"{self.name} bird can fly")

    def walk(self):
        print(f"{self.name} bird can walk")

    def __str__(self):
        return f"{self.name} bird can walk"


class FlyingBird(Bird):
    def __init__(self, name, ration="grains"):
        super().__init__(name)
        self.ration = ration

    def eat(self):
        print(f"Flying bird {self.name} eats mostly {self.ration}")

    def __str__(self):
        return f"{self.name} bird can walk and fly"


class NonFlyingBird(Bird):
    def __init__(self, name, ration="fish"):
        super().__init__(name)
        self.ration = ration

    def fly(self):
        raise AttributeError(f"{self.name} object has no attribute fly")

    def eat(self):
        print(f"Nonflying bird {self.name} eats mostly {self.ration}")

    def swim(self):
        print(f"{self.name} can swim")

    def __str__(self):
        return f"{self.name} bird can walk and swim"


class SuperBird(FlyingBird, NonFlyingBird):
    def __str__(self):
        return f"{self.name} bird can walk, swim and fly"


def main():
    bird = Bird("Any")
    bird.walk()

    penguin = NonFlyingBird("Penguin")
    penguin.swim()
    # penguin.fly()
    penguin.eat()

    canary = FlyingBird("Canary")
    print(canary)
    canary.eat()

    gull = SuperBird("Gull")
    print(gull)
    gull.eat()

    print(SuperBird.mro())


if __name__ == "__main__":
    main()
