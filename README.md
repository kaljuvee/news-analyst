# News Analysis Dashboard

A Streamlit application for analyzing news articles and their potential impact on financial markets. The dashboard provides tools for collecting, filtering, and visualizing news data from multiple sources.

## Features

### 📰 News Data Collection
- Fetch news articles from NewsData.io API
- Filter articles by event type
- View and analyze raw news data
- Filter by publishers and categories
- View data visualizations and statistics

### 🔍 Google News
- Sample news data collection
- Interactive filtering options
- Publisher and category analysis
- Data visualization tools
- Statistical insights

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/news-analyst.git
cd news-analyst
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your API keys:
```env
NEWSDATAIO_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run Home.py
```

2. Navigate through the dashboard:
   - Use the News Data page to fetch and analyze real news articles
   - Use the Google News page to explore sample data and visualizations

3. Use the filtering options to narrow down your search:
   - Select event types
   - Choose categories
   - Filter by publishers
   - Adjust date ranges

4. View the visualizations and statistics to analyze the data:
   - Article counts by publisher
   - Category distribution
   - Time-based trends

## Project Structure

```
news-analyst/
├── Home.py                 # Main dashboard entry point
├── pages/
│   ├── 01_Google_News.py   # Google News sample data page
│   └── 02_News_Data.py     # NewsData.io integration page
├── utils/                  # Utility functions and helpers
├── .env                    # Environment variables (not tracked)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Requirements

- Python 3.8 or higher
- Streamlit
- Pandas
- Requests
- Python-dotenv

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NewsData.io for providing the news API
- Streamlit for the web application framework
- All contributors who have helped with the project