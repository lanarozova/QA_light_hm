from typing import Collection, Any, Iterable, Self


class Cycle:
    def __init__(self, elements: Collection[Any]) -> None:
        self.elements = elements

    def __iter__(self) -> Self:
        self.current_element = 0
        return self

    def __next__(self) -> Iterable:
        if len(self.elements):
            result = self.elements[self.current_element]
            self.current_element = (self.current_element + 1) % len(self.elements)
            return result
        else:
            raise StopIteration
