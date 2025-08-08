import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import random
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Driver Performance Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sample user database (in production, this would be a real database)
USERS = {
    "driver001": {"password": "driver123", "name": "John Smith"},
    "driver002": {"password": "sarah456", "name": "Sarah Johnson"},
    "driver003": {"password": "mike789", "name": "Mike Wilson"}
}

def verify_password(plain_password, stored_password):
    """Verify a password against stored password."""
    return plain_password == stored_password

def generate_mock_data(user_id):
    """Generate mock performance data for a driver."""
    np.random.seed(hash(user_id) % 2**32)  # Consistent data for each user
    
    # Generate data for past 3 months + current month
    current_date = datetime.now()
    start_date = current_date.replace(day=1) - timedelta(days=90)
    
    data = []
    
    # Generate daily data
    current_day = start_date
    while current_day <= current_date:
        # Simulate varying pickup counts and earnings
        base_pickups = random.randint(8, 25)
        
        # Package size distribution
        small_pickups = random.randint(0, base_pickups // 2)
        medium_pickups = random.randint(0, (base_pickups - small_pickups) // 2)
        large_pickups = max(0, base_pickups - small_pickups - medium_pickups)
        
        # Earnings per package size (in local currency)
        small_earning = random.uniform(2.5, 4.0)
        medium_earning = random.uniform(4.0, 6.5)
        large_earning = random.uniform(6.5, 10.0)
        
        total_pickups = small_pickups + medium_pickups + large_pickups
        total_earnings = (small_pickups * small_earning + 
                         medium_pickups * medium_earning + 
                         large_pickups * large_earning)
        
        data.append({
            'date': current_day,
            'total_pickups': total_pickups,
            'total_earnings': round(total_earnings, 2),
            'small_pickups': small_pickups,
            'medium_pickups': medium_pickups,
            'large_pickups': large_pickups,
            'small_earnings': round(small_pickups * small_earning, 2),
            'medium_earnings': round(medium_pickups * medium_earning, 2),
            'large_earnings': round(large_pickups * large_earning, 2)
        })
        
        current_day += timedelta(days=1)
    
    return pd.DataFrame(data)

def get_monthly_summary(df):
    """Get monthly summary of pickups and earnings."""
    df['year_month'] = df['date'].dt.to_period('M')
    monthly_summary = df.groupby('year_month').agg({
        'total_pickups': 'sum',
        'total_earnings': 'sum'
    }).reset_index()
    monthly_summary['month_name'] = monthly_summary['year_month'].dt.strftime('%B %Y')
    return monthly_summary

def login_page():
    """Display login page."""
    st.title("🚚 Driver Performance Dashboard")
    st.markdown("### Please login to access your performance data")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("#### Login Credentials")
            user_id = st.text_input("User ID", placeholder="Enter your user ID")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
            
            if submit_button:
                if user_id in USERS and verify_password(password, USERS[user_id]["password"]):
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.user_name = USERS[user_id]["name"]
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid user ID or password!")
        
        # Demo credentials info
        with st.expander("Demo Credentials"):
            st.info("""
            **Demo Login Credentials:**
            - User ID: driver001, Password: driver123
            - User ID: driver002, Password: sarah456  
            - User ID: driver003, Password: mike789
            """)

def dashboard_page():
    """Display main dashboard."""
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"Welcome back, {st.session_state.user_name}! 👋")
    with col2:
        if st.button("Logout", type="secondary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Load data
    df = generate_mock_data(st.session_state.user_id)
    
    # Past 3 months summary
    st.markdown("## 📊 Past 3 Months Performance")
    monthly_summary = get_monthly_summary(df)
    
    # Display past 3 months (excluding current month)
    current_month = datetime.now().replace(day=1)
    past_months = monthly_summary[monthly_summary['year_month'] < pd.Period(current_month, 'M')].tail(3)
    
    if not past_months.empty:
        col1, col2, col3 = st.columns(3)
        for idx, (_, month_data) in enumerate(past_months.iterrows()):
            with [col1, col2, col3][idx % 3]:
                st.metric(
                    label=month_data['month_name'],
                    value=f"{month_data['total_pickups']} pickups",
                    delta=f"${month_data['total_earnings']:.2f} earned"
                )
    
    # Current month detailed view
    st.markdown("## 🎯 Current Month Performance")
    
    # Filter current month data
    current_month_data = df[df['date'].dt.month == datetime.now().month]
    
    # Date range selector for current month
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now().replace(day=1).date(),
            min_value=datetime.now().replace(day=1).date(),
            max_value=datetime.now().date()
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now().date(),
            min_value=datetime.now().replace(day=1).date(),
            max_value=datetime.now().date()
        )
    
    # Filter data by selected date range
    filtered_data = current_month_data[
        (current_month_data['date'].dt.date >= start_date) &
        (current_month_data['date'].dt.date <= end_date)
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected date range.")
        return
    
    # Current month metrics
    total_pickups = filtered_data['total_pickups'].sum()
    total_earnings = filtered_data['total_earnings'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pickups", total_pickups)
    with col2:
        st.metric("Total Earnings", f"${total_earnings:.2f}")
    with col3:
        avg_daily_pickups = total_pickups / len(filtered_data) if len(filtered_data) > 0 else 0
        st.metric("Avg Daily Pickups", f"{avg_daily_pickups:.1f}")
    with col4:
        avg_earning_per_pickup = total_earnings / total_pickups if total_pickups > 0 else 0
        st.metric("Avg per Pickup", f"${avg_earning_per_pickup:.2f}")
    
    # Pickup breakdown by size
    st.markdown("### 📦 Pickup Breakdown by Package Size")
    
    size_summary = {
        'Small': {
            'pickups': filtered_data['small_pickups'].sum(),
            'earnings': filtered_data['small_earnings'].sum()
        },
        'Medium': {
            'pickups': filtered_data['medium_pickups'].sum(),
            'earnings': filtered_data['medium_earnings'].sum()
        },
        'Large': {
            'pickups': filtered_data['large_pickups'].sum(),
            'earnings': filtered_data['large_earnings'].sum()
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pickups by size pie chart
        pickup_values = [size_summary[size]['pickups'] for size in size_summary.keys()]
        fig_pickups = px.pie(
            values=pickup_values,
            names=list(size_summary.keys()),
            title="Pickups Distribution by Size",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        st.plotly_chart(fig_pickups, use_container_width=True)
    
    with col2:
        # Earnings by size pie chart
        earnings_values = [size_summary[size]['earnings'] for size in size_summary.keys()]
        fig_earnings = px.pie(
            values=earnings_values,
            names=list(size_summary.keys()),
            title="Earnings Distribution by Size",
            color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1']
        )
        st.plotly_chart(fig_earnings, use_container_width=True)
    
    # Detailed breakdown table
    col1, col2, col3 = st.columns(3)
    for idx, (size, data) in enumerate(size_summary.items()):
        with [col1, col2, col3][idx]:
            st.info(f"""
            **{size} Packages**
            - Pickups: {data['pickups']}
            - Earnings: ${data['earnings']:.2f}
            - Avg per pickup: ${data['earnings']/data['pickups']:.2f if data['pickups'] > 0 else 0}
            """)
    
    # Daily performance chart
    st.markdown("### 📈 Daily Performance Trend")
    
    fig_daily = go.Figure()
    
    # Add pickups line
    fig_daily.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['total_pickups'],
        mode='lines+markers',
        name='Daily Pickups',
        line=dict(color='#45B7D1', width=3),
        yaxis='y'
    ))
    
    # Add earnings line on secondary y-axis
    fig_daily.add_trace(go.Scatter(
        x=filtered_data['date'],
        y=filtered_data['total_earnings'],
        mode='lines+markers',
        name='Daily Earnings ($)',
        line=dict(color='#FF6B6B', width=3),
        yaxis='y2'
    ))
    
    fig_daily.update_layout(
        title='Daily Pickups and Earnings Trend',
        xaxis_title='Date',
        yaxis=dict(title='Number of Pickups', side='left'),
        yaxis2=dict(title='Earnings ($)', side='right', overlaying='y'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig_daily, use_container_width=True)

def main():
    """Main application function."""
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if st.session_state.logged_in:
        dashboard_page()
    else:
        login_page()

if __name__ == "__main__":

    main() 
