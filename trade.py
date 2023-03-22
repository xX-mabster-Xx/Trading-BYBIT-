
import talib
from talib import abstract
import yfinance as yf

from tvDatafeed import TvDatafeed, Interval
import matplotlib.pyplot as plt
username = 'x-mabster-x'
password = 'qwerty123'

tv = TvDatafeed(username, password)

def solve(index: str) -> float:
    data = tv.get_hist(symbol= index, exchange='BYBIT', interval=Interval.in_1_minute, n_bars=1500)
    # print(data)
    sma = abstract.NATR(data)
    # print(sma.dtypes)
    data.plot(kind='line',y='open', color='red', )
    plt.show()
    # print(talib.get_function_groups())
    return 0


if __name__ == '__main__':
    solve('BTCUSDT.P')




