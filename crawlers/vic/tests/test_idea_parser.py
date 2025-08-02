import os

import pytest

from crawlers.vic.parsers import IdeaParser

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='module')
def idea_axyx():
    with open(os.path.join(DIR_PATH, 'fixtures', 'idea', 'Axonyx_AXYX.html')) as f:
        yield f.read()

@pytest.fixture(scope='module')
def idea_inmb():
    with open(os.path.join(DIR_PATH, 'fixtures', 'idea', 'inmune_bio_inc_INMB.html')) as f:
        yield f.read()


@pytest.mark.parametrize('idea_page,expected_ticker', [
    ('idea_axyx', 'axyx'),
    ('idea_inmb', 'inmb')
]
                         )
def test_get_ticker(idea_page, expected_ticker, request):
    parser = IdeaParser(request.getfixturevalue(idea_page))
    assert parser.get_ticker() == expected_ticker

