"""update_loan_offers

Usage:
  update_loan_offers
  update_loan_offers --debug
  update_loan_offers (-h | --help)

Options:
  -h --help     Show this screen.
  --debug       Dry run verbose mode.

"""
from docopt import docopt
import os

from poloniex import Poloniex


BTC_PER_BIG_OFFER = 10.0
DEBUG = False


def main():
    """
    Algorithm:

    If unused BTC:
        get min big loan offer
        Offer unused BTC at (min loan offer - 0.0001%)
    """
    global DEBUG
    args = docopt(__doc__)
    if args['--debug']:
        DEBUG = True

    api_key = os.environ.get('POLONIEX_API_KEY')
    secret = os.environ.get('POLONIEX_SECRET')

    poloniex = Poloniex(api_key=api_key, secret=secret)
    unused_btc = poloniex.get_unused()

    if unused_btc:
        min_big_offer = poloniex.get_min_offer_rate(BTC_PER_BIG_OFFER)

        # Get 0.0001% below
        my_rate = min_big_offer - (0.0001 / 100)

        # Place the actual order
        order_id = poloniex.offer_btc_loan(my_rate, unused_btc, 2)

        # Order status
        if order_id:
            print "Order placed ({})".format(order_id),
        else:
            print "Order failed",
        print "(Rate:", my_rate * 100, "%, Amount:", unused_btc, "BTC)"

if __name__ == "__main__":
    main()
