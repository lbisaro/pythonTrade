import time
import logging
from binance.lib.utils import config_logging
from binance.websocket.spot.websocket_client import SpotWebsocketClient as Client
import pandas as pd
from datetime import datetime


config_logging(logging, logging.DEBUG)

filename = 'websocket.csv'
file_object = open(filename, 'w')
string = 'event;eventDate;tradeDate;orderType;qty;price;usd;tradeId;firstId;lastId;buyerId;sellerId;'+"\n"
file_object.write(string)
file_object.close()

file_object = open(filename, 'a')

def message_handler(message):
    if message.get('e'):
      event = message.get('e')

      eventTS = pd.to_datetime(message.get('T'),unit='ms') - pd.Timedelta('03:00:00')
      eventDate = eventTS.strftime("%d/%m/%Y %H:%M:%S")
      tradeTS = pd.to_datetime(message.get('E'),unit='ms') - pd.Timedelta('03:00:00')
      tradeDate = tradeTS.strftime("%d/%m/%Y %H:%M:%S")

      if message.get('m'):
        orderType = 'Limit' # Maker crea orden tipo LIMIT
      else:
        orderType = 'Market' # Taker crea orden tipo MARKET

      qty = message.get('q')
      price = message.get('p')
      usd = "{:.2f}".format(float(message.get('q'))*float(message.get('p')))


      firstId = ''
      lastId = ''
      buyerId = ''
      sellerId = ''
      if (message.get('e')=='trade'):
        tradeId = str(message.get('t'))
        buyerId = str(message.get('b'))
        sellerId = str(message.get('a'))
      if (message.get('e')=='aggTrade'):
        tradeId = str(message.get('a'))
        firstId = str(message.get('f'))
        lastId = str(message.get('l'))

      if (message.get('e')=='aggTrade') and float(usd)>1000:
        string = event+';'+eventDate+';'+tradeDate+';'+orderType+';'+qty+';'+price+';'+usd+';'+tradeId+';'+firstId+';'+lastId+';'+buyerId+';'+sellerId+';'
        print(string)
      
        string = string+"\n"
        file_object.write(string)
      
    #else:
    #  print(message)


my_client = Client()
my_client.start()
print("\n\nStart\n\n")

my_client.agg_trade(
    symbol="btcusdt",
    id=1,
    callback=message_handler,
)

#my_client.trade(
#    symbol="btcusdt",
#    id=2,
#    callback=message_handler,
#)



time.sleep(60) # Pausa en segundos
file_object.close()
print("\n\nStop\n\n")
logging.debug("closing ws connection")
my_client.stop()