import pandas as pd

# Load the file
df = pd.read_csv('genz_money_spends.csv')

# Exclude ID and Age columns to focus only on financials
financial_cols = [c for c in df.columns if c not in ['ID', 'Age']]

# Let's see the total amount across the entire dataset for each column
total_amounts = df[financial_cols].sum()

# Identify the income column and the spending/savings columns
income_col = 'Income (USD)'
spending_saving_cols = [c for c in financial_cols if c != income_col]

# Calculate total pool of income and total pool of tracked allocations
total_income = df[income_col].sum()

# Calculate global percentages relative to Total Income
global_percentages = (df[spending_saving_cols].sum() / total_income) * 100

print("Global Percentages relative to Total Income:")
print(global_percentages.round(2))

# Also calculate percentages relative to Total Expenditures/Allocations combined
total_allocations = df[spending_saving_cols].sum().sum()
global_share_of_wallet = (df[spending_saving_cols].sum() / total_allocations) * 100

print("\nGlobal Share of Wallet (Relative to total money allocated):")
print(global_share_of_wallet.round(2))
