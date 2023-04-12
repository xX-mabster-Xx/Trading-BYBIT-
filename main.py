import asyncio
import time

from CONFIG import API_KEY, API_SECRET, API_KEY2, API_SECRET2
from bybit import Bybit
from trade import solve
from traderequests import buy, sell
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

indexes = ['BTCUSDT.P', 'RENUSDT.P']
amounts = {'BTCUSDT.P': 0,
           'RENUSDT.P': 0}


def summ(res: float, amount: float) -> float:
    pass


async def trade(index: str, wallet: float):
    result = solve(index)
    if result > 0.5:
        try:
            buy(index, summ(result, wallet))
        except Exception as e:
            logging.error(f'NOT BOUGHT {index} {summ(result, wallet)} {e}')
        else:
            logging.info(f'BOUGHT {index} {summ(result, wallet)}')
    elif result < 0.5:
        try:
            sell(index, summ(result, wallet))
        except Exception as e:
            logging.error(f'NOT SOLD {index} {summ(result, wallet)} {e}')
        else:
            logging.info(f'SOLD {index} {summ(result, wallet)}')


def main():
    loop = asyncio.get_event_loop()
    tasks = []
    for i in indexes:
        tasks.append(loop.create_task(trade(i, amounts[i])))
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    pb = Bybit(API_KEY2, API_SECRET2)
    x = pb.create_order('RENUSDT', 'Buy', 100, 0.098, tp=0.1, sl=0.09)
    print(x)
    orId = x['result']['orderId']
    time.sleep(0.5)
    y = pb.amend_order('RENUSDT', 95, 0.1, orId, tp=0.1, sl=0.09)
    print(y)
    time.sleep(5)
    y = pb.cancel_order('RENUSDT', orId)
    print(y)

    # main()
