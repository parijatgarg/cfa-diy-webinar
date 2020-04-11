import DataLayer


def GetPriceHistory(num_days=2):
    latest_trading_days = DataLayer.get_latest_trading_days(num_days)
    prices = []
    for dt in latest_trading_days:
        prices.append(DataLayer.get_prices_for_date(dt))
    return prices


def FindBullishEngulfingPatterns(latest, previous):
    if previous is None:
        return False
    if latest['high'] > previous['high'] and \
        latest['low'] < previous['low'] and \
        latest['close'] > latest['open'] and \
        previous['close'] < previous['open']:
        return True
    else:
        return False


def FindPatterns(prices):
    instruments = prices[0].keys()
    has_pattern = []
    # Determine securities showing this pattern
    for inst in instruments:
        if FindBullishEngulfingPatterns(
            prices[0][inst], prices[1].get(inst, None)
            ):
                has_pattern.append(inst)
    return has_pattern


def DisplayCompanies(instruments, pattern_name):
    secinfo = DataLayer.get_security_info(instruments)
    print("{} Pattern Found In:".format(pattern_name))
    print("-"*50)
    for idx in secinfo:
        if secinfo[idx]['name'] is None:
            continue
        print(secinfo[idx]['name'])


if __name__ == '__main__':
    prices = GetPriceHistory()
    instruments = FindPatterns(prices)
    DisplayCompanies(instruments, "Bullish Engulfing Pattern")
