import requests
from bs4 import BeautifulSoup
from sentiment_analysis import analyze_sentiment

def get_news(company_name):
    print(f"Fetching news for: {company_name}")  

    search_url = f"https://www.bing.com/news/search?q={company_name.replace(' ', '+')}&form=QBNH"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch news. Status code: {response.status_code}")
        return []

    print("Successfully fetched the webpage. Parsing now...")  
    soup = BeautifulSoup(response.text, "html.parser")
    
    news_data = []
    articles = soup.find_all("a", {"class": "title"})  # Updated selector for Bing News

    for idx, article in enumerate(articles[:10]):  # Limiting to 10 articles
        title = article.get_text()
        link = article["href"]

        # No direct summaries available, so we use the title for sentiment analysis
        sentiment = analyze_sentiment(title)  

        print(f"\nArticle {idx+1}: {title}")  
        print(f"Sentiment: {sentiment}")
        print(f"Link: {link}")

        news_data.append({
            "title": title,
            "link": link,
            "summary": "No summary available",
            "sentiment": sentiment
        })

    print(f"\nTotal articles fetched: {len(news_data)}")  
    return news_data

# Test the function
if __name__ == "__main__":
    company = input("Enter company name: ")
    print(f"Company entered: {company}")  
    
    news_articles = get_news(company)
    
    if not news_articles:
        print("No articles found. Try a different company name.")
    else:
        print("\nNews extraction completed successfully!")
