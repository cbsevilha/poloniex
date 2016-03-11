import keen
import requests


BTC_PER_BIG_OFFER = 10


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

    for demand in data['demands']:
        if max_demand is None or float(demand['rate']) > max_demand:
            max_demand = float(demand['rate'])

    for offer in data['offers']:
        if min_offer is None or float(offer['rate']) < min_offer:
            min_offer = float(offer['rate'])
        if (float(offer['amount']) >= BTC_PER_BIG_OFFER and
                (min_big_offer is None or
                    float(offer['rate']) < min_big_offer)):
            min_big_offer = float(offer['rate'])

    return (max_demand, min_offer, min_big_offer)


def main():
    (max_demand, min_offer, min_big_offer) = get_lending_rates()

    print "max_demand:", max_demand,
    print "min_offer:", min_offer,
    print "min_big_offer:", min_big_offer

    keen.add_event("lending-rates", {
        "max-demand": max_demand,
        "min-offer": min_offer,
        "min-big-offer": min_big_offer
    })


if __name__ == "__main__":
    main()
