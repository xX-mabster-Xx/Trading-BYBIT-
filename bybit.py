# # from pybit import usdt_perpetual
# from pybit.unified_trading import HTTP
# # import pybit.
import datetime
import hashlib
import hmac
import time

# from CONFIG import API_KEY, API_SECRET, API_KEY2, API_SECRET2

import requests


class Bybit:
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
        print(payload)
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

