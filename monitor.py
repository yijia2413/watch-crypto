#coding: utf8

import logging
from stock import stock
from crypto import crypto

g_dst_html = './result.html'

def generate_html():
    l = []
    # 
    crypto_app = crypto.Crypto()
    crypto_html = crypto_app.get_html()
    l.append(crypto_html)

    # 
    stock_app = stock.Stock()
    stock_html = stock_app.get_html()
    l.append(stock_html)

    return l

def dump_html(hl:list):
    with open(g_dst_html, 'w') as f:
        f.write('\n'.join(hl))

def main():
    l = generate_html()
    dump_html(l)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("monitor.log"),
            logging.StreamHandler()
        ]
    )
    main()