# # from pybit import usdt_perpetual
import logging

from pybit.unified_trading import HTTP
# # import pybit.
import datetime
import hashlib
import hmac
import json
import time

# from CONFIG import API_KEY, API_SECRET, API_KEY2, API_SECRET2

import requests
import urllib3

from CONFIG import API_KEY2, API_SECRET2


def create_batch_order(symbol: str, side: str, qty: float, prices: list,
                     orderType: str = 'Limit', category='inverse'):

    order = {
        "category": category,
        "request": [
            {
                "symbol": symbol,
                "side": side,
                "orderType": orderType,
                "qty": str(qty),
                "price": str(i),
                "timeInForce": "GTC",
                "positionIdx": 0,
                "orderLinkId": f"test{int(i * 10000)}",
                "reduceOnly": False,
                "mmp": False
            }
         for i in prices]
    }
    return order

class Bybit_v3:
    def __init__(self, API_KEY: str, API_SECRET: str):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET

    def genSignature(self, payload1):
        time_stamp = str(int(time.time() * 10 ** 3))
        param_str = str(time_stamp) + self.API_KEY + '20000' + payload1
        hash1 = hmac.new(bytes(self.API_SECRET, "utf-8"), param_str.encode("utf-8"), hashlib.sha256)
        signature1 = hash1.hexdigest()
        return time_stamp, signature1

    def create_order(self, symbol: str, side: str, qty: float, price: float,
                     tp: float = None, sl: float = None, triggerPrice: float = None,
                     triggerDirection: int = None,
                     orderType: str = 'Limit', category='inverse'):

        triggerPrice = 'null' if triggerPrice is None else ('\"' + str(triggerPrice) + '\"')
        sl = 'null' if sl is None else ('\"' + str(sl) + '\"')
        tp = 'null' if tp is None else ('\"' + str(tp) + '\"')
        triggerDirection = 'null' if triggerDirection is None else triggerDirection
        payload = "{\n " + \
         f"\"category\": \"{category}\",\n \
         \"symbol\": \"{symbol}\",\n \
         \"isLeverage\": 0,\n \
         \"side\": \"{side}\",\n \
         \"orderType\": \"{orderType}\",\n \
         \"qty\": \"{str(qty)}\",\n \
         \"price\": \"{price}\",\n \
         \"triggerPrice\": {triggerPrice},\n \
         \"triggerDirection\": {triggerDirection},\n \
         \"triggerBy\": \"IndexPrice\",\n \
         \"orderFilter\": null,\n \
         \"orderIv\": null,\n \
         \"timeInForce\": \"GTC\",\n \
         \"positionIdx\": 0,\n \
         \"takeProfit\": {tp},\n \
         \"stopLoss\": {sl},\n \
         \"tpTriggerBy\": null,\n \
         \"slTriggerBy\": null,\n \
         \"reduceOnly\": false,\n \
         \"closeOnTrigger\": false,\n \
         \"mmp\": null\n"+"}"
        # print(payload)
        time_stamp, signature = self.genSignature(payload)
        headers = {
            'X-BAPI-API-KEY': self.API_KEY,
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': '20000',
            'X-BAPI-SIGN': signature
        }

        response = requests.request("POST", "https://api.bybit.com/v5/order/create", headers=headers, data=payload)

        return response.json()

    def amend_order(self, symbol: str, qty: float, price: float, orderId: str,
                     tp: float = None, sl: float = None, triggerPrice: float = None, category='inverse'):
        triggerPrice = 'null' if triggerPrice is None else ('\"' + str(triggerPrice) + '\"')
        sl = 'null' if sl is None else ('\"' + str(sl) + '\"')
        tp = 'null' if tp is None else ('\"' + str(tp) + '\"')
        payload = "{\n " + \
         f"\"category\": \"{category}\",\n \
         \"symbol\": \"{symbol}\",\n \
         \"orderId\": \"{orderId}\",\n \
         \"orderLinkId\": null, \n \
         \"qty\": \"{str(qty)}\",\n \
         \"price\": \"{price}\",\n \
         \"orderIv\": null,\n \
         \"triggerPrice\": {triggerPrice},\n \
         \"takeProfit\": {tp},\n \
         \"stopLoss\": {sl},\n \
         \"triggerBy\": \"IndexPrice\",\n \
         \"tpTriggerBy\": null,\n \
         \"slTriggerBy\": null\n" + "}"
        # print(payload)
        time_stamp, signature = self.genSignature(payload)
        headers = {
            'X-BAPI-API-KEY': self.API_KEY,
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': '20000',
            'X-BAPI-SIGN': signature
        }

        response = requests.request("POST", "https://api.bybit.com/v5/order/amend", headers=headers, data=payload)

        return response.json()

    def cancel_order(self, symbol: str, orderId: str, category='inverse'):

        payload = "{\n " + \
         f"\"category\": \"{category}\",\n \
         \"symbol\": \"{symbol}\",\n \
         \"orderId\": \"{orderId}\",\n \
         \"orderLinkId\": null" + "}"
        # print(payload)
        time_stamp, signature = self.genSignature(payload)
        headers = {
            'X-BAPI-API-KEY': self.API_KEY,
            'X-BAPI-TIMESTAMP': time_stamp,
            'X-BAPI-RECV-WINDOW': '20000',
            'X-BAPI-SIGN': signature
        }

        response = requests.request("POST", "https://api.bybit.com/v5/order/cancel", headers=headers, data=payload)

        return response.json()
    def get_kline(self, symbol: str, interval: int, limit: int, category='inverse'):
        url = f"https://api.bybit.com/v5/market/index-price-kline/?category={category}&symbol={symbol}&interval={interval}&limit={limit}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)

        return response

    def get_position_info(self,symbol:str, limit:int, category:str = 'inverse'):
        session = HTTP(
            testnet=False,
            api_key=self.API_KEY,
            api_secret=self.API_SECRET,
        )
        return session.get_positions(
            category=category,
            symbol=symbol,
        )

