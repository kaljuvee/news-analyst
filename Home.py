import streamlit as st

# Page config
st.set_page_config(
    page_title="News Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("News Analysis Dashboard")
st.markdown("""
Welcome to the News Analysis Dashboard! This application helps you analyze news articles and their potential impact on financial markets.
""")

# Create two columns for the features
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📰 News Data Collection")
    st.markdown("""
    The **News Data** page allows you to:
    - Fetch news articles from NewsData.io API
    - Filter articles by event type
    - View and analyze raw news data
    - Filter by publishers and categories
    - View data visualizations and statistics
    """)
    st.page_link("pages/02_News_Data.py", label="Go to News Data", use_container_width=True)

with col2:
    st.markdown("### 🔍 Google News")
    st.markdown("""
    The **Google News** page provides:
    - Sample news data collection
    - Interactive filtering options
    - Publisher and category analysis
    - Data visualization tools
    - Statistical insights
    """)
    st.page_link("pages/01_Google_News.py", label="Go to Google News", use_container_width=True)

# Additional information
st.markdown("---")
st.markdown("""
### Getting Started
1. Choose between **News Data** or **Google News** to start collecting news articles
2. Use the filtering options to narrow down your search
3. View the visualizations and statistics to analyze the data
4. Make sure your `.env` file contains the necessary API keys:
   - `NEWSDATAIO_API_KEY` for news data collection
""") 