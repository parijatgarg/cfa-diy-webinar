import DataLayer


def FindMomentumDeciles():
    ids = DataLayer.get_largest_companies_by_market_cap(200)
    latest_trading_days = DataLayer.get_latest_trading_days(250)
    start_date = latest_trading_days[-1]
    end_date = latest_trading_days[22]
    start_prices = DataLayer.get_prices_for_date(start_date)
    end_prices = DataLayer.get_prices_for_date(end_date)
    returns = {}
    for idx in ids:
        if idx not in start_prices or idx not in end_prices:
            continue
        returns[idx] = 100 * (
            end_prices[idx]['close'] / start_prices[idx]['close'] - 1)
    highest_momentum = sorted(
        returns.keys(), key=lambda x: returns[x], reverse=True)
    lowest_momentum = sorted(
        returns.keys(), key=lambda x: returns[x])
    highest_momentum = highest_momentum[0:20]
    lowest_momentum = lowest_momentum[0:20]
    return {
        'highest_momentum': highest_momentum,
        'lowest_momentum': lowest_momentum
    }


def PrintResults(momentum):
    secinfo = DataLayer.get_security_info(
        momentum['highest_momentum'])
    print("Highest Momentum Decile")
    print('-----------------------')
    for sec in momentum['highest_momentum']:
        print(secinfo.get(sec, {}).get('name', ''))

    secinfo = DataLayer.get_security_info(
        momentum['lowest_momentum'])
    print("")
    print("Lowest Momentum Decile")
    print('-----------------------')
    for sec in secinfo:
        print(secinfo.get(sec, {}).get('name', ''))



if __name__ == '__main__':
    momentum = FindMomentumDeciles()
    PrintResults(momentum)
