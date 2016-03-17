"""watch_lending_rate

Usage:
  watch_lending_rate
  watch_lending_rate --debug
  watch_lending_rate (-h | --help)

Options:
  -h --help     Show this screen.
  --debug       Dry run verbose mode.

"""
from docopt import docopt
import keen

from poloniex import Poloniex


BTC_PER_BIG_OFFER = 10.0
DEBUG = False


def main():
    global DEBUG
    args = docopt(__doc__)
    if args['--debug']:
        DEBUG = True

    poloniex = Poloniex()
    max_demand = poloniex.get_max_demand_rate()
    min_offer = poloniex.get_min_offer_rate()
    min_big_offer = poloniex.get_min_offer_rate(BTC_PER_BIG_OFFER)

    print "max_demand:", max_demand,
    print "min_offer:", min_offer,
    print "min_big_offer:", min_big_offer

    if not DEBUG:
        keen.add_event("lending-rates", {
            "max-demand": max_demand,
            "min-offer": min_offer,
            "min-big-offer": min_big_offer
        })


if __name__ == "__main__":
    main()
