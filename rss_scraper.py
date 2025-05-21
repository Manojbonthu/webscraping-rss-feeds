import feedparser
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import time
import schedule
import sqlite3
import os
from datetime import datetime

# ---------- RSS Feed Dictionary ----------
rss_feeds = {
    "India - TOI - Top Stories": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "India - TOI - Politics": "https://timesofindia.indiatimes.com/rssfeeds/1221656.cms",
    "India - TOI - Business": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
    "India - TOI - Sports": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms",
    "India - TOI - Entertainment": "https://timesofindia.indiatimes.com/rssfeeds/1081479906.cms",


    
    # 🇬🇧 UK - BBC
    "UK - BBC - Top Stories": "http://feeds.bbci.co.uk/news/rss.xml",
    "UK - BBC - World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "UK - BBC - Business": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "UK - BBC - Technology": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "UK - BBC - Health": "http://feeds.bbci.co.uk/news/health/rss.xml",
    "UK - BBC - Science & Environment": "http://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "UK - BBC - UK": "http://feeds.bbci.co.uk/news/uk/rss.xml",
    "UK - BBC - Politics": "http://feeds.bbci.co.uk/news/politics/rss.xml",
    "UK - BBC - Education": "http://feeds.bbci.co.uk/news/education/rss.xml",
    "UK - BBC - Sports": "http://feeds.bbci.co.uk/sport/rss.xml",

    # 🇺🇸 US - CNN
    "US - CNN - Top": "http://rss.cnn.com/rss/edition.rss",
    "US - CNN - World": "http://rss.cnn.com/rss/edition_world.rss",
    "US - CNN - Business": "http://rss.cnn.com/rss/money_latest.rss",
    "US - CNN - Technology": "http://rss.cnn.com/rss/edition_technology.rss",
    "US - CNN - Sports": "http://rss.cnn.com/rss/edition_sport.rss",
    "US - CNN - US News": "http://rss.cnn.com/rss/cnn_us.rss",
    "US - CNN - Health": "http://rss.cnn.com/rss/cnn_health.rss",
    "US - CNN - Travel": "http://rss.cnn.com/rss/cnn_travel.rss",

    # 🇯🇵 Japan - NHK
    "Japan - NHK - General": "https://www3.nhk.or.jp/rss/news/cat0.xml",
    "Japan - NHK - Domestic": "https://www3.nhk.or.jp/rss/news/cat1.xml",
    "Japan - NHK - Politics": "https://www3.nhk.or.jp/rss/news/cat4.xml",
    "Japan - NHK - International": "https://www3.nhk.or.jp/rss/news/cat5.xml",
    "Japan - NHK - Economy": "https://www3.nhk.or.jp/rss/news/cat2.xml",
    "Japan - NHK - Science & Culture": "https://www3.nhk.or.jp/rss/news/cat6.xml",
    "Japan - NHK - Society": "https://www3.nhk.or.jp/rss/news/cat3.xml",

    # 🇲🇾 Malaysia - The Star
    "Malaysia - The Star - Business": "https://www.thestar.com.my/rss/business",
    "Malaysia - The Star - Sports": "https://www.thestar.com.my/rss/sport",

    # 🇸🇬 Singapore - CNA
    "Singapore - CNA - Top Stories": "https://www.channelnewsasia.com/rssfeeds/8395986",

    # 🇰🇷 South Korea - Korea Times
    "South Korea - Korea Times - National": "https://www.koreatimes.co.kr/www/rss/nation.xml",
    "South Korea - Korea Times - Business": "https://www.koreatimes.co.kr/www/rss/biz.xml",
    "South Korea - Korea Times - Sports": "https://www.koreatimes.co.kr/www/rss/sports.xml",

    # 🌍 Other Countries
    "Middle East - Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "Germany - DW - All": "https://rss.dw.com/rdf/rss-en-all",
    "France - France24 - All": "https://www.france24.com/en/rss",
    "Russia - RT - News": "https://www.rt.com/rss/news/",
   
    "Italy - ANSA": "https://www.ansa.it/sito/ansait_rss.xml",
    "Spain - El Pais": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
  
    "Philippines - Philstar - Headlines": "https://www.philstar.com/rss/headlines",

    # New additions
    "Australia - ABC - Top Stories": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "New Zealand - RNZ - National": "https://www.rnz.co.nz/rss/national.xml",
    "New Zealand - RNZ - International": "https://www.rnz.co.nz/rss/international.xml",
    "Norway - NRK - Top Stories": "https://www.nrk.no/toppsaker.rss",
    "Netherlands - DutchNews": "https://www.dutchnews.nl/feed/",
# 🇧🇷 Brazil - Globo
"Brazil - Globo - Top Stories": "https://g1.globo.com/rss/g1/",

# 🇦🇷 Argentina - Clarin
"Argentina - Clarin - Top Stories": "https://www.clarin.com/rss/lo-ultimo/",

# 🇵🇭 Philippines - Inquirer
"Philippines - Inquirer - Top Stories": "https://newsinfo.inquirer.net/feed",

# 🇮🇱 Israel - The Times of Israel
"Israel - Times of Israel - Top Stories": "https://www.timesofisrael.com/feed/",

# 🇸🇰 Slovakia - The Slovak Spectator
"Slovakia - The Slovak Spectator - News": "https://spectator.sme.sk/rss",

# 🇭🇰 Hong Kong - South China Morning Post
"Hong Kong - SCMP - Top Stories": "https://www.scmp.com/rss/91/feed"
}

