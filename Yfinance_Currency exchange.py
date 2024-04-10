import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the list of currencies against INR
currencies = ['EURINR=X', 'GBPINR=X', 'USDINR=X', 'JPYINR=X', 'SARUSD=X', 'CNYUSD=X']

# Define the start date
start_date = '2022-03-04'

# Set the end date to today
end_date = datetime.today().strftime('%Y-%m-%d')

# Initialize an empty dictionary to store close prices for each currency
close_prices = {}

# Fetch Forex data using yfinance for each currency
for currency in currencies:
    data = yf.download(currency, start=start_date, end=end_date)
    if not data.empty:
        close_prices[currency] = data['Close']

# Calculate SAR/INR and CNY/INR exchange rates by multiplying with USD/INR rate
usd_inr_data = close_prices.get('USDINR=X')  # Get USD/INR data
sar_usd_data = close_prices.get('SARUSD=X')  # Get SAR/USD data
cny_usd_data = close_prices.get('CNYUSD=X')  # Get CNY/USD data

if usd_inr_data is not None and sar_usd_data is not None and cny_usd_data is not None:
    # Convert SAR and CNY to INR
    close_prices['SARINR=X'] = sar_usd_data * usd_inr_data
    close_prices['CNYINR=X'] = cny_usd_data * usd_inr_data

# Convert the dictionary to a DataFrame
df = pd.DataFrame(close_prices)

# Reset index to make 'Date' a column instead of index
df.reset_index(inplace=True)

# Drop SARUSD and CNYUSD columns
df.drop(columns=['SARUSD=X', 'CNYUSD=X'], inplace=True)

# Melt the DataFrame
melted_df = pd.melt(df, id_vars=['Date'], var_name='Currency', value_name='Exchange_Rate')

# Split the 'Currency' column into 'From_Currency' and 'To_Currency'
melted_df['FCURR'] = melted_df['Currency'].str[:3]
melted_df['TCURR'] = melted_df['Currency'].str[3:6]

# Drop the original 'Currency' column
melted_df.drop(columns=['Currency'], inplace=True)

# Rename columns as per requirements
melted_df.rename(columns={'Date': 'FDATE', 'Exchange_Rate': 'RATE'}, inplace=True)

# Reorder columns
melted_df = melted_df[['FDATE', 'FCURR', 'TCURR', 'RATE']]

# Save melted DataFrame to CSV file
file_name = f"{end_date}exchange_rat.csv"
melted_df.to_csv(file_name, index=False)

print('Melted exchange rates saved to', file_name)
