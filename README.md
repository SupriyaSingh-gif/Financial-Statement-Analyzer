# Financial-Statement-Analyzer
 Ratio analysis, Trend Charts, and Red-Flag Alerts 
import yfinance as yf

# Pick one company to start with
ticker = yf.Ticker("AAPL")

# Pull the three core financial statements
income_stmt = ticker.income_stmt
balance_sheet = ticker.balance_sheet
cashflow = ticker.cashflow

# Print them so you can see what you're working with
print("INCOME STATEMENT")
print(income_stmt)
print("\nBALANCE SHEET")
print(balance_sheet)
print("\nCASH FLOW")
print(cashflow)