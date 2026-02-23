# Explore xicor (Chatterjee's correlation coefficient).
import yfinance as yf
import pandas as pd
from scipy.stats import chatterjeexi
 
# Tickers with expected directional dependency
tickers = ["^GSPC", "INDA", "MCHI", "QQQ", "MTUM", "VLUE"]
 
data = yf.download(tickers, period="3y")['Close'].pct_change().fillna(0)
 
# Matrix computation (Row X predicts Column Y)
xi_matrix = data.apply(lambda col_y:
    data.apply(lambda col_x: chatterjeexi(col_x, col_y).statistic)
)
 
print(xi_matrix)

