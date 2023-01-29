from models import Stock, YahooProvider
from views import GUI, TUI, Telegram
from edgar.edgar import RecentSubmissionsAtom

from pprint import pprint


class UserInterests:
    def __init__(self):
        pass

    def instruments(self) -> list:
        return ['tesls', 'scion', 'apld']


if __name__ == '__main__':
    interests = UserInterests().instruments()
    submissions = RecentSubmissionsAtom().get_instruments()
    activities = []
    for interest in interests:
        if interest in submissions:
            activities.append(interest)

    tg = Telegram()
    if activities:
        text = '\n'.join(activities)
    else:
        text = 'Nothing found'
    tg.send(text)

