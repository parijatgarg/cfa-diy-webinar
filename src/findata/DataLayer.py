from dbutil import Database


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


def get_all_computed_ratios():
    query = '''SELECT
            roe, roa, cmp,
            price_to_book, price_to_earnings,
            price_to_sales, market_cap,
            net_margin, profit_growth, revenue_growth,
            name
            FROM markets_india_calculated_ratios A,
            markets_india_stock_symbols B
            WHERE A.instrument_id = B.instrument_id
            '''
    return DB.execute_query(query)


def get_latest_trading_days(num_days):
    query = '''SELECT DISTINCT trade_date
            FROM markets_india_stock_prices
            ORDER BY trade_date DESC
            LIMIT %s
            '''
    response = DB.execute_query(query, num_days)
    return [res['trade_date'] for res in response]


def get_prices_for_date(date):
    query = '''SELECT instrument_id, open, high, low, close
            FROM markets_india_stock_prices
            WHERE trade_date = %s
            '''
    response = DB.execute_query(query, date)
    return {
        res['instrument_id']: res
        for res in response
    }


def get_security_info(instrument_ids):
    query = '''
        SELECT instrument_id, nse, name
        FROM markets_india_stock_symbols
        WHERE instrument_id IN ({})
    '''
    query = query.format(','.join(['%s'] * len(instrument_ids)))
    response = DB.execute_query(query, tuple(instrument_ids))
    return {
        res['instrument_id']: res
        for res in response
    }


def get_largest_companies_by_market_cap(count=100):
    query = '''SELECT instrument_id
            FROM markets_india_calculated_ratios
            ORDER BY market_cap
            DESC LIMIT %s
            '''
    response = DB.execute_query(query, count)
    return [res['instrument_id'] for res in response]
