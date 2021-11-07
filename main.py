from models import Stock
from views import GUIView, TerminalView

from pprint import pprint

if __name__ == '__main__':
    qqq = Stock('GOOG')
    # gv = GUIView()
    # gv.display(qqq)
    tv = TerminalView()
    tv.display([qqq.name, qqq.ask()])


