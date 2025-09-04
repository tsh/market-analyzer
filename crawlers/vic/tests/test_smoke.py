import os

import pytest

from crawlers.vic.parsers import IdeaParser

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.smoke
def test_get_ticker2(idea_page, expected_ticker, request):
    parser = IdeaParser(request.getfixturevalue(idea_page))
    assert parser.get_ticker() == expected_ticker

