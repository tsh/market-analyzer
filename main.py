from models import Stock, YahooProvider
from views import GUI, TUI, Telegram
from edgar.edgar import RecentSubmissionsAtom

from pprint import pprint


if __name__ == '__main__':
    interests = ['tesla', 'scion']
    activities = []
    for parser in RecentSubmissionsAtom().get_data():
        for interest in interests:
            for entree in  parser.entries:
                if interest.lower() in entree['title'].lower():
                    activities.append(entree['title'])

    tg = Telegram()
    if activities:
        text = '\n'.join(activities)
    else:
        text = 'Nothing found'
    tg.send(text)

