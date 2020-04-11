from dbutil import DB


# Note: Do not hard code db credentials into the file
#       You should ideally load these from a config
#       file. The following is only for simplified
#       demonstration purposes.
DB = Database({
        "host" : "localhost",
        "db" : "dbane",
        "user" : "userid",
        "passwd" : "password",
    })



def GetLatestTradeDate():
    query = '''SELECT max(trade_date) as tradedate
            FROM markets_india_stock_prices
            '''
    return DB.execute_query(query)[0]['tradedate']


def GetLatestPrices():
    latest_date = GetLatestTradeDate()
    query = '''
        SELECT instrument_id, close
        FROM markets_india_stock_prices
        WHERE trade_date = %s
        '''
    response = DB.execute_query(query, latest_date)
    return {
        res['instrument_id']: res['close']
        for res in response
    }


def GetCompanyFinancials():
    pnl_query = '''
        SELECT instrument_id, end_of_reporting_period,
        revenue_from_operations_net AS sales,
        total_revenue,
        net_profit, diluted_eps AS eps
        FROM markets_india_pnls
        ORDER BY instrument_id, end_of_reporting_period DESC        
    '''
    bs_query = '''
        SELECT instrument_id, end_of_reporting_period,
        total_shareholders_funds AS total_equity,
        share_capital AS share_capital,
        total_assets AS assets
        FROM markets_india_balance_sheets
        ORDER BY instrument_id, end_of_reporting_period DESC
    '''
    instrument_query = '''
        SELECT instrument_id, name, paidup_value
        FROM markets_india_stock_symbols
    '''
    all_pnls = DB.execute_query(pnl_query)
    all_balance_sheets = DB.execute_query(bs_query)
    instruments = DB.execute_query(instrument_query)
    current_pnl = {}
    previous_pnl = {}
    current_bs = {}
    instruments = {
        res['instrument_id']: res
        for res in instruments
    }
    for pnl in all_pnls:
        instrument_id = pnl['instrument_id']
        if instrument_id not in current_pnl:
            current_pnl[instrument_id] = pnl
        elif instrument_id not in previous_pnl:
            previous_pnl[instrument_id] = pnl
    for bs in all_balance_sheets:
        instrument_id = bs['instrument_id']
        if instrument_id not in current_bs:
            current_bs[instrument_id] = bs
    return {
        'current_pnl': current_pnl,
        'previous_pnl': previous_pnl,
        'current_bs': current_bs,
        'instruments': instruments,
    }


def CalculateStatistics(financials, prices):
    all_stats = []
    for instrument_id in financials['current_pnl']:
        cpnl = financials['current_pnl'][instrument_id]
        ppnl = financials['previous_pnl'].get(
            instrument_id, None)
        cbs = financials['current_bs'].get(
            instrument_id, None)
        instrument = financials['instruments'].get(
            instrument_id, None)
        px = prices.get(instrument_id, None)
        if ppnl is None or cbs is None or instrument is None or px is None:
            continue
        if instrument['paidup_value'] is None:
            continue
        num_shares = cbs['share_capital'] / instrument['paidup_value']
        if num_shares == 0:
            continue
        book_value = cbs['total_equity'] / num_shares
        try:
            pe = px / cpnl['eps']
        except:
            pe = 0
        try:
            ps = px / cpnl['sales'] * num_shares
        except:
            ps = 0
        try:
            pnl_growth = 100 * (cpnl['net_profit'] / ppnl['net_profit'] - 1)
        except:
            pnl_growth = 0
        try:
            net_margin = cpnl['net_profit'] / cpnl['total_revenue'] * 100
        except:
            net_margin = 0
        try:
            revenue_growth = 100 * (cpnl['total_revenue'] / ppnl['total_revenue'] - 1)
        except:
            revenue_growth = 0
        stats = {
            'roe': cpnl['eps'] / book_value * 100,
            'roa': cpnl['eps'] / (cbs['assets'] / num_shares),
            'cmp': px,
            'pb': px / book_value,
            'pe': pe,
            'ps': ps,
            'market_cap': px * num_shares / 1e7,
            'net_margin': net_margin,
            'profit_growth': pnl_growth,
            'revenue_growth': revenue_growth,
            'instrument_id': instrument_id
        }
        all_stats.append(stats)
    return all_stats


def UpdateDatabase(stats):
    query = '''
        UPDATE markets_india_calculated_ratios
        SET roe = %s, roa = %s, cmp = %s,
        price_to_book = %s, price_to_earnings = %s,
        price_to_sales = %s, market_cap = %s,
        net_margin = %s, profit_growth = %s,
        revenue_growth = %s
        WHERE instrument_id = %s
    '''
    for stat in stats:
        DB.execute_query(query, (
            stat['roe'], stat['roa'], stat['cmp'],
            stat['pb'], stat['pe'],
            stat['ps'], stat['market_cap'],
            stat['net_margin'], stat['profit_growth'],
            stat['revenue_growth'],
            stat['instrument_id']))


def UpdateStatistics():
    latest_prices = GetLatestPrices()
    financials = GetCompanyFinancials()
    stats = CalculateStatistics(financials, latest_prices)
    UpdateDatabase(stats)


if __name__ == '__main__':
    UpdateStatistics()
