import DataLayer
import pandas as pd


class Screener(object):

    def __init__(self):
        pass

    def _remap_fields(self, df):
        df.rename(columns={
                'roe': 'ROE',
                'roa': 'ROA',
                'price_to_book': 'Price_To_Book',
                'price_to_earnings': 'Price_To_Earnings',
                'price_to_sales': 'Price_To_Sales',
                'market_cap': 'Market_Cap',
                'net_margin': 'Net_Margin',
                'profit_growth': 'Profit_Growth',
                'revenue_growth': 'Revenue_Growth',
                'name': 'Name',
                'cmp': 'CMP',
            }, inplace=True)


    def run_screen(self, query_string):
        data = DataLayer.get_all_computed_ratios()
        df = pd.DataFrame(data)
        self._remap_fields(df)
        subset = df.loc[df.eval(query_string)]
        return subset.T.to_dict().values()
