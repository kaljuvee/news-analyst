import streamlit as st
import requests
from urllib.parse import urlencode
import pandas as pd
from typing import Dict, Any
from dotenv import load_dotenv
import os
import logging

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

# Page config
st.set_page_config(
    page_title="News Data Analysis",
    page_icon="📰",
    layout="wide"
)

# Title and description
st.title("News Data Analysis")
st.markdown("""
This page allows you to fetch and analyze news data from NewsData.io API. 
You can select an event type and fetch relevant news articles.
""")

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

api_key = os.getenv('NEWSDATAIO_API_KEY')

def query_newsdata_io(api_key: str, event: str) -> Dict[str, Any]:
    base_url = "https://newsdata.io/api/1/news"
    
    params = {
        "apikey": api_key,
        "q": event,
        "domain": ",".join(SAMPLE_PUBLISHERS),
        "language": "en",
    }
    
    # URL encode the parameters
    encoded_params = urlencode(params)
    
    # Construct the full URL
    full_url = f"{base_url}?{encoded_params}"
    
    # Make the GET request
    response = requests.get(full_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Error: {response.status_code}", 'message': response.text}

def format_results_as_dataframe(results: Dict[str, Any], category: str, event: str) -> pd.DataFrame:
    if 'results' in results and results['results']:
        df = pd.DataFrame(results['results'])
        # Select only the most relevant columns
        columns_to_keep = ['title', 'link', 'description', 'pubDate', 'source_id']
        df = df[columns_to_keep]
        
        # Rename columns to match the database schema
        column_mapping = {
            'description': 'content',
            'pubDate': 'published_date',
            'source_id': 'publisher'
        }
        df = df.rename(columns=column_mapping)
        
        # Add the category, event, and status columns
        df['category'] = category
        df['event'] = event
        df['status'] = 'raw'
        df['task'] = 'newsdata_io'
        
        return df
    else:
        return pd.DataFrame({'error': [results.get('error', 'Unknown error')], 'message': [results.get('message', 'No message')], 'category': [category], 'event': [event], 'status': ['raw']})

# Main content
if api_key:
    # Sidebar controls
    st.sidebar.header("Search Parameters")
    
    # Event selection
    event_type = st.sidebar.selectbox(
        "Select Event Type",
        options=SAMPLE_EVENTS
    )
    
    # Category selection
    category = st.sidebar.selectbox(
        "Select Category",
        options=SAMPLE_CATEGORIES
    )
    
    # Publisher multiselect
    selected_publishers = st.sidebar.multiselect(
        "Select Publishers",
        SAMPLE_PUBLISHERS,
        default=SAMPLE_PUBLISHERS[:3]
    )

    if st.sidebar.button("Fetch News Data"):
        with st.spinner("Fetching news data..."):
            # Query the API
            results = query_newsdata_io(api_key, event_type)
            
            # Format results
            df = format_results_as_dataframe(results, category, event_type)
            
            if 'error' not in df.columns:
                # Filter by selected publishers if any are selected
                if selected_publishers:
                    df = df[df['publisher'].isin(selected_publishers)]
                
                # Display results
                st.success(f"Found {len(df)} articles")
                st.dataframe(df)
                
                # Display statistics
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
            else:
                st.error(f"Error: {df['error'].iloc[0]}")
                st.error(f"Message: {df['message'].iloc[0]}")
else:
    st.error("NEWSDATAIO_API_KEY not found in environment variables. Please add it to your .env file.")
