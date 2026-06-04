import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Page Configuration
st.set_page_config(
    page_title="GenZ Money Spends Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for fine-tuning UI cards and elements
st.markdown("""
<style>
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 700;
        color: #6366F1;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #475569;
        font-weight: 500;
    }
    .card-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 15px;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# 2. Optimized Data Loading with Caching
@st.cache_data
def load_data():
    # Attempts to look up data directory first, falls back to root folder
    try:
        data = pd.read_csv('data/genz_money_spends.csv')
    except FileNotFoundError:
        data = pd.read_csv('genz_money_spends.csv')
    return data

df = load_data()

# Expense classification mapping
expense_cols = [
    'Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)', 
    'Entertainment (USD)', 'Subscription Services (USD)', 
    'Education (USD)', 'Online Shopping (USD)', 
    'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)'
]

# 3. Sidebar Filtering Options
st.sidebar.title("🎛️ Filter Controls")
st.sidebar.markdown("Slice the analytics engine based on specific age demographics.")

min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range Cohort", min_age, max_age, (min_age, max_age))

# Dynamic subset generation based on selection
filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]

# Main Dashboard Frame
st.title("💳 GenZ Money Spends & Financial Behavior")
st.markdown("An interactive analytics dashboard tracking income distribution, spending choices, and asset accumulation patterns.")

# 4. KPI Scorecard Metrics Layer
st.markdown("---")
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(label="👥 Sample Cohort Size", value=f"{len(filtered_df):,}")
with m2:
    st.metric(label="💵 Avg Monthly Income", value=f"${filtered_df['Income (USD)'].mean():,.2f}")
with m3:
    st.metric(label="🐖 Avg Monthly Savings", value=f"${filtered_df['Savings (USD)'].mean():,.2f}")
with m4:
    st.metric(label="📈 Avg Monthly Investments", value=f"${filtered_df['Investments (USD)'].mean():,.2f}")

st.markdown("---")

# 5. UI Tabbing Structuring
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Spending Allocation Breakdown", 
    "👶 Age-Wise Cohort Trends", 
    "🎯 Income & Accumulation Dynamics", 
    "🔮 Interactive Benchmark Calculator"
])

# TAB 1: Spending Allocations
with tab1:
    st.markdown("<p class='card-title'>Where is the Money Going?</p>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    # Calculate Mean Distribution Breakdown
    mean_expenses = filtered_df[expense_cols].mean().reset_index()
    mean_expenses.columns = ['Expense Category', 'Average Amount']
    mean_expenses = mean_expenses.sort_values(by='Average Amount', ascending=False)
    
    with col1:
        # Donut Chart for Expense Share
        fig_donut = px.pie(
            mean_expenses, 
            values='Average Amount', 
            names='Expense Category', 
            hole=0.45,
            color_discrete_sequence=px.colors.sequential.Indigo_r,
            title="Percentage Share of Core Expenses"
        )
        fig_donut.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig_donut, use_container_width=True)
        
    with col2:
        # Horizontal Bar Chart for Categorical Rankings
        fig_bar = px.bar(
            mean_expenses,
            x='Average Amount',
            y='Expense Category',
            orientation='h',
            text_auto='.2s',
            color='Average Amount',
            color_continuous_scale='indigo',
            title="Ranked Average Categorical Outflows"
        )
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig_bar, use_container_width=True)

# TAB 2: Age Cohort Analysis
with tab2:
    st.markdown("<p class='card-title'>Financial Progression by Age Metric</p>", unsafe_allow_html=True)
    
    # Aggregate attributes by age
    age_grouped = filtered_df.groupby('Age')[['Income (USD)', 'Savings (USD)', 'Investments (USD)']].mean().reset_index()
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=age_grouped['Age'], y=age_grouped['Income (USD)'], name='Avg Income', line=dict(color='#6366F1', width=3)))
    fig_line.add_trace(go.Scatter(x=age_grouped['Age'], y=age_grouped['Savings (USD)'], name='Avg Savings', line=dict(color='#10B981', width=2, dash='dash')))
    fig_line.add_trace(go.Scatter(x=age_grouped['Age'], y=age_grouped['Investments (USD)'], name='Avg Investments', line=dict(color='#F59E0B', width=2, dash='dot')))
    
    fig_line.update_layout(
        title="Income vs Capital Allocation Across Age Demographics",
        xaxis_title="Age (Years)",
        yaxis_title="Amount in USD ($)",
        hovermode="x unified",
        margin=dict(t=40, b=40, l=40, r=40)
    )
    st.plotly_chart(fig_line, use_container_width=True)

# TAB 3: Correlations & Cross Plots
with tab3:
    st.markdown("<p class='card-title'>Income Scaling vs Wealth Building Behavior</p>", unsafe_allow_html=True)
    
    col3_1, col3_2 = st.columns(2)
    
    with col3_1:
        fig_scatter_inv = px.scatter(
            filtered_df,
            x='Income (USD)',
            y='Investments (USD)',
            color='Age',
            color_continuous_scale='Viridis',
            opacity=0.7,
            title="Correlation Spectrum: Income vs. Investments"
        )
        st.plotly_chart(fig_scatter_inv, use_container_width=True)
        
    with col3_2:
        fig_scatter_sav = px.scatter(
            filtered_df,
            x='Income (USD)',
            y='Savings (USD)',
            color='Age',
            color_continuous_scale='Plasma',
            opacity=0.7,
            title="Correlation Spectrum: Income vs. Savings"
        )
        st.plotly_chart(fig_scatter_sav, use_container_width=True)

# TAB 4: Personal Benchmark Tool
with tab4:
    st.markdown("<p class='card-title'>Benchmark Your Metrics Against This Cohort</p>", unsafe_allow_html=True)
    st.write("Enter your personal details below to see where you rank relative to the dataset peers.")
    
    calc_col1, calc_col2 = st.columns([1, 2])
    
    with calc_col1:
        with st.form("benchmark_form"):
            user_age = st.number_input("Your Age", min_value=min_age, max_value=max_age, value=22)
            user_income = st.number_input("Your Monthly Income (USD)", min_value=0, value=4500)
            user_savings = st.number_input("Your Monthly Savings (USD)", min_value=0, value=1200)
            user_investments = st.number_input("Your Monthly Investments (USD)", min_value=0, value=1800)
            submitted = st.form_submit_with_button("Calculate Percentiles")
            
    with calc_col2:
        if submitted:
            # Filter the peer context to exactly matches the input age
            peer_group = df[df['Age'] == user_age]
            
            if len(peer_group) > 0:
                inc_pct = (peer_group['Income (USD)'] < user_income).mean() * 100
                sav_pct = (peer_group['Savings (USD)'] < user_savings).mean() * 100
                inv_pct = (peer_group['Investments (USD)'] < user_investments).mean() * 100
                
                st.subheader(f"📊 Benchmarking Results against Age {user_age} Peer Group")
                st.markdown(f"**Income Percentile:** You earn more than **{inc_pct:.1f}%** of peers at your age.")
                st.markdown(f"**Savings Percentile:** You save more than **{sav_pct:.1f}%** of peers at your age.")
                st.markdown(f"**Investments Percentile:** You invest more than **{inv_pct:.1f}%** of peers at your age.")
                
                # Visual comparison layout
                comparison_metrics = pd.DataFrame({
                    'Metric': ['Income', 'Savings', 'Investments'],
                    '
