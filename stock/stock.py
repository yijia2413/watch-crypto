#coding: utf8

import yfinance as yf
import pandas as pd

class Stock():
    def __init__(self):
        self.companies = ['MSFT', 'aapl', 'goog']

    def get_data(self):
        tickers = yf.Tickers(' '.join(self.companies))

        dfs = []
        for c in self.companies:
            df = tickers.tickers.get(c.upper()).history(period="1d")
            df.insert(0, 'company', c.upper())    
            dfs.append(df)
            
        result = pd.concat(dfs).fillna(0)
        return result
    
    def get_html(self):
        # return html str
        df = self.get_data()
        result = df.to_html()
        return '<H1>Stock:</H1><br></br>\n' + result