# ---------- Fetch News Function ----------
def fetch_news(rss_sources):
    all_news = []
    for label, url in rss_sources.items():
        try:
            start_time = time.time()
            feed = feedparser.parse(url)
            articles_fetched = 0

            if not hasattr(feed, 'entries'):
                print(f"⚠️ No entries found for {label}")
                continue

            for entry in feed.entries:
                summary = entry.get("summary", "").strip()
                if not summary:
                    continue

                parts = label.split(" - ")
                country = parts[0]
                source = parts[1] if len(parts) > 1 else "Unknown"

                news = {
                    "Country": country,
                    "Source": source,
                    "Title": entry.get("title", "N/A"),
                    "Published": entry.get("published", "N/A"),
                    "Summary": summary,
                    "Link": entry.get("link", "N/A")
                }
                all_news.append(news)
                articles_fetched += 1

            end_time = time.time()
            print(f"✅ Fetched {articles_fetched} articles from: {label} in {end_time - start_time:.2f} sec")

        except Exception as e:
            print(f"⚠️ Failed to fetch from {label}: {e}")
    return all_news

# ---------- Main Job Function ----------
def run_feed_collection():
    print(f"\n⏳ Running RSS feed job at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    rss_news = fetch_news(rss_feeds)
    df = pd.DataFrame(rss_news).drop_duplicates(subset=["Title", "Link"]).copy()

    if df.empty:
        print("⚠️ No data fetched. Skipping saving and analysis.")
        return

    # ---------- Save CSV ----------
    df.to_csv("combined_news_data.csv", index=False, encoding="utf-8")
    print(f"📁 File saved as 'combined_news_data.csv' with {len(df)} articles.")

    # ---------- Save to SQLite ----------
    conn = sqlite3.connect("news_data.db")
    df.to_sql("articles", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Data saved to SQLite as 'news_data.db'")

    # ---------- Visualization: Articles by Country ----------
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, y='Country', order=df['Country'].value_counts().index)
    plt.title("Number of Articles by Country")
    plt.xlabel("Article Count")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.savefig("Visualization/articles_by_country.png")
    plt.close()

    # ---------- Visualization: Top 10 Title Keywords ----------
    all_words = " ".join(df['Title'].dropna()).lower().split()
    common_words = [word for word in all_words if word.isalpha() and len(word) > 3]
    word_freq = Counter(common_words).most_common(10)

    if word_freq:
        words, counts = zip(*word_freq)
        plt.figure(figsize=(10, 5))
        sns.barplot(x=list(counts), y=list(words))
        plt.title("Top 10 Frequent Words in News Titles")
        plt.xlabel("Frequency")
        plt.ylabel("Keyword")
        plt.tight_layout()
        plt.savefig("Visualization/top_keywords.png")
        plt.close()
    else:
        print("⚠️ No frequent words found to plot.")

    # ---------- Visualization: Top 5 Sources ----------
    plt.figure(figsize=(10, 5))
    top_sources = df['Source'].value_counts().head(5)
    sns.barplot(x=top_sources.index, y=top_sources.values)
    plt.title("Top 5 News Sources by Article Count")
    plt.ylabel("Article Count")
    plt.xlabel("Source")
    plt.tight_layout()
    plt.savefig("Visualization/top_sources.png")
    plt.close()

    print("📊 Visualizations saved: articles_by_country.png, top_keywords.png, top_sources.png")
    print("✅ Job complete.\n")

# ---------- Schedule Job ----------
# Run immediately once
run_feed_collection()

# Schedule to run every 1 hour
schedule.every(1).hours.do(run_feed_collection)

# ---------- Keep Running ----------
print("⏲️ Scheduler started. Press Ctrl+C to stop.\n")
while True:
    schedule.run_pending()
    time.sleep(60)