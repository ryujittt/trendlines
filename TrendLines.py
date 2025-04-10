import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget,QHBoxLayout,QComboBox,QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import ccxt
from PyQt5.QtCore import QTimer, Qt
import pandas as pd 
import mplfinance as mpf
import os





class TrendLines(QMainWindow):
    def __init__(self):
        super().__init__()




        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()

        self.layout = QVBoxLayout(central_widget)
        
        self.Box = QHBoxLayout()
        self.layout.addLayout(self.Box)
        



        
#         self.start = False
        self.label_symbol = QLabel()
        self.label_symbol.setText('Symbol')
        self.Box.addWidget(self.label_symbol)

        # Add QComboBox for symbol
        self.symbol_combobox = QComboBox(self)
        self.symbol_combobox.addItems(['ETH/USDT', 'BTC/USDT', 'TOMO/USDT', 'DOGE/USDT', 'BNB/USDT', 'XRP/USDT', 'LTC/USDT', 'SOL/USDT', 'ADA/USDT', 'AVAX/USDT', 'DOT/USDT'])
        self.Box.addWidget(self.symbol_combobox)
        self.symbol_combobox.setCurrentIndex(0)

        


        self.label_timeframe = QLabel()
        self.label_timeframe.setText('Timeframe')
        self.Box.addWidget(self.label_timeframe)


        
        # Add QComboBox for timeframe
        self.timeframe_combobox = QComboBox(self)
        self.timeframe_combobox.addItems(['1m', '5m', '15m', '1h'])  # Add more options as needed
        self.Box.addWidget(self.timeframe_combobox)
        self.timeframe_combobox.setCurrentIndex(0)



 
        self.label_limit = QLabel()
        self.label_limit.setText('Limit')
        self.Box.addWidget(self.label_limit)

        # Add QComboBox for limit
        self.limit_combobox = QComboBox(self)
        self.limit_combobox.addItems(['100' ,'150' , '200', '300', '400', '500', '600', '700', '800', '900', '1000'])  # Add more options as needed
        self.Box.addWidget(self.limit_combobox)
        self.limit_combobox.setCurrentIndex(3)

        
        self.label_backtime = QLabel()
        self.label_backtime.setText('BackTime')


        
        self.Box.addWidget(self.label_backtime)
        
        # Add QComboBox for limit
        self.backtime_combobox = QComboBox(self)
        self.backtime_combobox.addItems(['100' ,'150' , '200', '250', '400', '500', '600', '700', '800', '900', '1000'])  # Add more options as needed
        self.Box.addWidget(self.backtime_combobox)
        self.backtime_combobox.setCurrentIndex(3)


        # Update Button
        update_button = QPushButton('Update Data', self)
        update_button.clicked.connect(self.execute_code)
        self.layout.addWidget(update_button)




        self.setCentralWidget(central_widget)

        self.setWindowTitle('TrendLines')
#         self.setGeometry(50, 50, 400, 300)
        self.show()

        
    def execute_code(self):

        self.update_and_plot()

    def update_and_plot(self, val=None):


        # Initialize Binance exchange object
        exchange = ccxt.binance()

        # Get symbol, timeframe, limit, and backtime from user input (assuming they are instance variables in a class)
        symbol = self.symbol_combobox.currentText()
        timeframe = self.timeframe_combobox.currentText()
        limit = int(self.limit_combobox.currentText())
        backtime = int(self.backtime_combobox.currentText())

        # Fetch OHLCV data using CCXT
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

        # Convert OHLCV data to a DataFrame
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])



        # Calculate additional columns
        df['index'] = np.arange(len(df))
        df['avge_candle'] = np.mean(abs(df['high'] - df['low']))
        df['volume_ratio'] = df['volume'] / abs(1 + df['close'] - df['open'])

        avge_candle = np.mean(df['avge_candle'])
        # Get top indices
        
        added_plots = []

        # Create a Series of NaNs
        scatter_data = np.full(len(df), np.nan)

        # Fill only the top 3 volume_ratio points with some visible value (e.g., the high price or close)
        top_indices = df['volume_ratio'].argsort()[-3:]
        scatter_data[top_indices] = df['high'].iloc[top_indices]  # or df['close'].iloc[top_indices]

        # Create the addplot

        # Calculate smart line
        coefficients = np.polyfit(df['index'].iloc[top_indices], df['close'].iloc[top_indices], 1)
        smart_line = np.polyval(coefficients, df['index'])

        # Calculate support and resistance
        support_index = min(top_indices) + np.argmin(df['low'].iloc[min(top_indices):max(top_indices)])
        support_value = df['close'].iloc[support_index]
        support = smart_line - abs(support_value - smart_line[support_index])

        resistance_index = min(top_indices) + np.argmax(df['high'].iloc[min(top_indices):max(top_indices)])
        resistance_value = df['close'].iloc[resistance_index]
        resistance = smart_line + abs(resistance_value - smart_line[resistance_index])

        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        added_plots.append(mpf.make_addplot(support,  width = 1, color='green', alpha = 0.8))
        added_plots.append(mpf.make_addplot(resistance,  width = 1, color='red', alpha = 0.6))
        added_plots.append(mpf.make_addplot(smart_line,  width = 1, color='navy', alpha = 0.8))
        added_plots.append(mpf.make_addplot(scatter_data, scatter=True, markersize=20, marker='o', color='black', alpha=0.8))


            
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # Set the full path for the file
        fname = os.path.join(desktop_path, "trend_lines.png")
        mydpi = 80
        

        fig1, _ = mpf.plot(df, type='candle',style='yahoo' ,addplot=added_plots, returnfig=True,  volume=True)

          
        fig1.savefig(fname,dpi=mydpi)
        



if __name__ == '__main__':
    app =None
    app = QApplication(sys.argv)
    ex = TrendLines()
    sys.exit(app.exec_())
