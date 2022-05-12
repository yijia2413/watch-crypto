#coding: utf8

import requests
import logging
import datetime
import markdown
import pytablewriter as wt

class Crypto():
    def __init__(self):
        # only show 10 lines of history
        self.g_hist_limit = 10

        #  https://api-pub.bitfinex.com/v2/trades/tBTCUSD/hist
        self.g_base_hist_url = 'https://api-pub.bitfinex.com/v2/trades'

        # https://api-pub.bitfinex.com/v2/tickers?symbols=ALL
        # https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD,tDOGE:USD,tSHIB:USD,tUNIUSD
        self.g_base_realtime_url = 'https://api-pub.bitfinex.com/v2/tickers?symbols='

        # monitor btc and eth, for more: https://api-pub.bitfinex.com/v2/conf/pub:list:currency
        self.g_monitor_coins = {
            'tBTCUSD': 'BTC', 
            'tETHUSD': 'ETH', 
            'tDOGE:USD': 'DogeCoin',
            'tUNIUSD': 'Uniswap',
            'tSHIB:USD': 'SHIB',
        }

        # history data
        self.g_hist_headers = ['ID', 'MTS', 'AMOUNT', 'PRICE']
        # current value
        self.g_realtime_headers = ['SYMBOL', 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_RELATIVE', 'LAST_PRICE', 'VOLUME', 'HIGH', 'LOW']

    def get_json(self, url):
        try:
            ret = requests.get(url)
        except Exception as e:
            logging.error(e)
            return None
        if ret.status_code != 200:
            logging.error('status:%d, u:%s', ret.status_code, url)
            return None

        return ret.json()

    def get_realtime_price(self):
        url = self.g_base_realtime_url + ','.join(self.g_monitor_coins.keys())
        return self.get_json(url)

    def get_hist_price(self, coin):
        url = '{}/{}/hist?limit={}'.format(self.g_base_hist_url, coin, self.g_hist_limit)
        return self.get_json(url)

    def get_data(self):

        result = '# Crypto\n* Time:{}\n'.format(str(datetime.datetime.now()))
        result += '* URL: [yahoo](https://finance.yahoo.com/cryptocurrencies/), [coinbase](https://www.coinbase.com/price)\n'

        realtime_list = self.get_realtime_price()

        # list btc and eth price
        if realtime_list and (len(self.g_monitor_coins) == len(realtime_list)):
            for index, value in enumerate(realtime_list):
                # restapi value 0 return name
                if len(value) != len(self.g_realtime_headers):
                    continue 
                result += '* {}:{}$\n'.format(self.g_monitor_coins.get(value[0]), value[7])
        
        # try:
        #     writer = wt.MarkdownTableWriter(
        #         table_name=','.join(g_monitor_coins.values()),
        #         headers=g_realtime_headers,
        #         value_matrix=realtime_list,
        #     )
        #     result += writer.dumps()
        # except Exception as e:
        #     logging.error(e)

        # result += '\n\n'

        # for coin in g_monitor_coins:
        #     hist_list = get_hist_price(coin)
        #     if (not hist_list) or (not isinstance(hist_list, list)):
        #         continue

        #     writer = wt.MarkdownTableWriter(
        #         table_name=g_monitor_coins.get(coin),
        #         headers=g_hist_headers,
        #         value_matrix=hist_list,
        #     )
        #     result += (writer.dumps() + '\n')

        return result

    def get_html(self):
        md = self.get_data()
        html = markdown.markdown(md, extensions=['markdown.extensions.tables'])
        return html