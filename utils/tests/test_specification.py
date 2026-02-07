import unittest
from utils.specification import AbstractSpecification, AndSpecification, OrSpecification, NotSpecification

import pytest
from typing import List


class IsEven(AbstractSpecification):
    def is_satisfied_by(self, candidate) -> bool:
        return candidate % 2 == 0


class IsPositive(AbstractSpecification):
    def is_satisfied_by(self, candidate) -> bool:
        return candidate > 0


class IsGreaterThanTen(AbstractSpecification):
    def is_satisfied_by(self, candidate) -> bool:
        return candidate > 10


@pytest.fixture
def is_even():
    return IsEven()


@pytest.fixture
def is_positive():
    return IsPositive()


@pytest.fixture
def is_greater_than_ten():
    return IsGreaterThanTen()


class TestSimpleSpecifications:
    """Test basic specification functionality"""

    def test_is_even_with_even_number(self, is_even):
        assert is_even.is_satisfied_by(4)
        assert is_even.is_satisfied_by(2)
        assert is_even.is_satisfied_by(0)

    def test_is_even_with_odd_number(self, is_even):
        assert not is_even.is_satisfied_by(3)
        assert not is_even.is_satisfied_by(5)

    def test_is_positive_with_positive_number(self, is_positive):
        assert is_positive.is_satisfied_by(5)
        assert is_positive.is_satisfied_by(1)

    def test_is_positive_with_negative_number(self, is_positive):
        assert not is_positive.is_satisfied_by(-5)
        assert not is_positive.is_satisfied_by(0)


class TestAndSpecification:
    """Test AND specification combinations"""

    def test_both_conditions_satisfied(self, is_even, is_positive):
        spec = is_even & is_positive
        assert spec.is_satisfied_by(4)
        assert spec.is_satisfied_by(2)
        assert spec.is_satisfied_by(8)

    def test_first_condition_fails(self, is_even, is_positive):
        spec = is_even & is_positive
        assert not spec.is_satisfied_by(3)
        assert not spec.is_satisfied_by(5)

    def test_second_condition_fails(self, is_even, is_positive):
        spec = is_even & is_positive
        assert not spec.is_satisfied_by(-2)
        assert not spec.is_satisfied_by(-4)

    def test_both_conditions_fail(self, is_even, is_positive):
        spec = is_even & is_positive
        assert not spec.is_satisfied_by(-3)
        assert not spec.is_satisfied_by(-5)

    def test_returns_and_specification_instance(self, is_even, is_positive):
        spec = is_even & is_positive
        assert isinstance(spec, AndSpecification)
        assert isinstance(spec, AbstractSpecification)

    def test_chained_and(self, is_even, is_positive, is_greater_than_ten):
        spec = is_even & is_positive & is_greater_than_ten
        assert spec.is_satisfied_by(12)
        assert spec.is_satisfied_by(20)
        assert not spec.is_satisfied_by(4)  # not > 10
        assert not spec.is_satisfied_by(11)  # odd
        assert not spec.is_satisfied_by(-12)  # negative


class TestOrSpecification:
    """Test OR specification combinations"""

    def test_both_conditions_satisfied(self, is_even, is_positive):
        spec = is_even | is_positive
        assert spec.is_satisfied_by(4)
        assert spec.is_satisfied_by(2)

    def test_only_first_condition_satisfied(self, is_even, is_positive):
        spec = is_even | is_positive
        assert spec.is_satisfied_by(-2)
        assert spec.is_satisfied_by(-4)

    def test_only_second_condition_satisfied(self, is_even, is_positive):
        spec = is_even | is_positive
        assert spec.is_satisfied_by(3)
        assert spec.is_satisfied_by(5)

    def test_both_conditions_fail(self, is_even, is_positive):
        spec = is_even | is_positive
        assert not spec.is_satisfied_by(-3)
        assert not spec.is_satisfied_by(-5)

    def test_returns_or_specification_instance(self, is_even, is_positive):
        spec = is_even | is_positive
        assert isinstance(spec, OrSpecification)
        assert isinstance(spec, AbstractSpecification)

    def test_chained_or(self, is_even, is_positive, is_greater_than_ten):
        spec = is_even | is_positive | is_greater_than_ten
        assert spec.is_satisfied_by(4)
        assert spec.is_satisfied_by(3)
        assert spec.is_satisfied_by(15)
        assert spec.is_satisfied_by(-2)  # even
        assert not spec.is_satisfied_by(-3)


class TestNotSpecification:
    """Test NOT specification"""

    def test_negates_true_condition(self, is_even):
        spec = NotSpecification(is_even)
        assert not spec.is_satisfied_by(4)
        assert not spec.is_satisfied_by(2)

    def test_negates_false_condition(self, is_even):
        spec = NotSpecification(is_even)
        assert spec.is_satisfied_by(3)
        assert spec.is_satisfied_by(5)

    def test_returns_not_specification_instance(self, is_even):
        spec = NotSpecification(is_even)
        assert isinstance(spec, NotSpecification)
        assert isinstance(spec, AbstractSpecification)

    def test_double_negation(self, is_even):
        spec = NotSpecification(NotSpecification(is_even))
        assert spec.is_satisfied_by(4)
        assert not spec.is_satisfied_by(3)


class TestComplexCombinations:
    """Test complex specification combinations"""

    def test_and_or_combination(self, is_even, is_positive, is_greater_than_ten):
        # (even AND positive) OR greater_than_ten
        spec = (is_even & is_positive) | is_greater_than_ten

        assert spec.is_satisfied_by(4)  # even and positive
        assert spec.is_satisfied_by(15)  # greater than 10
        assert spec.is_satisfied_by(11)  # greater than 10 (odd)
        assert not spec.is_satisfied_by(3)  # odd, not > 10
        assert not spec.is_satisfied_by(-2)  # even but negative, not > 10

    def test_not_and_combination(self, is_even, is_positive):
        # NOT(even) AND positive
        spec = NotSpecification(is_even) & is_positive

        assert spec.is_satisfied_by(3)
        assert spec.is_satisfied_by(7)
        assert not spec.is_satisfied_by(4)  # even
        assert not spec.is_satisfied_by(-3)  # negative

    def test_or_and_combination(self, is_even, is_positive, is_greater_than_ten):
        # even OR (positive AND greater_than_ten)
        spec = is_even | (is_positive & is_greater_than_ten)

        assert spec.is_satisfied_by(2)  # even
        assert spec.is_satisfied_by(15)  # positive and > 10
        assert spec.is_satisfied_by(-4)  # even
        assert not spec.is_satisfied_by(3)  # odd and not > 10
        assert not spec.is_satisfied_by(-15)  # not even, negative


@pytest.mark.parametrize("value,expected", [
    (4, True),
    (2, True),
    (8, True),
    (3, False),
    (5, False),
    (7, False),
])
def test_is_even_parametrized(value, expected):
    spec = IsEven()
    assert spec.is_satisfied_by(value) == expected


@pytest.mark.parametrize("value,expected", [
    (4, True),  # even and positive
    (2, True),  # even and positive
    (3, False),  # odd
    (-2, False),  # negative
    (-3, False),  # odd and negative
    (0, False),  # zero
])
def test_and_specification_parametrized(value, expected):
    spec = IsEven() & IsPositive()
    assert spec.is_satisfied_by(value) == expected


@pytest.mark.parametrize("value,expected", [
    (4, True),  # even and positive
    (3, True),  # positive
    (-2, True),  # even
    (-3, False),  # odd and negative
])
def test_or_specification_parametrized(value, expected):
    spec = IsEven() | IsPositive()
    assert spec.is_satisfied_by(value) == expected