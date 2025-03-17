import requests
from bs4 import BeautifulSoup
from sentiment_analysis import analyze_sentiment
from comparative_analysis import comparative_sentiment_analysis
from tts_generator import generate_tts

def get_news(company_name):
    """
    Fetches news articles from Bing News related to the given company name.
    Performs sentiment analysis and generates a Hindi TTS summary.
    """
    print(f"\nFetching news for: {company_name}")

    # Bing News Search URL
    search_url = f"https://www.bing.com/news/search?q={company_name.replace(' ', '+')}&form=QBNH"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch news. Status code: {response.status_code}")
        return []

    print("Successfully fetched the webpage. Parsing now...\n")
    soup = BeautifulSoup(response.text, "html.parser")

    news_data = []
    articles = soup.find_all("a", {"class": "title"})  # Bing News headline selector

    for idx, article in enumerate(articles[:10]):  # Limit to 10 articles
        title = article.get_text()
        link = article["href"]

        # Perform sentiment analysis
        sentiment = analyze_sentiment(title)

        print(f"Article {idx+1}: {title}")
        print(f"Sentiment: {sentiment}")
        print(f"Link: {link}\n")

        news_data.append({
            "title": title,
            "link": link,
            "summary": "No summary available",
            "sentiment": sentiment
        })

    print(f"\nTotal articles fetched: {len(news_data)}")

    # Perform comparative sentiment analysis if news articles exist
    if news_data:
        print("\nComparative Sentiment Analysis:")
        analysis_result = comparative_sentiment_analysis(news_data)
        print(analysis_result)

        # Generate Hindi TTS for sentiment summary
        tts_filename = "sentiment_report.mp3"
        generate_tts(analysis_result, tts_filename)
        print(f"Sentiment report saved as: {tts_filename}")

    return news_data

# Run the script for testing
if __name__ == "__main__":
    company = input("Enter company name: ")
    print(f"\nCompany entered: {company}\n")
    
    news_articles = get_news(company)
    
    if not news_articles:
        print("No articles found. Try a different company name.")
    else:
        print("\nNews extraction and analysis completed successfully!")
