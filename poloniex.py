import requests


class Poloniex(object):
    """Represents a Poloniex exchange"""

    base_url = 'https://poloniex.com/'

    def get_max_demand_rate(cls):
        """
        Returns:
            float: The maximum loan rate asked for BTC
        """
        req = requests.get('{base_url}public'
                           '?command=returnLoanOrders&currency=BTC'
                           .format(base_url=cls.base_url))

        data = req.json()

        demand_rates = set()
        for demand in data['demands']:
            demand_rates.add(float(demand['rate']))

        max_demand = max(demand_rates)

        return max_demand

    def get_min_offer_rate(cls, min_amount=0.0):
        """
        Args:
            min_amount (float): Minimum amount of BTC offered. If not offer is
                                proposing the given amount, returns None
        Returns:
            float: The minimum loan rate offered for BTC, or None if no offer
                   is providing min_amount BTC.
        """
        req = requests.get('{base_url}public'
                           '?command=returnLoanOrders&currency=BTC'
                           .format(base_url=cls.base_url))

        data = req.json()

        offer_rates = set()

        for offer in data['offers']:
            rate = float(offer['rate'])
            if float(offer['amount']) >= min_amount:
                offer_rates.add(rate)

        if offer_rates:
            min_offer = min(offer_rates)
        else:
            min_offer = None

        return min_offer
