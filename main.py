import asyncio
import json
import time

from CONFIG import API_KEY, API_SECRET, API_KEY2, API_SECRET2
from bybit import Bybit_v5, create_batch_order
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
    # loop = asyncio.get_event_loop()
    # tasks = []
    # for i in indexes:
    #     tasks.append(loop.create_task(trade(i, amounts[i])))
    # loop.run_until_complete(asyncio.wait(tasks))
    pass


def net_strategy():
    # print(pb.get_position_info('RENUSDT', 20))
    #
    while True:
        price = float(pb.get_kline('RENUSDT', 15, 1)['result']['list'][0][4])
        qty = 0.1
        buy_orders = []
        sell_orders = []
        for i in range(14):
            buy = pb.create_order(symbol='RENUSDT', side='Buy', qty=str(qty),
                                  price=str(float("%.5f" % (price - 0.0002 - i * 0.00025))),
                                  category='inverse', orderType='Limit')
            sell = pb.create_order(symbol='RENUSDT', side='Sell', qty=str(qty),
                                   price=str(float("%.5f" % (price + 0.0002 + i * 0.00025))),
                                   category='inverse', orderType='Limit')
            buy_orders.append(buy['result']['orderId'])
            sell_orders.append(sell['result']['orderId'])
            logging.info(buy)
            logging.info(sell)
            qty *= 2
        while True:
            position = pb.get_position_info()
            if position['result']['list'][0]['side'] == 'Sell' and len(buy_orders) > 0:
                for order in buy_orders:
                    pb.cancel_order(symbol='RENUSDT', orderId=order)
            if position['result']['list'][0]['side'] == 'Buy' and len(sell_orders) > 0:
                for order in sell_orders:
                    pb.cancel_order(symbol='RENUSDT', orderId=order)
            avg = float(position['result']['list'][0]['avgPrice'])
            if position['result']['list'][0]['side'] == 'Sell' and float(position['result']['list'][0]['takeProfit']) != avg-0.00025:
                print(pb.set_position(symbol='RENUSDT', category='inverse', positionIdx=0, takeProfit=str(avg-0.00025)))
            if position['result']['list'][0]['side'] == 'Buy' and float(position['result']['list'][0]['takeProfit']) != avg+0.00025:
                print(pb.set_position(symbol='RENUSDT', category='inverse', positionIdx=0, takeProfit=str(avg+0.00025)))
            if position['result']['list'][0]['side'] == 'None':
                break
            time.sleep(5)

if __name__ == '__main__':
    pb = Bybit_v5(API_KEY2, API_SECRET2)
    # print(pb.get_position_info('NEARUSDT', 15))
    # print(pb.set_position(symbol='RENUSDT', category='inverse', positionIdx=0, takeProfit=str(0.1059)))
    net_strategy()


