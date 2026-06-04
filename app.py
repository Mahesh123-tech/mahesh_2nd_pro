import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="GenZ Budget & Benchmark Tracker", layout="wide")

st.title("📊 Personal Budget Analysis & Peer Benchmarking")
st.write("Enter your profile details and monthly breakdown below to see how your spending matches up against peers.")

# 1. Load your baseline dataset safely
@st.cache_data
def load_data():
    return pd.read_csv("genz_money_spends.csv")

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'genz_money_spends.csv'. Please make sure it's in the same folder as this app.")
    st.stop()

# Define categories present in genz_money_spends.csv
categories = [
    'Rent (USD)', 'Groceries (USD)', 'Eating Out (USD)', 
    'Entertainment (USD)', 'Subscription Services (USD)', 'Education (USD)', 
    'Online Shopping (USD)', 'Savings (USD)', 'Investments (USD)', 
    'Travel (USD)', 'Fitness (USD)', 'Miscellaneous (USD)'
]

# 2. Setup the User Input Form with a Submit Button
with st.form("user_budget_form"):
    st.subheader("📋 Step 1: Your Profile & Monthly Allocations")
    
    # Form layout columns
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        user_name = st.text_input("Full Name:", value="Alex")
    with col_p2:
        user_age = st.number_input("Age:", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=22)
    with col_p3:
        user_income = st.number_input("Monthly Salary / Income (USD):", min_value=1, value=4000)
        
    st.markdown("---")
    st.markdown("##### Enter your estimated monthly allocations (in USD):")
    
    # Split the categories into two side-by-side columns for a clean look
    col_c1, col_c2 = st.columns(2)
    user_values = {}
    
    for i, cat in enumerate(categories):
        # Even indexes go to column 1, odd to column 2
        with col_c1 if i % 2 == 0 else col_c2:
            # Default values given just as a placeholder starter
            user_values[cat] = st.number_input(f"{cat}", min_value=0, value=250 if "Rent" in cat or "Savings" in cat or "Investment" in cat else 100)
            
    # Form Submission button
    submit_button = st.form_submit_button(label="Analyze & Calculate Percentages")

# 3. Process data ONLY after the form is submitted
if submit_button:
    st.markdown("---")
    st.subheader(f"👋 Results for {user_name} (Age {user_age})")
    
    # Total Allocation calculation
    total_allocated = sum(user_values.values())
    allocation_percentage = (total_allocated / user_income) * 100
    
    # Check if they went over their budget
    if total_allocated > user_income:
        st.warning(f"⚠️ **Note:** Your total allocations (${total_allocated:,}) exceed your monthly income (${user_income:,}) by **{allocation_percentage - 100:.1f}%**.")
    else:
        st.success(f"✅ **Budget Managed:** You have allocated **{allocation_percentage:.1f}%** of your total monthly income.")

    # KPI Summary Cards
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Income", f"${user_income:,}")
    kpi2.metric("Total Allocated", f"${total_allocated:,}")
    kpi3.metric("Total Income Allocated (%)", f"{allocation_percentage:.1f}%")

    # 4. Filter and Calculate the Average Peer Baseline Group
    peer_group = df[df['Age'] == user_age]
    # Fallback if specific age data is sparse
    if len(peer_group) < 5:
        peer_group = df
    
    peer_averages = [round(peer_group[cat].mean(), 2) for cat in categories]
    user_list_values = [user_values[cat] for cat in categories]

    # 5. Fixed Plotly Grouped Bar Chart Setup
    fig_comp = go.Figure()

    # User allocation trace
    fig_comp.add_trace(go.Bar(
        x=[cat.replace(" (USD)", "") for cat in categories], # Clean up label names
        y=user_list_values,
        name=f"{user_name}'s Spending",
        marker_color='#1E3A8A'
    ))

    # Peer group baseline trace
    fig_comp.add_trace(go.Bar(
        x=[cat.replace(" (USD)", "") for cat in categories],
        y=peer_averages,
        name=f"Peer Average Baseline (Age {user_age})",
        marker_color='#9CA3AF'
    ))

    # The layout update where 'barmode' fixes your error
    fig_comp.update_layout(
        barmode='group',  
        title={
            'text': f"Your Spending/Savings Breakdown vs. Peer Average Group",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center'
        },
        xaxis_title="Financial Allocation Categories",
        yaxis_title="Amount in USD ($)",
        legend_title="Comparison Groups",
        template="plotly_white",
        height=550,
        margin=dict(t=80, b=40)
    )

    # Render layout in dashboard
    st.plotly_chart(fig_comp, use_container_width=True)

    # 6. Structured Breakdown Grid displaying percentages for each individual item
    st.markdown("### Detailed Itemized Breakdown & Percentages")
    
    breakdown_data = []
    for cat in categories:
        item_user_val = user_values[cat]
        item_peer_val = peer_group[cat].mean()
        item_percentage = (item_user_val / user_income) * 100
        
        breakdown_data.append({
            "Category Area": cat.replace(" (USD)", ""),
            "Your Amount ($)": f"${item_user_val:,}",
            "Share of Your Income (%)": f"{item_percentage:.1f}%",
            "Peer Base Avg ($)": f"${round(item_peer_val, 2):,}"
        })
        
    st.table(pd.DataFrame(breakdown_data))
else:
    st.info("💡 Fill out the form above and click **'Analyze & Calculate Percentages'** to generate your charts and tracking reports.")
