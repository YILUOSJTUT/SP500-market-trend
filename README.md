# SP500-market-trend

# 📈 SP500 Market Breadth Analyzer

This project analyzes the **recent decline behavior** of the U.S. stock market, focusing on stocks in the S&P 500 index. As of early April 2025, U.S. equities have experienced a noticeable downturn. In response, this project aims to identify potential **buy-in opportunities** by analyzing market breadth data and investor sentiment on a daily basis.

## 🎯 Motivation

When markets fall broadly, it raises the question: **When is the best time to buy?**

To explore this, we monitor two key indicators:
1. **Percentage of S&P 500 stocks that decline on a given day**
2. **Percentage of total trading volume that goes into declining stocks**

📌 Our hypothesis:  
When **both metrics exceed 80%**, the market may be experiencing **capitulation** — a potential buy signal for long-term investors.

---

## 🚀 What It Does

- 📉 Calculates % of stocks declining per trading day
- 📊 Calculates % of volume concentrated in declining stocks
- 📈 Plots daily trends to visualize extreme market-wide selloffs
- ⏰ Runs **daily** using GitHub Actions (on weekdays)
- 💾 Automatically saves and commits updated charts to this repository

---

## 🔧 Tools Used

- Python 3.10
- Libraries: `yfinance`, `pandas`, `matplotlib`, `lxml`
- GitHub Actions for automation and scheduling

---

## 📅 Project Info

- **Start Date**: April 5, 2025
- **Maintainer**: YI LUO
- **Data Source**: Yahoo Finance via the `yfinance` API
- **Update Frequency**: Daily (Weekdays @ 4 PM UTC)

---

## 📊 Output Example

Each day, a plot is generated showing the trend of the two key indicators. When both spike above 80%, it may represent an optimal time to investigate potential entry points into the market.

Stay tuned, as this tool will evolve and expand to cover other indices or incorporate sentiment/news signals.
