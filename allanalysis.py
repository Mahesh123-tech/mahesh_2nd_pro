import pandas as pd
df = pd.read_csv('genz_money_spends.csv')
print(df.head())
print(df.info())

# Let's see what the user wants: "i want to like the average global percentages like this"
# Looking at the columns, let's calculate the average percentage breakdown of where Gen Z spends/allocates their total money.
# Wait, let's look at what columns are spending vs savings/investments.
# Columns: 'Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)', 'Entertainment (USD)', 'Subscription Services (USD)', 'Education (USD)', 'Online Shopping (USD)', 'Savings (USD)', 'Investments (USD)', 'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)'

categories = [
    'Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)', 'Entertainment (USD)', 
    'Subscription Services (USD)', 'Education (USD)', 'Online Shopping (USD)', 
    'Savings (USD)', 'Investments (USD)', 'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)'
]

# Calculate total allocation per row or check if Income matches sum of allocations.
df['Total_Allocation'] = df[categories].sum(axis=1)

print(df[['Income (USD)', 'Total_Allocation']].head())

# Let's find the average spending/allocation across all records as global percentages
mean_spends = df[categories].mean()
total_mean = mean_spends.sum()
percentage_spends = (mean_spends / total_mean) * 100

print("\nAverage Allocations:")
for cat, val, pct in zip(categories, mean_spends, percentage_spends):
    print(f"{cat.replace(' (USD)', '')}: ${val:.2f} ({pct:.2f}%)")

import matplotlib.pyplot as plt
import seaborn as sns

# Let's sort the percentages for better presentation
percentage_df = pd.DataFrame({
    'Category': [c.replace(' (USD)', '') for c in categories],
    'Percentage': percentage_df_vals := (df[categories].sum() / df[categories].sum().sum() * 100).values
}).sort_values(by='Percentage', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Percentage', y='Category', data=percentage_df, palette='viridis')
plt.title('Average Budget Allocation Percentages (genz_money_spends.csv)')
plt.xlabel('Percentage (%)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('budget_allocation.png')
print(percentage_df)

# Correcting syntax error
import matplotlib.pyplot as plt
import seaborn as sns

pct_vals = (df[categories].sum() / df[categories].sum().sum() * 100).values
percentage_df = pd.DataFrame({
    'Category': [c.replace(' (USD)', '') for c in categories],
    'Percentage': pct_vals
}).sort_values(by='Percentage', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='Percentage', y='Category', data=percentage_df, palette='viridis')
plt.title('Average Global Allocation Percentages (genz_money_spends.csv)')
plt.xlabel('Percentage (%)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('budget_allocation.png')
print(percentage_df)
