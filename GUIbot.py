# Import the requests library 
import requests, time, os, math

from multiprocessing import Process
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException

indicator = "rsi","macd","avgprice","fibonacciretracement","dmi","bbands2","adx","mfi","vwap"
api_key = "" #binance api
api_secret = "" #secret here

seconds = time.time()

client = Client(api_key, api_secret)

coina = 'USDT'

coinb = 'MANA'
digitb = 1

coinc = 'CHZ'
digitc = 0

coind = 'AVAX'
digitd = 2

coine = 'DOT'
digite = 2

coinf ="BNB"
digitf = 2

coing ="BNT"
digitg = 2



class Bot:
    def __init__(self, coina, coinb,digit, indicator, client):
        self.client = client
        self.result = [0]*9
        self.endpoint = [0]*9
        self.pair = coinb +'/'+ coina
        self.bnb_api_pair = coinb + coina
        self.coina = coina
        self.coinb = coinb
        self.digit = digit
        self.buy_price = [0]
        self.sell_price = [0]
        self.profit = 0
        self.factor = 0
        self.ava_coina = float(client.get_asset_balance(asset=self.coina)['free'])
        self.ava_coinb = float(client.get_asset_balance(asset=self.coinb)['free'])
        self.isrunning = 0
        self.info_for_gui = [0]*7
        self.old_pd = 0
        self.fib = 0
        self.count = 0
        for i,value in enumerate(indicator):
            self.endpoint[i] = f"https://api.taapi.io/{value}"
        self.parameters = {
    'secret': APIKEYHERE TAAPI.io,
    'exchange': 'binance',
    'symbol':self.pair ,
    'interval': '1m',
        }
        self.fib_pram = {
    'secret': APIKEYHERE TAAPI.io,
    'exchange': 'binance',
    'symbol': self.pair,
    'interval': '1m',
    'trend':'smart'
        }
        
        
    def get_apidata(self):
     try:
        for i,value in enumerate(self.endpoint):
            if value == 'https://api.taapi.io/fibonacciretracement':
                response = requests.get(url = value, params = self.fib_pram)
                self.result[i] = response.json()    
            else:
                response = requests.get(url = value, params = self.parameters)
                self.result[i] = response.json()
                
     except:
        print("API error")
    
    def dmi(self):
     if self.result[4]["plusdi"] > self.result[4]["minusdi"] and self.result[4]['adx'] >  self.result[4]["plusdi"] and  self.result[4]['adx'] >   self.result[4]["minusdi"]:
        return 2
     if  self.result[4]["adx"] > 20:
        if  self.result[4]["plusdi"] > self.result[4]["minusdi"]:
            if self.fib > 0:
                return 1
            if self.fib < 0:
                return -1
            else:
                return 0
        if  self.result[4]["plusdi"] <  self.result[4]["minusdi"]:
            if self.fib >  0:
                return 1
            if self.fib < 0:
                return -1
            else:
                return 0
        else:
            return 0
     else:
        return 0
    def vwamp(self):
     if self.result[8]['value'] < self.result[2]['value']:
        if self.fib > 0:
            return 1
        else:
            return -1
     else:
        return 0
    def macd(self):
     if abs(self.result[1]["valueMACD"] - self.result[1]["valueMACDSignal"]/self.result[1]['valueMACD']) < 0.005:
        if self.fib > 0:
            return 1
        else:
            return -1
     else:
        return 0
    def rsi(self):
     return round(float(-((2*(self.result[0]['value']/(100-0)))-1)),2)    
    def mfi(self):
     return round(float(-((2*(self.result[7]['value']/(100-0)))-1)),2)   
    def adx(self):
     return round(float((2*(self.result[6]['value'])/(100-0))-1),2)

    #def getslope(self):
    #    if self.old_pd == 0:
    #        self.old_pd = self.result[3]['value']
    #        return 0
    #    else:
    #        self.slope = self.result[3]['value'] - self.old_pd
    #        if self.count % 5 == 0:
    #         self.old_pd = self.result[3]['value']
    #        return 0
    def fibr(self):
        
        if self.result[3]["trend"] == "DOWNTREND":
            self.fib = -1
        else:
            self.fib = 1

    def binance_info(self):
          self.ava_coina = float(client.get_asset_balance(asset=self.coina)['free'])
          self.ava_coinb = float(client.get_asset_balance(asset=self.coinb)['free'])
         
    def getfactor(self):
        if(self.adx() > 0):
            ad = self.adx()
        if(self.adx() < -0.80):
            ad = -1
        else:
            ad = 0
        self.factor = (self.rsi()+self.macd()+self.dmi()+self.mfi()+self.vwamp())*(1+ad)
        self.info_for_gui[0] = str(self.rsi())
        self.info_for_gui[1] = str(self.macd())
        self.info_for_gui[2] = str(self.dmi())
        self.info_for_gui[3] = str(self.adx())
        self.info_for_gui[4] = str(self.mfi())
        self.info_for_gui[5] = str(self.vwamp())
        self.info_for_gui[6] = str(self.result[2]['value'])
        
        
    
    def buy(self,x):
     try:
            print('buying!')
            limit_order = self.client.order_limit_buy(symbol=self.bnb_api_pair, quantity = '%f' % x, price = '%.3f' % self.result[2]['value'])
            time.sleep(10)
            if float(self.client.get_asset_balance(asset=self.coina)['locked']) >= float(x) or float(self.client.get_asset_balance(asset=self.coinb)['locked']) >= float(x*self.result[2]['value']):
                cancel = self.client.cancel_order(symbol=self.bnb_api_pair, orderId=limit_order['orderId'])

            else:
                print("bought!")
                self.buy_price.append(float(limit_order['price']))
                print(self.buy_price)
                print(limit_order)
                
     except BinanceAPIException as e:
            # error handling goes here
                print(e)
     except BinanceOrderException as e:
            # error handling goes here
                print(e)
    def sell(self,x):

     try:
            print('selling!')
            limit_order = self.client.order_limit_sell(symbol=self.bnb_api_pair, quantity = '%f' % x, price = '%.3f' % self.result[2]['value'])
            
            time.sleep(10)
            if float(self.client.get_asset_balance(asset=self.coina)['locked']) >= float(x) or float(self.client.get_asset_balance(asset=self.coinb)['locked']) >= float(x*self.result[2]['value']):
                cancel = self.client.cancel_order(symbol=self.bnb_api_pair, orderId=limit_order['orderId'])
               
            else:
                print("sold!")
                self.sell_price.append(float(limit_order['price']))
                print('sellprice: ', self.sell_price[-1])
                if self.buy_price[-1] != 0:
                 self.profit += ((self.sell_price[-1]*(float(limit_order['executedQty']))) - (self.buy_price[-1]*(float(limit_order['executedQty']))))
                 del self.buy_price[-1]
                 print(limit_order)
                
     except BinanceAPIException as e:
            # error handling goes here
                print(e)
     except BinanceOrderException as e:
            # error handling goes here
                print(e)

    def binancebot(self):

     upperbound = round(abs((self.result[5]['valueUpperBand'] - self.result[2]['value']) /self.result[5]['valueUpperBand'])*100,2)
     middlebound = round(abs((self.result[5]['valueMiddleBand'] - self.result[2]['value']) /self.result[5]['valueMiddleBand'])*100,2)
     lowerbound = round(abs((self.result[2]['value'] - self.result[5]['valueLowerBand'])/self.result[2]['value'])*100,2)
     
     if upperbound + lowerbound > .5: #if bands are too close together it wont sell
   
         if (self.factor < 0 and (self.buy_price[-1]*1.03) < self.result[2]['value']) and self.ava_coinb > round(15/self.result[2]['value'],self.digit) : #market sell at 1% gain
             print('%f' % round(15/self.result[2]['value'],self.digit))
             self.sell(round(self.ava_coinb-0.10,self.digit))
             return 0
         if (upperbound < 0.5 and (self.fib < 0 or self.factor <= -1)and (self.buy_price[-1]*1.0045 <= self.result[2]['value']) and self.ava_coinb > round(15/self.result[2]['value'],self.digit)) : #sell when near upperband,factor is less than -1 and buy price is over trade fee + 0.025% profit
             print('%f' % round(15/self.result[2]['value'],self.digit))
             self.sell(round(15/self.result[2]['value'],self.digit))
             
             return 0
         if self.buy_price[-1]*0.98 < self.result[2]['value'] and self.ava_coinb > round(15/self.result[2]['value'],self.digit) and self.fib < 0 and self.factor < 0 : #stop loss
             print('%f' % round(15/self.result[2]['value'],self.digit))
             self.sell(round(15/self.result[2]['value'],self.digit))
             if self.buy_price[-1] != 0:
              self.profit += ( (self.sell_price[-1] * self.ava_coinb) - (self.buy_price[-1] * self.ava_coinb) )
             return 0
     if  self.factor > 1.5 and self.ava_coina >= 15 and upperbound > 1 and self.fib > 0 : 
             print(round(15/self.result[2]['value'],self.digit))
             self.buy(round(15/self.result[2]['value'],self.digit))
             return 0
     if lowerbound < 0.3 and self.fib > 0 and self.ava_coina >= 15 and self.factor > 0:
             print(round(15/self.result[2]['value'],self.digit))
             self.buy(round(15/self.result[2]['value'],self.digit))
             return 0

    def info(self):
        try:
            self.binance_info()
        except:
            print('binance api not responding')
        else:
            print(self.pair)
            print('----------------------------------------------------------------------------------------------')
            print('rsi: ',self.info_for_gui[0],'macd: ',self.info_for_gui[1],'dmi: ',self.info_for_gui[2], 'adx:', self.info_for_gui[3],'mfi: ', self.info_for_gui[4],"vwamp:",self.info_for_gui[5])
            print('fib: ', self.fib)
            print("factor value: ",self.factor)
            print("price: ",round(self.result[2]['value'],8))
            print("last buy price: ", self.buy_price[-1])
            if self.buy_price[-1] != 0 :
                print("price change since buy", round(((self.result[2]['value'] - self.buy_price[-1])/self.result[2]['value'])*100,2),'%')
            print("last sell price: ", self.sell_price[-1])
            print('profit: ',self.profit)
            print(self.coina, ' :',self.ava_coina)
            print(self.coinb, ' :',self.ava_coinb)

    def mainloop(self):
         self.isrunning = 1
         self.count += 1
         try:
            self.get_apidata()
         except:
            print('issue with get_api')
         try:
            self.binance_info()
         except:
            print('issue with binance_info')
       
         self.fibr()
         self.getfactor()
         self.binancebot()
         self.info()
         print(self.result[3])   
        
         
         self.isrunning = 0
        
       




b1 = Bot(coina,coinb,digitb,indicator,client)
b2 = Bot(coina,coinc,digitc,indicator,client)
b3 = Bot(coina,coind,digitd,indicator,client)
b4 = Bot(coina,coine,digite,indicator,client)
b5 = Bot(coina,coinf,digitf,indicator,client)
b6 = Bot(coina,coing,digitg,indicator,client)
poff = 0
while True:
    if b6.isrunning == 0:
        b1.mainloop()
    if b1.isrunning == 0:
        b2.mainloop()
    if b2.isrunning == 0:
        b3.mainloop() 
    if b3.isrunning == 0:
        b4.mainloop()
    if b4.isrunning == 0:
        b5.mainloop()
    if b5.isrunning == 0:
        b6.mainloop()

    print('time running (min):', (time.time() - seconds)/60)
    
    poff += b1.profit
    poff += b2.profit
    poff += b3.profit
    poff += b4.profit
    poff += b5.profit
    poff += b6.profit
    print('profit: ', poff)




 
 









