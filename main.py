from models import Stock, YahooProvider
from views import GUI, TUI
from edgar.edgar import RecentSubmissionsAtom

from pprint import pprint


if __name__ == '__main__':
    RecentSubmissionsAtom().get_data()
