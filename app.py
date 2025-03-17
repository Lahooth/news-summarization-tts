import streamlit as st
from scraper import get_news
import os

st.title("📰 News Sentiment Analyzer")
st.write("Enter a company name to fetch recent news articles and analyze sentiment.")

# User input for company name
company_name = st.text_input("Enter Company Name", "")

if st.button("Analyze News"):
    if company_name:
        st.write(f"Fetching news for **{company_name}**...")
        news_articles = get_news(company_name)
        
        if not news_articles:
            st.error("No articles found. Try a different company name.")
        else:
            st.success("News analysis completed!")
            
            # Display news articles
            for idx, article in enumerate(news_articles, start=1):
                st.subheader(f"📰 Article {idx}")
                st.write(f"**Title:** {article['title']}")
                st.write(f"**Sentiment:** {article['sentiment']}")
                st.write(f"[Read more]({article['link']})")
                st.write("---")
            
            # Play the generated Hindi TTS file
            tts_filename = "sentiment_report.mp3"
            if os.path.exists(tts_filename):
                st.audio(tts_filename, format="audio/mp3")
    else:
        st.warning("Please enter a company name.")
