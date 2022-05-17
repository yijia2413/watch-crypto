#coding: utf8

import yfinance as yf
import pandas as pd
import logging

class Stock():
    def __init__(self):
        self.companies = {
            '1119.HK': '创梦天地',
            '300454.SZ': '深信服',
            '0268.HK': '金蝶',
            'tsla': '特斯拉',
            'BA': '波音',
            'PDD': '拼多多',
            '0700.HK': '腾讯',
            'NOW': 'ServiceNow',
            'DDOG': 'Datadog',
            'zm': 'ZOOM',
            'baba': 'Alibaba',
            'gtlb': 'Gitlab',
            'jd': '京东',
            'BIDU': 'Baidu',
            'DT': 'Dynatrace',
            'li': '理想汽车',
            'tsp': '图森未来',
            'twtr': 'Twitter',
            'CAR': '安飞士',
            'fb': 'Facebook',
            '1801.HK': '小米',
            '0772.HK': '阅文集团',
            'msft': '微软',
            'aapl': 'Apple',
            'goog': 'Google',
        }

    def get_data(self):
        tickers = yf.Tickers(' '.join(self.companies))

        dfs = []
        for c, name in self.companies.items():
            df = tickers.tickers.get(c.upper()).history(period="1d")
            df.insert(0, 'company', name)    
            dfs.append(df)
            
        result = pd.concat(dfs).fillna(0)
        return result
    
    def get_html(self):
        prefix = '<H1>Stock:</H1><br></br>'
        df = self.get_data()
        try:
            df = df.drop(['Volume', 'Dividends', 'Stock Splits'], axis=1)
        except Exception as e:
            logging.error(e)

        result = df.to_html()
        return  prefix + result