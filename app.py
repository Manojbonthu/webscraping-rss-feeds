
from flask import Flask, render_template_string
import sqlite3
import pandas as pd
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

app = Flask(__name__)

# Fix seed for consistent language detection
DetectorFactory.seed = 0

# Language code to name mapping
LANG_CODE_TO_NAME = {
    "af": "Afrikaans", "ca": "Catalan", "da": "Danish", "de": "German",
    "en": "English", "es": "Spanish", "et": "Estonian", "fi": "Finnish",
    "fr": "French", "id": "Indonesian", "it": "Italian", "ja": "Japanese",
    "ko": "Korean", "lv": "Latvian", "nl": "Dutch", "no": "Norwegian",
    "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", "sv": "Swedish",
    "zh-cn": "Chinese (Simplified)",
}

# Get news data from SQLite
def get_data_from_db():
    conn = sqlite3.connect("news_data.db")
    df = pd.read_sql_query("SELECT * FROM articles", conn)
    conn.close()
    return df

# Detect language from text
def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

@app.route('/')
def home():
    countries = [
        "UK", "US", "Japan", "Malaysia", "Singapore", "South Korea",
        "Middle East", "Germany", "France", "Russia", "Italy", "Spain",
        "Philippines", "Australia", "New Zealand", "Norway", "Netherlands", "India",
        "Brazil", "Argentina", "Israel", "Slovakia", "Hong Kong"
    ]

    df = get_data_from_db()
    df['Language'] = df['Title'].fillna('').apply(detect_language)

    # Country count table
    country_counts = df['Country'].str.title().value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']

    # Country buttons
    buttons_html = ''
    for c in countries:
        url_country = c.lower().replace(' ', '_')
        buttons_html += f'<button class="fancy-btn" onclick="window.location.href=\'/news/{url_country}\'">🌍 {c} News</button>\n'

    # Language buttons
    lang_buttons_html = ''
    for lang in sorted(df['Language'].dropna().unique()):
        if lang == "unknown":
            continue
        lang_code = lang.lower()
        lang_name = LANG_CODE_TO_NAME.get(lang_code, lang.upper())
        lang_buttons_html += f'<button class="small-btn" onclick="window.location.href=\'/news/language/{lang_code}\'">🌐 {lang_name} News</button>\n'

    # Country table HTML
    table_html = '<table class="country-table">'
    rows = [country_counts[i:i + 3] for i in range(0, len(country_counts), 3)]
    for row in rows:
        table_html += '<tr>'
        for _, country in row.iterrows():
            table_html += f"<td>{country['Country']}</td><td>{country['Count']}</td>"
        if len(row) < 3:
            table_html += '<td></td><td></td>' * (3 - len(row))
        table_html += '</tr>'
    table_html += '</table>'

    return render_template_string(f'''
    <html>
    <head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #121212;
            color: #eee;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 10px;
            margin: 0;
        }}
        h1 {{
            font-size: 2.5rem;
            text-shadow: 0 0 10px #00b4d8;
        }}
        p {{
            font-size: 1.2rem;
            color: #ccc;
        }}
        .btn-container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            max-width: 1200px;
            margin: 20px auto;
        }}
        .fancy-btn {{
            background: linear-gradient(135deg, #00b4d8 0%, #90e0ef 100%);
            border: none;
            border-radius: 30px;
            box-shadow: 0 4px 6px rgba(0,180,216,0.4);
            color: #121212;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            padding: 12px 28px;
            transition: transform 0.3s ease;
        }}
        .fancy-btn:hover {{
            transform: scale(1.05);
            background: linear-gradient(135deg, #90e0ef 0%, #00b4d8 100%);
        }}
        .small-btn {{
            background: #007bff;
            color: white;
            border-radius: 20px;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
        }}
        .small-btn:hover {{
            background: #0056b3;
        }}
        .country-table {{
            margin-top: 30px;
            border-collapse: collapse;
            width: 90%;
            text-align: center;
        }}
        .country-table td {{
            border: 1px solid #555;
            padding: 10px;
            background-color: #1e1e1e;
        }}
        .country-table th {{
            background-color: #007bff;
            color: white;
        }}
    </style>
    </head>
    <body>
        <h1>📰 Welcome to the News API!</h1>
        <p>Choose a button to explore news:</p>
        <button class="small-btn" onclick="window.location.href='/news'">📄 View All News</button>
        <div class="btn-container">{buttons_html}</div>
        <p>Or filter by language:</p>
        <div class="btn-container">{lang_buttons_html}</div>
        <h2>📊 Article Count by Country</h2>
        {table_html}
    </body>
    </html>
    ''')

@app.route('/news')
def get_news():
    df = get_data_from_db()
    return render_news_html(df)

@app.route('/news/<country>')
def get_news_by_country(country):
    df = get_data_from_db()
    normalized_country = country.replace('_', ' ').lower()
    filtered = df[df['Country'].str.lower() == normalized_country]
    return render_news_html(filtered)

@app.route('/news/language/<lang_code>')
def get_news_by_language(lang_code):
    df = get_data_from_db()
    df['Language'] = df['Title'].fillna('').apply(detect_language)
    filtered = df[df['Language'] == lang_code]
    return render_news_html(filtered)

def render_news_html(df):
    return render_template_string('''
    <html>
    <head>
        <title>News Articles</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #f5f8fa;
                margin: 20px;
                color: #222;
            }
            .container {
                max-width: 900px;
                margin: auto;
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
            }
            .article-card {
                background: white;
                border-radius: 12px;
                padding: 20px 25px;
                margin-bottom: 20px;
                box-shadow: 0 3px 8px rgba(0,0,0,0.1);
            }
            .title {
                font-size: 1.4em;
                color: #007BFF;
                text-decoration: none;
            }
            .meta {
                font-size: 0.95em;
                color: #666;
                margin-bottom: 12px;
            }
            .summary {
                font-size: 1em;
                line-height: 1.5;
                color: #444;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
            }
            a.button {
                background: #007BFF;
                color: white;
                padding: 12px 22px;
                border-radius: 6px;
                text-decoration: none;
                font-weight: 600;
                margin: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>News Articles</h1>
            {% if articles|length == 0 %}
                <p>No articles found.</p>
            {% else %}
                {% for article in articles %}
                <div class="article-card">
                    <a class="title" href="{{ article.Link }}" target="_blank">{{ article.Title }}</a>
<div class="meta">Source: {{ article.Source }} | Published: {{ article.Published }}</div>
<div class="summary">{{ article.Summary }}</div>

                </div>
                {% endfor %}
            {% endif %}
            <div class="footer">
                <a class="button" href="/">🏠 Home</a>
            </div>
        </div>
    </body>
    </html>
    ''', articles=df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
