#coding: utf8

import requests
import logging
import datetime
import markdown
import pytablewriter as wt

# only show 30 lines of history
g_hist_limit = 30

#  https://api-pub.bitfinex.com/v2/trades/tBTCUSD/hist
g_base_hist_url = 'https://api-pub.bitfinex.com/v2/trades'

# https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD
g_base_realtime_url = 'https://api-pub.bitfinex.com/v2/tickers?symbols='

# monitor btc and eth, for more: https://api-pub.bitfinex.com/v2/conf/pub:list:currency
g_monitor_coins = {'tBTCUSD': 'BTC', 'tETHUSD': 'ETH'}

# history data
g_hist_headers = ['ID', 'MTS', 'AMOUNT', 'PRICE']
# current value
g_realtime_headers = ['SYMBOL', 'BID', 'BID_SIZE', 'ASK', 'ASK_SIZE', 'DAILY_CHANGE', 'DAILY_CHANGE_RELATIVE', 'LAST_PRICE', 'VOLUME', 'HIGH', 'LOW']

g_dst_html = './result.html'

def get_json(url):
    try:
        ret = requests.get(url)
    except Exception as e:
        logging.error(e)
        return None
    if ret.status_code != 200:
        logging.error('status:%d, u:%s', ret.status_code, url)
        return None

    return ret.json()

def get_realtime_price():
    url = g_base_realtime_url + ','.join(g_monitor_coins.keys())
    return get_json(url)

def get_hist_price(coin):
    url = '{}/{}/hist?limit={}'.format(g_base_hist_url, coin, g_hist_limit)
    return get_json(url)

def json2md():

    result = '# Basic\n* Time:{}\n'.format(str(datetime.datetime.now()))
    result += '* URL: [yahoo](https://finance.yahoo.com/cryptocurrencies/), [coinbase](https://www.coinbase.com/price)\n'

    realtime_list = get_realtime_price()

    # list btc and eth price
    if realtime_list and (len(g_monitor_coins) == len(realtime_list)):
        for index, value in enumerate(realtime_list):
            # restapi value 0 return name
            if len(value) != len(g_realtime_headers):
                continue 
            result += '* {}:{}$\n'.format(g_monitor_coins.get(value[0]), value[7])
    
    try:
        writer = wt.MarkdownTableWriter(
            table_name=','.join(g_monitor_coins.values()),
            headers=g_realtime_headers,
            value_matrix=realtime_list,
        )
        result += writer.dumps()
    except Exception as e:
        logging.error(e)

    result += '\n\n'

    for coin in g_monitor_coins:
        hist_list = get_hist_price(coin)
        if (not hist_list) or (not isinstance(hist_list, list)):
            continue

        writer = wt.MarkdownTableWriter(
            table_name=g_monitor_coins.get(coin),
            headers=g_hist_headers,
            value_matrix=hist_list,
        )
        result += (writer.dumps() + '\n')

    return result

def md2html():
    md = json2md()
    html = markdown.markdown(md, extensions=['markdown.extensions.tables'])
    with open(g_dst_html, 'w') as f:
        f.write(html)

def main():
    md2html()
    logging.info("get crypto price success")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("crypto.log"),
            logging.StreamHandler()
        ]
    )
    main()