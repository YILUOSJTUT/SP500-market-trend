#!/usr/bin/env python
# coding: utf-8
"""
📈 Stock Market Breadth Analysis — When to Buy US Stocks?
Author: YI LUO
Date: 2025-04-05

🧠 Introduction:
This project analyzes recent historical data from the S&P 500 to explore when the US stock market may be entering a "buy zone" — a condition often associated with panic selling and market bottoms. The data is sourced directly from Yahoo Finance using the `yfinance` API.

🎯 Objective:
We use two key indicators to help identify potential bottoming behavior in the stock market:
1. 📉 **Percentage of stocks declining in a single day**
2. 📊 **Percentage of total trading volume that went into declining stocks**

📌 The hypothesis: 
If both indicators exceed **80%** on the same trading day, it may suggest extreme negative sentiment — a potential signal to begin accumulating long positions (i.e., a contrarian buying opportunity).

🔍 What We Did:
- Fetched 7 days of historical data for all S&P 500 companies (adjusted for market closures).
- Calculated daily breadth statistics (declining stocks %, and volume in declining stocks %).
- Plotted the two indicators over time to visually track panic zones.

📊 Findings:
- The chart helps spot days when market-wide selling was broad and intense.
- When both metrics crossed the 80% line, these dates may represent capitulation points worth further investigation.
- This model can be extended to Russell 1000, NASDAQ-100, or sector-level analyses.

📁 Data Source:
All stock data was retrieved using the `yfinance` library from Yahoo Finance.

🛠️ Tools Used:
- Python 3.10
- pandas, matplotlib, yfinance

"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class StockMarketAnalyzer:
    def __init__(self, days=5):
        self.days = days
        self.tickers = self._get_sp500_tickers()
        self.stock_data = {}

    def _get_sp500_tickers(self):
        """Scrape S&P 500 stock tickers from Wikipedia."""
        url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        df = pd.read_html(url)[0]
        tickers = df["Symbol"].str.replace(".", "-", regex=False).tolist()
        return tickers

    def fetch_data(self):
        """Download historical OHLCV data for the given tickers over a time window."""
        end = datetime.today()
        start = end - timedelta(days=self.days * 2)  # buffer for non-trading days
        for ticker in self.tickers:
            try:
                df = yf.download(ticker, start=start, end=end, interval="1d", progress=False)
                if not df.empty:
                    df = df[["Close", "Volume"]].copy()
                    df.columns = [f"{ticker}_Close", f"{ticker}_Volume"]
                    self.stock_data[ticker] = df
            except Exception as e:
                print(f"⚠️ Failed to download {ticker}: {e}")

    def analyze_trend(self):
        """Analyze percentage of declining stocks and volume per day."""
        valid_data = [df for df in self.stock_data.values() if not df.empty]
        if not valid_data:
            print("❌ No valid stock data available.")
            return pd.DataFrame()

        combined = pd.concat(valid_data, axis=1, join='inner')
        combined.index = pd.to_datetime(combined.index)
        combined = combined.sort_index()

        trend = []

        for i in range(1, len(combined)):
            prev, curr = combined.iloc[i - 1], combined.iloc[i]
            date = combined.index[i]
            total, declining, volume, volume_decline = 0, 0, 0, 0

            for ticker in self.stock_data:
                try:
                    pc = prev[f"{ticker}_Close"]
                    cc = curr[f"{ticker}_Close"]
                    cv = curr[f"{ticker}_Volume"]
                    if pd.notna(pc) and pd.notna(cc) and pd.notna(cv):
                        total += 1
                        volume += cv
                        if cc < pc:
                            declining += 1
                            volume_decline += cv
                except KeyError:
                    continue

            if total > 0 and volume > 0:
                trend.append({
                    "Date": date,
                    "PctDeclining": declining / total * 100,
                    "PctVolumeDeclining": volume_decline / volume * 100
                })

        return pd.DataFrame(trend)

    def plot_trend(self, trend_df, save_path=None):
        """Visualize market-wide decline signals using line plots."""
        if trend_df.empty:
            print("⚠️ Nothing to plot.")
            return

        plt.figure(figsize=(12, 6))
        plt.plot(trend_df["Date"], trend_df["PctDeclining"], marker='o', label="% of Stocks Declining")
        plt.plot(trend_df["Date"], trend_df["PctVolumeDeclining"], marker='s', label="% of Volume in Declining Stocks")
        plt.axhline(80, color='red', linestyle='--', label="80% Threshold")
        plt.title("Market Breadth Analysis: % Declining Stocks and Volume")
        plt.xlabel("Date")
        plt.ylabel("Percentage (%)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()


if __name__ == "__main__":
    analyzer = StockMarketAnalyzer(days=7)
    analyzer.fetch_data()
    trend_df = analyzer.analyze_trend()
    analyzer.plot_trend(trend_df, save_path="market_trend.png")
