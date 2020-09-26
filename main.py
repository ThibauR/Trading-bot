import os
from time import sleep

from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor
import pandas as pd

#place keys between ''
api_key = ''
api_secret = ''
client = Client(api_key, api_secret)

def topup_bnb(min_balance: float, topup: float):
	bnb_balance = client.get_asset_balance(asset='BNB')
	bnb_balance = float(bnb_balance['free'])
	if bnb_balance < min_balance:
		qty = round(topup - bnb_balance, 5)
		print(qty)
		order = client.order_market_buy(symbol='BNBUSDT', quantity=qty)
		return order
	return False

#topup_bnb, if less than 0.5 BNB is available. Top up till 1.5 BNB
min_balance = 0.5
topup = 1.5
order = topup_bnb(min_balance, topup)

#check max buy amount
def buyAmount(coin, pair):
	balanceBuy = float(client.get_asset_balance(coin,
	recvWindow=10000)['free'])
	close = float(client.get_symbol_ticker(symbol=pair)['price'])
	maxBuy = round(balanceBuy / close * .995, 5)
	return maxBuy


#check max amount to sell
def sellAmount(coin):
	balanceSell = float(client.get_asset_balance(coin,
	recvWindow=10000)['free'])
	maxSell = round(balanceSell * .995, 5)
	return maxSell


#create test buy order
def buy(amount, pair):
	client.create_test_order(
		symbol=pair,
		side=Client.SIDE_BUY,
		type=Client.ORDER_TYPE_MARKET,
		quantity=amount,
		recvWindow=10000)
	print('Buy: {}'.format(amount))

#create test sell order
def sell(amount, pair):
	client.create_test_order(
		symbol=pair,
		side=Client.SIDE_SELL,
		type=Client.ORDER_TYPE_MARKET,
		quantity=amount,
		recvWindow=10000)
	print('Sell: {}'.format(amount))

#buy BTC with  USDT
maxBuy = buyAmount('USDT', 'BTCUSDT')
buy(maxBuy, 'BTCUSDT')

#sell alle BTC for USDT
maxSell = sellAmount('BTC')
sell(maxSell, 'BTCUSDT')


# show recent trades
trades = client.get_recent_trades(symbol='BTCUSDT')
print("\nRecent Trades: ", trades)
print("Local Time: ", time.localtime())
print("Recent Trades Time: ", convert_time_binance(trades[0]['time']))