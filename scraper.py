import requests
from bs4 import BeautifulSoup

def get_news(company_name):
    print(f"Fetching news for: {company_name}")  # Debugging print statement

    search_url = f"https://news.google.com/search?q={company_name}&hl=en-US&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print(f"Requesting URL: {search_url}")  # Debugging print statement
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch news. Status code: {response.status_code}")
        return []
    
    print("Successfully fetched the webpage. Parsing now...")  # Debugging print statement
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")  # Finding all news articles
    
    news_data = []
    
    for idx, article in enumerate(articles[:10]):  # Limiting to 10 articles
        title_tag = article.find("h3")
        if title_tag:
            title = title_tag.get_text()
            link = "https://news.google.com" + title_tag.find("a")["href"][1:]  # Formatting link
            
            summary_tag = article.find("p")  # Some articles have summaries
            summary = summary_tag.get_text() if summary_tag else "No summary available."
            
            print(f"\nArticle {idx+1}: {title}")  # Debugging print statement
            print(f"Link: {link}")
            print(f"Summary: {summary}")
            
            news_data.append({"title": title, "link": link, "summary": summary})
    
    print(f"\nTotal articles fetched: {len(news_data)}")  # Debugging print statement
    return news_data

# Test the function
if __name__ == "__main__":
    company = input("Enter company name: ")
    print(f"Company entered: {company}")  # Debugging print statement
    
    news_articles = get_news(company)
    
    if not news_articles:
        print("No articles found. Try a different company name.")
    else:
        print("\nNews extraction completed successfully!")
