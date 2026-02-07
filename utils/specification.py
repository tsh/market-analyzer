from abc import ABC, abstractmethod


class AbstractSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        pass

    def __and__(self, other):
        return AndSpecification(self, other)

    def __or__(self, other):
        return OrSpecification(self, other)


class AndSpecification(AbstractSpecification):
    def __init__(self, one, other):
        self.one = one
        self.other = other

    def is_satisfied_by(self, candidate) -> bool:
        return self.one.is_satisfied_by(candidate) and self.other.is_satisfied_by(candidate)


class OrSpecification(AbstractSpecification):
    def __init__(self, one, other):
        self.one = one
        self.other = other

    def is_satisfied_by(self, candidate) -> bool:
        return self.one.is_satisfied_by(candidate) or self.other.is_satisfied_by(candidate)


class NotSpecification(AbstractSpecification):
    def __init__(self, x):
        self.x = x

    def is_satisfied_by(self, candidate) -> bool:
        return not self.x.is_satisfied_by(candidate)