def to_str(x):
    if x is not None:
        return str(x)
    else:
        return None
class Bybit_v5:
    def __init__(self, API_KEY: str, API_SECRET: str):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.session = HTTP(
            testnet=False,
            api_key=self.API_KEY,
            api_secret=self.API_SECRET,
        )

    def create_order(self, **kwargs):
        response = self.session.place_order(**kwargs)
        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response

    def amend_order(self, symbol: str, qty: float, price: float, orderId: str,
                     tp: float = None, sl: float = None, triggerPrice: float = None, category='inverse'):
        response = self.session.amend_order(
            category=category,
            orderId=orderId,
            symbol=symbol,
            triggerPrice=triggerPrice,
            qty=to_str(qty),
            price=to_str(price),
            takeProfit=to_str(tp),
            stopLoss=to_str(sl),
        )

        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response

    def cancel_order(self, symbol: str, orderId: str, category='inverse'):
        response = self.session.cancel_order(
            category= category,
            symbol=symbol,
            orderId=orderId,
        )
        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response
    def get_kline(self, symbol: str, interval: int, limit: int, category='inverse'):
        response = self.session.get_index_price_kline(
            category= category,
            symbol= symbol,
            interval=interval,
            limit=limit,
        )
        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response

    def get_position_info(self,symbol:str, limit:int, category:str = 'inverse'):

        response =  self.session.get_positions(
            category=category,
            symbol=symbol,
        )
        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response
    def set_position(self, **kwargs):
        response = self.session.set_trading_stop(
            **kwargs
        )
        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response

    def get_balance(self, **kwargs):
        response =  self.session.get_wallet_balance(
            **kwargs
        )
        if type(response) is dict and 'ret_msg' in response and response['ret_msg'] == 'Too many visits!':
            logging.warning('SPEED LIMIT!!!!')
        return response

if __name__ == '__main__':
    pb = Bybit_v5(API_KEY2, API_SECRET2)
    print(pb.get_balance(accountType='CONTRACT', coin='USDT')['result']['list'][0]['coin'][0]['walletBalance'])