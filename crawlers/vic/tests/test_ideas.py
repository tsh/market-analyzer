import os

import pytest

from ..parsers import IdeasParser

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='session')
def ideas_page():
    with open(os.path.join(DIR_PATH, 'fixtures', 'ideas.html')) as f:
        return f.read()


def test_get_a(ideas_page):
    parser = IdeasParser(ideas_page)
    assert True
        