from threading import Thread, Lock
from time import sleep


class Fork:
    def __init__(self, number: int):
        self.number = number
        self.lock = Lock()

    def take(self):
        self.lock.acquire()

    def put(self):
        self.lock.release()

    def is_free(self):
        return not self.lock.locked()


class Philosopher(Thread):
    def __init__(self, number: int, left_fork: Fork, right_fork: Fork):
        super(Philosopher, self).__init__()
        self.number = number
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self) -> None:
        while True:
            self.think()
            self.eat()

    def think(self):
        print(f"Philosopher {self.number} is thinking...")
        sleep(3)
        print(f"Philosopher {self.number} is ready to eat!")

    def eat(self):
        left_fork, right_fork = self.left_fork, self.right_fork

        if left_fork.is_free():
            # take left_fork
            left_fork.take()
            print(f"Philosopher {self.number} took fork {left_fork.number}.")

            if right_fork.is_free():
                # take right_fork
                right_fork.take()
                print(f"Philosopher {self.number} took fork {right_fork.number}.")

                print(f"Philosopher {self.number} started eating.")
                sleep(3)
                print(f"Philosopher {self.number} finished eating.")

                left_fork.put()
                print(f"Philosopher {self.number} put fork {left_fork.number}.")

                right_fork.put()
                print(f"Philosopher {self.number} put fork {right_fork.number}.")

            else:
                # if right fork is taken, put left fork and go think
                left_fork.put()
                print(f"Philosopher {self.number} couldn't eat and put fork {left_fork.number}.")
        # if left fork is taken, go think


def main():
    # number of philosophers and forks
    n = 5

    forks = [Fork(i) for i in range(n)]
    philosophers = [Philosopher(i, forks[i % n], forks[(i + 1) % n]) for i in range(n)]

    for p in philosophers:
        p.start()


if __name__ == "__main__":
    main()
