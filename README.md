# trendlines
TrendLines is a PyQt5-based desktop application that fetches real-time OHLCV data  via the ccxt library, visualizes candlestick charts using mplfinance, and overlays smart trendlines, support/resistance zones, and high-volume signal markers.


# Functionality

Uses polynomial fitting to derive a "smart" trendline from the top 3 high-volume candles.
high-volume candles are  doji candles wich represents a struggle or standoff between buyers and sellers characterized by high volume exchanged.
The trend must balance between the support and resistance lines. A breakout may indicate the presence of new influencing factors.

Calculates deviation to estimate potential support/resistance zones.

Converts raw timestamped Binance data to a pandas.DataFrame and visualizes it cleanly with mplfinance.

# Installation
Clone this repository or copy the script.

Install the required libraries:

pip install PyQt5 matplotlib ccxt pandas mplfinance


#  How to Run

python trendlines.py


# Example Output
The chart includes:

Candlestick bars with volume

Navy smart trendline

Green support line

Red resistance line

Black circles for high-volume points

# Save the Plot:
The final chart is saved as a PNG file on desktop (trend_lines.png).

# Disclaimer:
This app is intended for research purposes only. The developers do not take any responsibility for any financial losses or damages resulting from the use of this app. Users are advised to make their own independent decisions and conduct thorough research before taking any actions based on the information provided by this app.

Trendlines Project. All rights reserved.

Open-source code, developed by [CHAKRAR ABDELMALIK].

