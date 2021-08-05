# Binance-Trading-Bot
 Trading bot that uses Relative Strength Index (RSI) to determine when to buy or sell

## Details
Features:
* The RSI provides signals that tell investors to buy when the currency is oversold and to sell when it is overbought.
* When RSI reaches 30 and you're not in position, bot will try to buy.
* When RSI reaches 70, you're in position and sell price is higher than buy price, bot will try to sell.

## Usage
* Run `pip install -r requirements.txt` to install all required modules.
* Enter your personal binance keys in config.py files.
* Change TRADE_SYMBOL if you want to trade different token pair (Default = ETH/USDT).
* Change TRADE_QUANTITY if you want to trade different amount of coins.
* If you're already in position, change in_position to True and set buyPrice to your buy price.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Support or Contact
I am open to suggestions and learning about new techniques that can help me improve my skills.

Have any recommendations or interested in contacting me? Send me a message! 

My email is karroge10@gmail.com.

My personal website is egorkabantsov.netlify.app

