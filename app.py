import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="GenZ Spend Tracker", layout="wide")
st.title("📊 GenZ Financial Spend Analysis")

# 1. Load your uploaded dataset
@st.cache_data
def load_data():
    # Make sure 'genz_money_spends.csv' is in the same folder as app.py
    return pd.read_csv("genz_money_spends.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'genz_money_spends.csv'. Please ensure it's in the application directory.")
    st.stop()

# Define the spending and saving categories present in your dataset
categories = [
    'Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)', 
    'Entertainment (USD)', 'Subscription Services (USD)', 'Education (USD)', 
    'Online Shopping (USD)', 'Savings (USD)', 'Investments (USD)', 
    'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)'
]

# 2. Sidebar to select a User ID from the dataset
st.sidebar.header("Select Profile")
user_id = st.sidebar.selectbox("Choose User ID:", df['ID'].unique())

# Extract data for the selected user
user_data = df[df['ID'] == user_id].iloc[0]
user_age = int(user_data['Age'])
user_income = user_data['Income (USD)']
user_values = [user_data[cat] for cat in categories]

# 3. Calculate the Average Peer Baseline Group (Grouping by the user's age)
peer_group = df[df['Age'] == user_age]
peer_averages = [peer_group[cat].mean() for cat in categories]

# Display summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Selected User Age", f"{user_age} years")
col2.metric("User Monthly Income", f"${user_income:,}")
col3.metric("Peer Group Size (Same Age)", f"{len(peer_group)} people")

st.markdown("---")

# 4. Generate the Comparison Bar Chart
fig_comp = go.Figure()

# Add individual user trace
fig_comp.add_trace(go.Bar(
    x=categories,
    y=user_values,
    name='Your Data',
    marker_color='#1E3A8A'
))

# Add baseline peer trace
fig_comp.add_trace(go.Bar(
    x=categories,
    y=peer_averages,
    name=f'Average Peer Baseline Group (Age {user_age})',
    marker_color='#9CA3AF'
))

# 5. FIXED: Using 'barmode' instead of 'bmode'
fig_comp.update_layout(
    barmode='group',  # <--- THIS FIXES THE VALUEERROR
    title={
        'text': "Your Data vs. Average Peer Baseline Group",
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center'
    },
    xaxis_title="Financial Categories",
    yaxis_title="Amount in USD ($)",
    legend_title="Legend",
    template="plotly_white",
    height=600
)

# Render the chart in Streamlit
st.plotly_chart(fig_comp, use_container_width=True)

# Optional: Show numerical breakdown table
with st.expander("Show Detailed Data Table"):
    comparison_table = pd.DataFrame({
        "Category": categories,
        "Your Spend ($)": user_values,
        "Peer Average ($)": [round(val, 2) for val in peer_averages]
    })
    st.dataframe(comparison_table, use_container_width=True)
