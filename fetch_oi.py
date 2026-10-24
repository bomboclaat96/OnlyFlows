import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def fetch_open_interest(ticker_symbol):
    print(f"Hole Daten für {ticker_symbol}...")
    stock = yf.Ticker(ticker_symbol)
    expirations = stock.options

    if not expirations:
        print(f"Keine Optionsdaten für {ticker_symbol} gefunden.")
        return None

    # Wir nehmen den nächsten Verfallstag als Beispiel
    next_expiry = expirations[0]
    opt_chain = stock.option_chain(next_expiry)

    calls = opt_chain.calls[['contractSymbol', 'strike', 'openInterest', 'volume', 'impliedVolatility']].copy()
    puts = opt_chain.puts[['contractSymbol', 'strike', 'openInterest', 'volume', 'impliedVolatility']].copy()

    calls['type'] = 'CALL'
    puts['type'] = 'PUT'

    df = pd.concat([calls, puts])
    df['ticker'] = ticker_symbol
    df['expiry'] = next_expiry
    df['date'] = datetime.now().strftime('%Y-%m-%d')

    return df

if __name__ == "__main__":
    # Ordner erstellen, falls nicht vorhanden
    os.makedirs("data", exist_ok=True)

    # Liste deiner Lieblings-Assets
    tickers = ["NVDA", "AMD", "NFLX"]
    all_data = []

    for t in tickers:
        df_t = fetch_open_interest(t)
        if df_t is not None:
            all_data.append(df_t)

    if all_data:
        final_df = pd.concat(all_data)
        file_path = "data/oi_snapshot.csv"
        final_df.to_csv(file_path, index=False)
        print(f"Daten erfolgreich gespeichert unter {file_path}")
