from models import Stock, YahooProvider
from views import GUI, TUI
from edgar.edgar import RecentSubmissionsAtom

from pprint import pprint


if __name__ == '__main__':
    interests = ['tesla', 'scion']
    for parser in RecentSubmissionsAtom().get_data():
        for interest in interests:
            for entree in  parser.entries:
                if interest.lower() in entree['title'].lower():
                    print(entree)

