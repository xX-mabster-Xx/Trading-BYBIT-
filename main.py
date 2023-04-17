import asyncio
import json
import time

from CONFIG import API_KEY, API_SECRET, API_KEY2, API_SECRET2
from bybit import Bybit_v5, create_batch_order
import pybit.exceptions
from trade import solve
from traderequests import buy, sell
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

indexes = ['BTCUSDT.P', 'RENUSDT.P']
amounts = {'BTCUSDT.P': 0,
           'RENUSDT.P': 0}

work = True
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


def net_strategy(symbol: str = 'RENUSDT', space_to_start: float = 0.00015, step: float = 0.00025, float_digits: int = 5,
                 qty1: float = 0.3, steps: int = 14, eps: float = 0.00003):
    if pb.get_position_info(symbol, 20)['result']['list'][0]['side'] != 'None':
        return

    while work:
        price = float(pb.get_kline(symbol, 15, 1)['result']['list'][0][4])+eps
        qty = qty1
        buy_orders = []
        sell_orders = []
        buy_sum = 0
        sell_sum = 0
        sum_qty = 0
        for i in range(steps):
            sum_qty += qty
            buy_sum += float(f"%.{float_digits}f" % (price - space_to_start - i * step)) * qty
            sell_sum += float(f"%.{float_digits}f" % (price + space_to_start + i * step)) * qty
            buy = pb.create_order(symbol=symbol, side='Buy', qty=str(qty),
                                  price=str(float(f"%.{float_digits}f" % (price - space_to_start - i * step))),
                                  takeProfit = f"%.{float_digits}f" % (buy_sum / sum_qty + step),
                                  category='inverse', orderType='Limit')
            sell = pb.create_order(symbol=symbol, side='Sell', qty=str(qty),
                                   price=str(float(f"%.{float_digits}f" % (price + space_to_start + i * step))),
                                   takeProfit=f"%.{float_digits}f" % (sell_sum / sum_qty - step),
                                   category='inverse', orderType='Limit')
            buy_orders.append(buy['result']['orderId'])
            sell_orders.append(sell['result']['orderId'])
            logging.info(buy)
            logging.info(sell)
            qty *= 2
        started = False
        while True:
            position = pb.get_position_info(symbol, 15)
            if not started:
                if position['result']['list'][0]['side'] == 'Sell' and len(buy_orders) > 0:
                    started = True
                    for order in buy_orders:
                        try:
                            pb.cancel_order(symbol=symbol, orderId=order)
                        except pybit.exceptions.InvalidRequestError:
                            pass
                if position['result']['list'][0]['side'] == 'Buy' and len(sell_orders) > 0:
                    started = True
                    for order in sell_orders:
                        try:
                            pb.cancel_order(symbol=symbol, orderId=order)
                        except pybit.exceptions.InvalidRequestError:
                            pass
            else:
                avg = float(position['result']['list'][0]['avgPrice'])
                if position['result']['list'][0]['side'] == 'Sell' and f"%.{float_digits}f" % (float(position['result']['list'][0]['takeProfit'])) != f"%.{float_digits}f" % (avg-step):
                    try:
                        logging.info(pb.set_position(symbol=symbol, category='inverse', positionIdx=0, takeProfit=f"%.{float_digits}f" % (avg-step)))
                    except pybit.exceptions.InvalidRequestError as e:
                        logging.warning(e)
                if position['result']['list'][0]['side'] == 'Buy' and f"%.{float_digits}f" % (float(position['result']['list'][0]['takeProfit'])) != f"%.{float_digits}f" % (avg+step):
                    try:
                        logging.info(pb.set_position(symbol=symbol, category='inverse', positionIdx=0, takeProfit=f"%.{float_digits}f" % (avg+step)))
                    except pybit.exceptions.InvalidRequestError as e:
                        logging.warning(e)
                if position['result']['list'][0]['side'] == 'None':
                    for order in sell_orders:
                        try:
                            pb.cancel_order(symbol=symbol, orderId=order)
                        except pybit.exceptions.InvalidRequestError:
                            pass
                    for order in buy_orders:
                        try:
                            pb.cancel_order(symbol=symbol, orderId=order)
                        except pybit.exceptions.InvalidRequestError:
                            pass
                    print('--------', pb.get_balance(accountType='CONTRACT', coin='USDT')['result']['list'][0]['coin'][0][
                              'walletBalance'])
                    break
            time.sleep(3)

# async def commands():
#     while True:
#         command = await loop.run_in_executor(None, input, 'command: ')
#         if command.lower() == 'stop':
#             work = False
#         if command.lower() == 'bebra':
#             print('bobus')

if __name__ == '__main__':
    pb = Bybit_v5(API_KEY2, API_SECRET2)
    work = True
    # print(pb.get_position_info('NEARUSDT', 15))
    # print(pb.set_position(symbol='RENUSDT', category='inverse', positionIdx=0, takeProfit=str(0.1059)))
    # loop = asyncio.get_event_ loop()
    # tasks = [loop.create_task(net_strategy()),
    #          loop.create_task(commands())]
    # loop.run_until_complete(asyncio.wait(tasks))
    set1 = {"steps": 7, "qty1": 38.4, "step": 0.0005}
    set2 = {"steps": 14, "qty1": 0.3, "step": 0.00025}
    set3 = {"steps": 15, "qty1": 0.1, "step": 0.00025}
    net_strategy()

