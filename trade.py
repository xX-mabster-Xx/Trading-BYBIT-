
import talib
from talib import abstract
import yfinance as yf


def solve(index: str) -> float:
    data = yf.download(index, start='2022-03-21')
    print(data)
    # data.rename(columns= {'O'})
    return 0


if __name__ == '__main__':
    solve('TSLA')




