import matplotlib.pyplot as plt
import seaborn as sns

# Clean the labels for the chart
labels = [c.replace(' (USD)', '') for c in global_share_of_wallet.index]
sizes = global_share_of_wallet.values

# Create a nice horizontal bar chart for the wallet share
plt.figure(figsize=(10, 6))
sns.barplot(x=sizes, y=labels, palette='viridis')
plt.title('Global Gen-Z Share of Wallet (%) \n(Where does every dollar allocated go?)')
plt.xlabel('Percentage of Total Financial Allocations (%)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('global_genz_spend.png')
plt.close()
