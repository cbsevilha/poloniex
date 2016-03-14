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
import requests


BTC_PER_BIG_OFFER = 10
DEBUG = False


def get_lending_rates():
    """
    Returns:
        (max_demand, min_offer, min_big_offer)
    """
    max_demand = None
    min_offer = None
    min_big_offer = None

    req = requests.get('https://poloniex.com/public'
                       '?command=returnLoanOrders&currency=BTC')

    data = req.json()

    demand_rates = set()
    for demand in data['demands']:
        demand_rates.add(float(demand['rate']))

    max_demand = max(demand_rates)

    offer_rates = set()
    big_offer_rates = set()

    for offer in data['offers']:
        rate = float(offer['rate'])
        offer_rates.add(rate)
        if float(offer['amount']) >= BTC_PER_BIG_OFFER:
            big_offer_rates.add(rate)

    min_offer = min(offer_rates)

    if big_offer_rates:
        min_big_offer = min(big_offer_rates)
    else:
        min_big_offer = max(offer_rates)

    return (max_demand, min_offer, min_big_offer)


def main():
    global DEBUG
    args = docopt(__doc__)
    if args['--debug']:
        DEBUG = True

    (max_demand, min_offer, min_big_offer) = get_lending_rates()

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
