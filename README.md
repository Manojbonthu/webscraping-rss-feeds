
# 🌍 Global News Scraper & Web App

This project scrapes RSS feeds from news agencies in over **20 countries** and presents them through a visual web dashboard using Flask.

---

## 📌 Features

- ✅ Fetches and parses RSS feeds using `feedparser`.
- ✅ Extracts: Title, Summary, Source, Country, Publication Date, and Link.
- ✅ Removes duplicates and handles missing values.
- ✅ Stores data in **CSV** and **SQLite** database.
- ✅ Generates 3 visualizations using `matplotlib` and `seaborn`:
  - Articles by Country
  - Top Title Keywords
  - Top News Sources
- ✅ Schedules scraping every hour using `schedule`.
- ✅ Flask web interface to:
  - View news by country or language.
  - See article count per country.
- ✅ Detects article language using `langdetect`.

---

## 📁 Project Structure

```
├── news_scraper.py        # Main scraping and visualization script
├── app.py                 # Flask web server to display news
├── combined_news_data.csv # CSV output file
├── news_data.db           # SQLite database of articles
├── Visualization/
│   ├── articles_by_country.png
│   ├── top_keywords.png
│   └── top_sources.png
└── README.md              # This file
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/news-scraper-app.git
cd news-scraper-app
```

### 2. Install Required Libraries
```bash
pip install -r requirements.txt
```

**`requirements.txt`**
```text
feedparser
pandas
matplotlib
seaborn
schedule
flask
langdetect
```

### 3. Run the Scraper
This will fetch news, generate visualizations, and save data in both CSV and SQLite.

```bash
python news_scraper.py
```

### 4. Start the Web App
```bash
python app.py
```

Then open your browser at: `http://127.0.0.1:5000/`

---

## 🌐 Web Dashboard Preview

- Homepage with country & language filters.
- Country-wise article counts in a table.
- Individual pages for news by country or language.

---

## 🧪 Advanced Features Implemented

- [✅] RSS feed scraping from 20+ countries.
- [✅] SQLite integration.
- [✅] Flask web application.
- [✅] Language detection using `langdetect`.
- [✅] Scheduling with `schedule`.

---

## ⚠️ Notes

- Encoding issues are handled using UTF-8.
- Some feeds might not support historical data (RSS feeds often show the most recent 10–50 items only).
- The scraping job is scheduled to run **every hour**. Keep the script running to enable it.

---

## 📊 Sample Summary (CSV Output)

| Country     | Source     | Title                      | Published             | Summary                  | Link                  |
|-------------|------------|----------------------------|------------------------|--------------------------|------------------------|
| UK          | BBC        | Latest UK news headline... | 2025-05-20T14:00:00Z   | Brief summary...         | https://bbc.co.uk/...  |
| India       | TOI        | Political event...         | 2025-05-20T13:30:00Z   | Brief summary...         | https://toi.in/...     |

---

## 📤 Submission Checklist

- [✅] Python files (`news_scraper.py`, `app.py`)
- [✅] Output CSV and SQLite database
- [✅] Visualizations
- [✅] README with setup & explanation
