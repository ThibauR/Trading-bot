import time
import numpy as np


## This function is used to calculate and return the RSI indicator.
def get_RSI(prices, rsiType=14):
	""" 
	This function uses 2 parameters to calculate the RSI-
	
	[PARAMETERS]
		prices	: The prices to be used.
		rsiType : The interval type.
	
	[CALCULATION]
		---
	
	[RETURN]
		[
		float,
		float,
		... ]
	"""
	prices 	= np.flipud(np.array(prices))
	deltas 	= np.diff(prices)
	rsi 	= np.zeros_like(prices)
	seed 	= deltas[:rsiType+1]
	up 		= seed[seed>=0].sum()/rsiType
	down 	= abs(seed[seed<0].sum()/rsiType)
	rs 		= up/down
	rsi[-1] = 100 - 100 /(1+rs)

	for i in range(rsiType, len(prices)):
		cDeltas = deltas[i-1]

		if cDeltas > 0:
			upVal = cDeltas
			downVal = 0
		else:
			upVal = 0
			downVal = abs(cDeltas)

		up = (up*(rsiType-1)+upVal)/rsiType
		down = (down*(rsiType-1)+downVal)/rsiType

		rs = up/down
		rsi[i] = 100 - 100 /(1+rs)

	fRSI = np.flipud(np.array(rsi[rsiType:]))

	return fRSI.round(2)


def get_stochastics(priceClose, priceHigh, priceLow, period=14):

	span = len(priceClose)-period
	stochastic = np.array([[priceHigh[i:period+i].max()-priceLow[i:period+i].min(), priceClose[i]-priceLow[i:period+i].min()] for i in range(span)])

	return stochastic


## This function is used to calculate and return the stochastics RSI indicator.
def get_stochRSI(prices, rsiPrim=14, rsiSecon=14, K=3, D=3):
	"""
	This function uses 3 parameters to calculate the  Stochastics RSI-
	
	[PARAMETERS]
		prices	: A list of prices.
		rsiType : The interval type.
		ind_span: The span of the indicator.
	
	[CALCULATION]
		---
	
	[RETURN]
		[{
		"%K":float,
		"%D":float
		}, ... ]
	"""
	span = len(prices)-rsiPrim-rsiSecon-K
	RSI = get_RSI(prices, rsiType=rsiPrim)
	
	return get_S_O(RSI, RSI, RSI, period=rsiSecon, K=K, D=D)
