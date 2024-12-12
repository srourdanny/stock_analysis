from datetime import datetime


def adjust_for_splits(ticker, trade_date, price):
  """
    The stock data obtain from the Alpha Vantage API is based on real time prices.
    Our team noticed the sharp dropoffs in some line graphs.  This behavior
    is attributed to the stock splits.
    
    The goal of this function is to processes the price of a stock and its date
    to obtain the split-adjusted price.

    Args:
    ticker (string): a stock ticker
    trade_date (date): the date of trade/closing
    price (float): the stock close price on the trade_date

    Returns:
      float: a split-adjusted price

    AMZN split -    2022-06-06    20:1
    GOOG split -    2022-07-18    20:1
    NVDA splits 1 - 2021-07-20     4:1
                2 - 2024-06-10    10:1
    TSLA splits 1 - 2020-08-31     5:1
                2 - 2022-08-25     3:1

    ORCL and META didn't have a split in the period 12/2019 - 11/2024
  """

  match ticker.lower():
    case 'amzn':
      split_date = datetime.strptime('2022-06-06', '%Y-%m-%d').date()
      if (trade_date < split_date):
        return price / 20.0
      else:
        return price
    case 'goog':
      split_date = datetime.strptime('2022-07-18', '%Y-%m-%d').date()
      if (trade_date < split_date):
        return price / 20.0
      else:
        return price
    case 'nvda':
      split_date_1 = datetime.strptime('2021-07-20', '%Y-%m-%d').date()
      split_date_2 = datetime.strptime('2024-06-10', '%Y-%m-%d').date()
      if (trade_date < split_date_1):
        return price / 40.0
      else:
        if (trade_date < split_date_2):
          return price / 10.0
        else:
          return price
    case 'tsla':
      split_date_1 = datetime.strptime('2020-08-31', '%Y-%m-%d').date()
      split_date_2 = datetime.strptime('2022-08-25', '%Y-%m-%d').date()
      if (trade_date < split_date_1):
        return price / 15.0
      else:
        if (trade_date < split_date_2):
          return price / 3.0
        else:
          return price
    case _:
      return price