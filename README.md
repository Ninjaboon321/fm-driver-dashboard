# 🚚 Driver Performance Dashboard

A comprehensive Streamlit web application designed for pickup drivers in courier services to track their performance, earnings, and productivity metrics.

## ✨ Features

### 🔐 Authentication System
- Secure login with user ID and password
- Password encryption using bcrypt
- Session management with Streamlit

### 📊 Performance Dashboard
- **Past 3 Months Overview**: Monthly summary of total pickups and earnings
- **Current Month Details**: Comprehensive breakdown of current month performance
- **Date Range Filtering**: Select custom date ranges within the current month
- **Package Size Analytics**: Detailed breakdown by Small, Medium, and Large packages

### 📈 Data Visualizations
- Interactive pie charts showing pickup and earnings distribution by package size
- Daily performance trend charts with dual y-axis for pickups and earnings
- Responsive metrics cards with key performance indicators

### 🎯 Key Metrics Tracked
- Total pickups and earnings
- Average daily pickups
- Average earnings per pickup
- Package size distribution
- Daily performance trends

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the app:**
   - Open your web browser
   - Navigate to `http://localhost:8501`

## 👥 Demo Credentials

The app comes with pre-configured demo accounts for testing:

| User ID | Password | Driver Name |
|---------|----------|-------------|
| driver001 | driver123 | John Smith |
| driver002 | sarah456 | Sarah Johnson |
| driver003 | mike789 | Mike Wilson |

## 📱 How to Use

1. **Login**: Enter your user ID and password on the login page
2. **View Past Performance**: Check the past 3 months summary at the top
3. **Analyze Current Month**: 
   - View overall metrics for the current month
   - Use date range selectors to filter specific periods
   - Examine package size breakdowns with interactive charts
4. **Track Trends**: Review daily performance charts to identify patterns
5. **Logout**: Use the logout button to securely end your session

## 🛠 Technical Details

### Built With
- **Streamlit**: Web framework for the user interface
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualizations
- **bcrypt**: Password hashing and security
- **NumPy**: Numerical computations

### Data Structure
The app generates realistic mock data including:
- Daily pickup counts by package size (Small, Medium, Large)
- Earnings calculations based on package size rates
- Historical data for past 3 months plus current month
- Consistent data generation per user for realistic testing

## 🌐 Deployment Options

### Free Deployment on Streamlit Cloud

1. **Fork/Upload to GitHub**: Put your code in a GitHub repository

2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Deploy with one click

3. **Alternative Free Options**:
   - **Railway**: Connect GitHub repo and deploy
   - **Render**: Free tier with automatic deploys
   - **Heroku**: Free dyno hours (limited)

### Local Network Deployment
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

## 🔧 Customization

### Adding New Users
Edit the `USERS` dictionary in `app.py`:
```python
USERS = {
    "your_user_id": {
        "password": "hashed_password_here", 
        "name": "Display Name"
    }
}
```

### Modifying Earnings Rates
Adjust the earning ranges in the `generate_mock_data()` function:
```python
small_earning = random.uniform(2.5, 4.0)    # Small package rate
medium_earning = random.uniform(4.0, 6.5)   # Medium package rate  
large_earning = random.uniform(6.5, 10.0)   # Large package rate
```

### Database Integration
For production use, replace the mock data generation with actual database connections:
- PostgreSQL, MySQL, or MongoDB for data storage
- SQLAlchemy or pymongo for database interactions
- Environment variables for database credentials

## 📊 Sample Data Overview

The app generates realistic sample data including:
- **Daily Pickups**: 8-25 packages per day with size variations
- **Package Distribution**: Random but realistic small/medium/large ratios
- **Earnings**: Variable rates based on package size
- **Time Range**: Past 3 months + current month data

## 🔒 Security Features

- Password hashing with bcrypt
- Session-based authentication
- Input validation and sanitization
- Secure logout functionality

## 🆘 Troubleshooting

**Common Issues:**

1. **Import Errors**: Ensure all packages are installed via `pip install -r requirements.txt`
2. **Port Conflicts**: If port 8501 is busy, Streamlit will automatically use the next available port
3. **Data Not Loading**: Check console for any error messages related to data generation

**Performance Tips:**
- Use date range filters for large datasets
- Clear browser cache if experiencing loading issues
- Restart the app if session state becomes corrupted

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Streamlit documentation at [docs.streamlit.io](https://docs.streamlit.io)
3. Verify all dependencies are correctly installed

---

**Ready to track your driver performance? Run the app and start monitoring your pickup efficiency today!** 🚀 