from forex_python.converter import CurrencyRates
from functools import lru_cache

class CurrencyConverter:
    def __init__(self):
        self.c = CurrencyRates()

    @lru_cache(maxsize=None)  # Cache all results
    def convert_currency(self, from_currency, to_currency, amount):
        return self.c.convert(from_currency, to_currency, amount)

    def get_supported_currencies(self):
        return self.c.get_currencies()
