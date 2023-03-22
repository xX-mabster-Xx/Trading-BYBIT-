import asyncio
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
    main()
