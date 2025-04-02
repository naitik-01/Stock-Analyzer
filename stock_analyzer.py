import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, ttk  # Added ttk for dropdown

# Function to fetch and plot stock data
def fetch_stock_data():
    stock_symbol = stock_var.get().upper()  # Get selected stock symbol

    if not stock_symbol:
        messagebox.showerror("Error", "Please enter or select a stock symbol!")
        return

    try:
        # Fetch stock data
        stock = yf.Ticker(stock_symbol)
        df = stock.history(period="6mo")

        if df.empty:
            messagebox.showerror("Error", "Invalid stock symbol or no data available!")
            return

        # Calculate moving averages
        df["50_MA"] = df["Close"].rolling(window=50).mean()
        df["200_MA"] = df["Close"].rolling(window=200).mean()

        # Plot stock price & moving averages
        plt.figure(figsize=(12,6))
        plt.plot(df.index, df['Close'], label="Closing Price", color='blue')
        plt.plot(df.index, df['50_MA'], label="50-Day MA", color='red')
        plt.plot(df.index, df['200_MA'], label="200-Day MA", color='green')
        plt.title(f"{stock_symbol} Stock Price (Last 6 Months)")
        plt.xlabel("Date")
        plt.ylabel("Stock Price (USD)")
        plt.legend()
        plt.grid()
        plt.show()

        # Plot trading volume
        plt.figure(figsize=(12,6))
        plt.bar(df.index, df['Volume'], color='gray', alpha=0.6)
        plt.title(f"{stock_symbol} Trading Volume")
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.grid()
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {str(e)}")

# Create UI
root = tk.Tk()
root.title("Stock Analysis Tool")
root.geometry("400x250")

# Label
tk.Label(root, text="Enter or Select Stock Symbol:", font=("Arial", 12)).pack(pady=10)

# Stock symbol input field + dropdown
stock_var = tk.StringVar()
stock_entry = ttk.Combobox(root, textvariable=stock_var, font=("Arial", 12), width=20)

# Suggested stock symbols
stock_entry['values'] = ("AAPL", "TSLA", "GOOGL", "MSFT", "AMZN")
stock_entry.pack(pady=5)

# Button to fetch stock data
fetch_button = tk.Button(root, text="Analyze Stock", font=("Arial", 12), command=fetch_stock_data)
fetch_button.pack(pady=10)

# Run the Tkinter app
root.mainloop()
