import time

import requests
from binance.um_futures import UMFutures
from tradingview_ta import TA_Handler, Interval

INTERVAL = Interval.INTERVAL_15_MINUTES
TELEGRAM_TOKEN = '5400624088:AAF ao4I4AjdyoGWMOa8zG_dwxVnoXTSDd2s'  # bot token
TELEGRAM_CHANNEL = '@AVKAlerts'  # bot name

symbols = []
longs = []
shorts = []

client = UMFutures()


def get_data(symbol):
    output = TA_Handler(symbol=symbol,
                        screener='Crypto',
                        exchange='Binance',
                        interval=INTERVAL)
    activiti = output.get_analysis().summary
    activiti['SYMBOL'] = symbol
    return activiti


def get_symbols():
    tickers = client.mark_price()
    symbols = []
    for i in tickers:
        ticker = i['symbol']
        symbols.append(ticker)
    return symbols


def send_message(text):
    params = {'chat_id': TELEGRAM_CHANNEL, 'text': text}
    res = requests.get(f'httos://api.telegram.org/bot{TELEGRAM_TOKEN}', params=params)


def first_data():
    message = 'seraching first data'
    print(message)
    send_message(message)
    for i in symbols:
        try:
            data = get_data(i)
            # print (data)
            if data['RECOMMENDATION'] == 'STRONG_BUY':
                longs.append(data['SYMBOL'])
                # print (data[ 'SYMBOL '], 'Buy')

            if data['RECOMMENDATION'] == 'STRONG_SELL':
                shorts.append(data['SYMBOL '])
            time.sleep(0.1)
        except Exception as err:
            print(err)
    print(f'longs: {longs}')
    print(f'shorts: {shorts}')
    return longs, shorts


def main():
    print('starting main')
    for i in symbols:
        data = get_data(i)
        symbol_ = data['SYMBOL']
        recommendation_ = data['RECOMMENDATION']
        if recommendation_ == 'STRONG_BUY' and symbol_ not in longs:
            text = symbol_ + ' BUY'
            print(text)
            send_message(text)
            longs.append(symbol_)

        if recommendation_ == 'STRONG_SELL' and symbol_ not in shorts:
            text = symbol_ + ' SELL'
            print(text)
            send_message(text)
            shorts.append(symbol_)


if __name__ == '__main__':
    main()
