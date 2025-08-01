import os

import pytest

from crawlers.vic.parsers import VICIdeasParser

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


@pytest.fixture(scope='session')
def ideas_page():
    with open(os.path.join(DIR_PATH, 'fixtures', 'ideas.html')) as f:
        return f.read()


def test_get_ideas_urls(ideas_page):
    parser = VICIdeasParser(ideas_page)

    assert set(parser.get_ideas_links()) == {'/idea/PALTALK_INC/1612654727', '/idea/PALTALK_INC/1612654727',
                                             '/idea/TENAZ_ENERGY_CORP/1214082761', '/idea/TENAZ_ENERGY_CORP/1214082761',
                                             '/idea/Central_Depository_Services_India_Limited/3967162029',
                                             '/idea/Central_Depository_Services_India_Limited/3967162029',
                                             '/idea/Dream_International_LTD/6584662208',
                                             '/idea/Dream_International_LTD/6584662208',
                                             '/idea/u-blox_Holding/2927900850', '/idea/u-blox_Holding/2927900850',
                                             '/idea/Ashtead_Technology_Holdings_Plc/3736298381',
                                             '/idea/Ashtead_Technology_Holdings_Plc/3736298381',
                                             '/idea/Estee_Lauder/7216195691', '/idea/Estee_Lauder/7216195691',
                                             '/idea/CURBLINE_PROPERTIES_CORP/5616295273',
                                             '/idea/CURBLINE_PROPERTIES_CORP/5616295273',
                                             '/idea/Aerovironment/1885732964', '/idea/Aerovironment/1885732964',
                                             '/idea/WIZZ_AIR_HOLDINGS_PLC/8499285928',
                                             '/idea/WIZZ_AIR_HOLDINGS_PLC/8499285928'}
