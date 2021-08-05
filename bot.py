import websocket, json, talib, numpy
import config
from binance.client import Client
from binance.enums import *

# Setting for 1 minute candles
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"

RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
# Replace with token pair you want to trade
TRADE_SYMBOL = 'ETHUSDT' 
# Replace with the quantity you want to trade
TRADE_QUANTITY = 0.01

closes = []
# If in position, replace with buy price and set in_position to True
buyPrice = 0
in_position = False

client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('sending order')
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e: 
        print("an exception occured - {}".format(e))
        return False
    
    return True

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, message):
    global closes, in_position, buyPrice

    json_message = json.loads(message)

    candle = json_message['k']
    is_candle_closed = candle['x']
    close = candle['c']

    if is_candle_closed:
        print('Candle closed at {} $'.format(close))
        closes.append(float(close))
        if len(closes) > 50:
            closes.pop(0)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)

            print('Last 10 RSI: ' , rsi[-10:])
            last_rsi = rsi[-1] 
            print('Current RSI: {}'.format(last_rsi))

            # Sell logic:
            # If rsi > 70, in position and sell price is higher than buy price : sell
            if last_rsi > RSI_OVERBOUGHT:
                if float(close) < float(buyPrice):
                    print("OVERBOUGHT: Price lower than buy price. Can't sell...")
                    print('close: ', float(close), 'buy price: ', float(buyPrice))
                else:
                    if in_position:
                        print("OVERBOUGHT: Selling...")
                        order_succeeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                        if order_succeeded:
                            in_position = False
                            buyPrice = 0;
                            print('buyPrice = ', buyPrice)
                    else:
                        print("OVERBOUGHT: Nothing owned. Can't sell...")   

            # Buy logic:
            # If rsi < 30 and not in position : buy
            if last_rsi < RSI_OVERSOLD:
                if in_position:
                    print("OVERSOLD: Already owned. Can't buy...")
                else: 
                    print('OVERSOLD: Buying...')
                    order_succeeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeeded:
                        in_position = True
                        buyPrice = float(close)
                        print('buyPrice = ', buyPrice)


ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()