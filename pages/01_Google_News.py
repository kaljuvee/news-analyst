import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import logging
from typing import Dict, Any
from GoogleNews import GoogleNews

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Publisher whitelist
PUBLISHER_WHITELIST = [
    "Reuters", "Bloomberg", "Financial Times", "Wall Street Journal",
    "CNBC", "BBC News", "The Guardian", "The Economist"
]

CATEGORIES = [
    "Economic Events", "Monetary Policy", "Market Analysis",
    "Financial Markets", "Economic Indicators"
]

EVENTS = [
    "Interest Rate Decision", "Inflation Report", "GDP Release",
    "Employment Data", "Central Bank Meeting"
]

def query_google_news(query: str, days: int = 1, count: int = 100) -> Dict[str, Any]:
    gn = GoogleNews(lang='en')
    gn.set_period(f'{days}d')
    gn.set_encode('utf-8')
    
    try:
        gn.get_news(query)
        results = gn.results(sort=True)[:count]
        return {'value': results}
    except Exception as e:
        logger.error(f"Error querying Google News: {str(e)}")
        return {'value': []}

def format_results_as_dataframe(results: Dict[str, Any], category: str, event: str) -> pd.DataFrame:
    if 'value' in results and results['value']:
        df = pd.DataFrame(results['value'])
        
        # Rename columns to match the expected schema
        column_mapping = {
            'title': 'title',
            'link': 'link',
            'desc': 'content',
            'datetime': 'published_date',
            'media': 'publisher'
        }
        df = df.rename(columns={old: new for old, new in column_mapping.items() if old in df.columns})
        
        # Ensure all required columns are present, fill with None if missing
        for col in ['title', 'link', 'content', 'published_date', 'publisher']:
            if col not in df.columns:
                df[col] = None
        
        # Add the category, event, and status columns
        df['category'] = category
        df['event'] = event
        df['status'] = 'raw'
        df['task'] = 'google_news'
        
        # Filter for whitelist publishers
        df = df[df['publisher'].isin(PUBLISHER_WHITELIST)]
        
        if df.empty:
            logger.warning(f"No results found after filtering for whitelist publishers. Category: {category}, Event: {event}")
        
        return df
    else:
        logger.warning(f"No results found from Google News. Category: {category}, Event: {event}")
        return pd.DataFrame()

def main():
    st.title("Google News API")
    st.write("Search for financial news articles using Google News API.")
    
    # Sidebar controls
    st.sidebar.header("Search Parameters")
    
    # Date range selector
    days = st.sidebar.slider("Number of days to search", 1, 7, 1)
    
    # Category multiselect
    selected_categories = st.sidebar.multiselect(
        "Select Categories",
        CATEGORIES,
        default=CATEGORIES[:2]
    )
    
    # Event multiselect
    selected_events = st.sidebar.multiselect(
        "Select Events",
        EVENTS,
        default=EVENTS[:2]
    )
    
    # Publisher multiselect
    selected_publishers = st.sidebar.multiselect(
        "Select Publishers",
        PUBLISHER_WHITELIST,
        default=PUBLISHER_WHITELIST[:3]
    )
    
    # Number of results
    num_results = st.sidebar.slider("Number of results", 5, 50, 10)
    
    # Search button
    if st.sidebar.button("Search News"):
        all_results = pd.DataFrame()
        
        # Search for each combination of category and event
        for category in selected_categories:
            for event in selected_events:
                query = f"{category} {event}"
                results = query_google_news(query, days, num_results)
                df = format_results_as_dataframe(results, category, event)
                all_results = pd.concat([all_results, df], ignore_index=True)
        
        if not all_results.empty:
            # Filter based on selected publishers
            if selected_publishers:
                all_results = all_results[all_results['publisher'].isin(selected_publishers)]
            
            # Display the dataframe
            st.dataframe(all_results)
            
            # Display some statistics
            st.subheader("Data Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Articles", len(all_results))
            with col2:
                st.metric("Unique Publishers", all_results['publisher'].nunique())
            with col3:
                st.metric("Categories Covered", all_results['category'].nunique())
            
            # Display a bar chart of publishers
            st.subheader("Articles by Publisher")
            st.bar_chart(all_results['publisher'].value_counts())
            
            # Display a pie chart of categories
            st.subheader("Articles by Category")
            st.pie_chart(all_results['category'].value_counts())
        else:
            st.warning("No results found for the selected criteria.")

if __name__ == "__main__":
    main()
