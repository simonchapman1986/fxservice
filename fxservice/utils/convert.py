from decimal import Decimal


def calculate_fx(current: float, rate: float, places: int) -> Decimal:
    """calculates exchange rate

    :param current: current value
    :type current: float
    :param rate: current exchange rate
    :type rate: float
    :return: new value
    :rtype: float
    """
    current = Decimal(current)
    rate = Decimal(rate)

    return round(current * rate, places)
