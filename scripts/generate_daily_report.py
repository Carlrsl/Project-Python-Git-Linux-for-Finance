import sys
import os
import pandas as pd
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_loader import get_data

def generate_report():
    # 1. Configuration
    tickers = "AAPL,MSFT,BTC-USD,EURUSD=X"
    today_str = datetime.now().strftime("%Y-%m-%d")
    report_folder = os.path.join("data", "reports")
    
    # Ensure the report directory exists
    os.makedirs(report_folder, exist_ok=True)
    report_path = os.path.join(report_folder, f"report_{today_str}.txt")

    print(f"[INFO] Starting daily report generation for {today_str}...")

    # 2. Fetch Data (Last 5 days to calculate recent variations)
    try:
        df = get_data(tickers, period="5d")
        
        if df.empty:
            print("[ERROR] No data retrieved. Aborting report.")
            return

        # 3. Generate Content
        lines = []
        lines.append(f"DAILY FINANCIAL REPORT - {today_str}")
        lines.append("=" * 40)
        lines.append(f"Generated at: {datetime.now().strftime('%H:%M:%S')}\n")
        lines.append(f"{'ASSET':<10} | {'CLOSE':<10} | {'RETURN 1D':<10} | {'VOLATILITY (5D)':<15}")
        lines.append("-" * 55)

        # Calculate metrics for each asset
        for ticker in df.columns:
            # Get the last 2 prices
            series = df[ticker].dropna()
            if len(series) < 2:
                continue
            
            current_price = series.iloc[-1]
            prev_price = series.iloc[-2]
            daily_return = (current_price / prev_price) - 1
            
            # Simple volatility (std dev of last 5 days returns)
            recent_vol = series.pct_change().std()

            lines.append(f"{ticker:<10} | {current_price:<10.2f} | {daily_return:<10.2%} | {recent_vol:<15.2%}")

        # 4. Save to File
        with open(report_path, "w") as f:
            f.write("\n".join(lines))
        
        print(f"[SUCCESS] Report saved to: {report_path}")

    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")

if __name__ == "__main__":
    generate_report()