import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Sample data for demonstration
SAMPLE_PUBLISHERS = [
    "Reuters", "Bloomberg", "Financial Times", "Wall Street Journal",
    "CNBC", "BBC News", "The Guardian", "The Economist"
]

SAMPLE_CATEGORIES = [
    "Economic Events", "Monetary Policy", "Market Analysis",
    "Financial Markets", "Economic Indicators"
]

SAMPLE_EVENTS = [
    "Interest Rate Decision", "Inflation Report", "GDP Release",
    "Employment Data", "Central Bank Meeting"
]

def generate_sample_news_data(num_items: int = 10) -> pd.DataFrame:
    """Generate sample news data for demonstration purposes."""
    data = []
    
    for _ in range(num_items):
        # Generate random dates within the last 7 days
        days_ago = random.randint(0, 7)
        date = datetime.now() - timedelta(days=days_ago)
        
        # Generate sample news item
        news_item = {
            'title': f"Sample News Title {random.randint(1, 1000)}",
            'link': f"https://example.com/news/{random.randint(1000, 9999)}",
            'content': f"This is a sample news content about {random.choice(['economy', 'markets', 'policy'])}. "
                      f"Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            'published_date': date.strftime("%Y-%m-%d %H:%M:%S"),
            'publisher': random.choice(SAMPLE_PUBLISHERS),
            'category': random.choice(SAMPLE_CATEGORIES),
            'event': random.choice(SAMPLE_EVENTS),
            'status': 'raw',
            'task': 'google_news'
        }
        data.append(news_item)
    
    return pd.DataFrame(data)

def main():
    st.title("Google News API Demo")
    st.write("This is a demonstration of how the Google News API data would be displayed.")
    
    # Sidebar controls
    st.sidebar.header("Search Parameters")
    
    # Date range selector
    days = st.sidebar.slider("Number of days to search", 1, 7, 1)
    
    # Category multiselect
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        SAMPLE_CATEGORIES,
        default=SAMPLE_CATEGORIES[:2]
    )
    
    # Event multiselect
    selected_events = st.sidebar.multiselect(
        "Select Events",
        SAMPLE_EVENTS,
        default=SAMPLE_EVENTS[:2]
    )
    
    # Publisher multiselect
    selected_publishers = st.sidebar.multiselect(
        "Select Publishers",
        SAMPLE_PUBLISHERS,
        default=SAMPLE_PUBLISHERS[:3]
    )
    
    # Number of results
    num_results = st.sidebar.slider("Number of results", 5, 50, 10)
    
    # Generate and display sample data
    if st.sidebar.button("Generate Sample Data"):
        df = generate_sample_news_data(num_results)
        
        # Filter based on selections
        if selected_categories:
            df = df[df['category'].isin(selected_categories)]
        if selected_events:
            df = df[df['event'].isin(selected_events)]
        if selected_publishers:
            df = df[df['publisher'].isin(selected_publishers)]
        
        # Display the dataframe
        st.dataframe(df)
        
        # Display some statistics
        st.subheader("Data Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Articles", len(df))
        with col2:
            st.metric("Unique Publishers", df['publisher'].nunique())
        with col3:
            st.metric("Categories Covered", df['category'].nunique())
        
        # Display a bar chart of publishers
        st.subheader("Articles by Publisher")
        st.bar_chart(df['publisher'].value_counts())
        
        # Display a pie chart of categories
        st.subheader("Articles by Category")
        st.pie_chart(df['category'].value_counts())

if __name__ == "__main__":
    main()
