import requests
import hmac
import time
import urllib
import hashlib


class Poloniex(object):
    """Represents a Poloniex exchange"""

    base_url = 'https://poloniex.com/'

    def __init__(self, api_key=None, secret=None):
        """
        Args:
            api_key (str): Optional API Key
            secret (str): Option Secret
        """
        assert isinstance(api_key, (str, type(None)))
        assert isinstance(secret, (str, type(None)))
        assert ((api_key is not None and secret is not None) or
                (api_key is None and secret is None))

        self._api_key = api_key
        self._secret = secret

    def _get(self, path):
        """
        Args:
            path (unicode)

        Returns:
            dict
        """
        assert isinstance(path, unicode)

        req = requests.get('{base_url}public'
                           '?command=returnLoanOrders&currency=BTC'
                           .format(base_url=self.base_url))

        data = req.json()

        return data

    def _post(self, command, data):
        """
        Args:
            command (str)
            data (dict)

        Returns:
            dict
        """
        assert isinstance(command, str)
        assert isinstance(data, dict)

        data['command'] = command
        data['nonce'] = int(time.time() * 1000)

        encoded_data = urllib.urlencode(data)
        sign = hmac.new(self._secret, encoded_data, hashlib.sha512).hexdigest()

        headers = {
            'Key': self._api_key,
            'Sign': sign
        }

        url = self.base_url + 'tradingApi'
        req = requests.post(url, data=data, headers=headers)
        response = req.json()

        return response

    def get_max_demand_rate(self):
        """
        Returns:
            float: The maximum loan rate asked for BTC
        """
        data = self._get(u'public?command=returnLoanOrders&currency=BTC')

        demand_rates = set()
        for demand in data['demands']:
            demand_rates.add(float(demand['rate']))

        max_demand = max(demand_rates)

        return max_demand

    def get_min_offer_rate(self, min_amount=0.0):
        """
        Args:
            min_amount (float): Minimum amount of BTC offered. If not offer is
                                proposing the given amount, returns the
                                maximum known offer.
        Returns:
            float: The minimum loan rate offered for BTC, or None if no offer
                   is providing min_amount BTC.
        """
        assert isinstance(min_amount, float)

        data = self._get(u'public?command=returnLoanOrders&currency=BTC')

        offer_rates = set()

        # Filter the offers based on the min_amount, if any
        for offer in data['offers']:
            if float(offer['amount']) >= min_amount:
                rate = float(offer['rate'])
                offer_rates.add(rate)

        # If we have valid offers, get the lowest one
        if offer_rates:
            min_offer = min(offer_rates)
        # If we have no valid offer, get the largest unfiltered offer, as the
        # API won't let us get more offers
        else:
            for offer in data['offers']:
                rate = float(offer['rate'])
                offer_rates.add(rate)
            min_offer = max(offer_rates)

        return min_offer

    def get_unused(self):
        """
        Returns:
            float: Amount of BTC available in the lending wallet.
        """
        data = {
            'account': 'lending'
        }
        response = self._post('returnAvailableAccountBalances', data)
        if u'BTC' in response[u'lending']:
            unused_btc = float(response[u'lending'][u'BTC'])
        else:
            unused_btc = 0.0

        return unused_btc

    def offer_btc_loan(self, rate, amount, duration):
        """
        Args:
            rate (float)
            amount (float)
            duration (int): Duration of the loan, in days (2-60).

        Returns:
            int or None: Order ID if successful
        """
        assert isinstance(rate, float)
        assert isinstance(amount, float)
        assert isinstance(duration, int)

        data = {
            'currency': 'BTC',
            'amount': amount,
            'duration': duration,
            'autoRenew': 0,
            'lendingRate': rate
        }
        resp = self._post('createLoanOffer', data)

        if resp[u'success'] == 1:
            order_id = resp[u'orderID']
        else:
            order_id = None

        return order_id
