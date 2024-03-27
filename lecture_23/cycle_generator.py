from typing import Iterable


class Cycle():
    def __init__(self, elements) -> None:
        self.elements = elements

    def __iter__(self) -> Iterable:
        self.current_element = 0
        return self

    def __next__(self) -> Iterable:
        if len(self.elements):
            result = self.elements[self.current_element]
            self.current_element = (self.current_element + 1) % len(self.elements)
            return result
        else:
            raise StopIteration


if __name__ == "__main__":
    # testing
    ls = [1, 2, 3]

    iterator = iter(Cycle(ls))

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
