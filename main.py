import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)


def get_ratios(ticker_symbol):
    try:
        ticker = yf.Ticker(ticker_symbol)
        income_stmt = ticker.income_stmt
        balance_sheet = ticker.balance_sheet

        current_ratio = balance_sheet.loc["Current Assets"] / balance_sheet.loc["Current Liabilities"]
        net_profit_margin = income_stmt.loc["Net Income"] / income_stmt.loc["Total Revenue"]
        debt_to_equity = balance_sheet.loc["Total Liabilities Net Minority Interest"] / balance_sheet.loc["Stockholders Equity"]
        roe = income_stmt.loc["Net Income"] / balance_sheet.loc["Stockholders Equity"]

        company_ratios = pd.DataFrame({
            "Current Ratio": current_ratio,
            "Net Profit Margin": net_profit_margin,
            "Debt to Equity": debt_to_equity,
            "ROE": roe
        })
        company_ratios["Ticker"] = ticker_symbol
        return company_ratios

    except Exception as e:
        print(f"Could not process {ticker_symbol}: {e}")
        return None


# Pick companies across different industries
tickers = ["AAPL", "MSFT", "JPM", "PG", "XOM"]

results_list = [get_ratios(t) for t in tickers]
results_list = [r for r in results_list if r is not None]  # drop any that failed
all_results = pd.concat(results_list)

print("\nALL COMPANIES RATIO TABLE")
print(all_results)

# --- Export to Excel ---
with pd.ExcelWriter("data/financial_analysis.xlsx", engine="openpyxl") as writer:
    all_results.to_excel(writer, sheet_name="All Companies")
    for t in tickers:
        subset = all_results[all_results["Ticker"] == t]
        subset.to_excel(writer, sheet_name=t)

# --- Chart: Net Profit Margin trend across companies ---
for t in tickers:
    subset = all_results[all_results["Ticker"] == t].sort_index()
    plt.plot(subset.index, subset["Net Profit Margin"], marker="o", label=t)

plt.title("Net Profit Margin Trend by Company")
plt.xlabel("Year")
plt.ylabel("Net Profit Margin")
plt.legend()
plt.savefig("data/profit_margin_trend.png")
plt.show()