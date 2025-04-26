import os
import uuid
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import praw
from textblob import TextBlob
import cloudinary.uploader

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')


reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return 'positive'
    elif polarity < -0.1:
        return 'negative'
    else:
        return 'neutral'

def fetch_reddit_data(product, year):
    posts = []
    current_year = datetime.datetime.now().year
    if int(year) > current_year:
        raise ValueError("Year cannot be in the future.")

    for submission in reddit.subreddit("all").search(product, limit=200):
        created_year = datetime.datetime.fromtimestamp(submission.created_utc).year
        if created_year == int(year):
            posts.append({
                "title": submission.title,
                "created": datetime.datetime.fromtimestamp(submission.created_utc),
                "text": submission.selftext
            })

    df = pd.DataFrame(posts)
    if df.empty:
        return df

    df["content"] = df["title"] + " " + df["text"]
    df["sentiment"] = df["content"].apply(analyze_sentiment)
    df["month"] = df["created"].dt.strftime('%B')

    return df

def generate_graph(data, product, year, option):
    plt.figure(figsize=(10, 6))

    if option == "1":
        sentiment_counts = data["sentiment"].value_counts()
        sentiment_counts.plot(kind="pie", autopct="%1.1f%%", colors=["green", "red", "gray"])
        plt.title(f"Sentiment Distribution for '{product}' in {year}")
    elif option == "2":
        monthly = data.groupby("month")["sentiment"].value_counts().unstack().fillna(0)
        monthly = monthly.reindex([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
        monthly.plot(kind="bar", stacked=True)
        plt.title(f"Monthly Sentiment Trend for '{product}' in {year}")
    elif option == "3":
        count = data.groupby("month").size()
        count = count.reindex([
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
        count.plot(kind="line", marker="o")
        plt.title(f"Mentions Per Month for '{product}' in {year}")
    elif option == "4":
        best_month = data[data["sentiment"] == "positive"]["month"].value_counts().idxmax()
        plt.text(0.1, 0.5, f"Best Performing Month: {best_month}", fontsize=15)
        plt.axis('off')
    elif option == "5":
        worst_month = data[data["sentiment"] == "negative"]["month"].value_counts().idxmax()
        plt.text(0.1, 0.5, f"Worst Performing Month: {worst_month}", fontsize=15)
        plt.axis('off')

    plt.tight_layout()
    tmp_file = f"/tmp/{uuid.uuid4().hex}.png"
    plt.savefig(tmp_file)
    plt.clf()

    upload_result = cloudinary.uploader.upload(tmp_file)
    return upload_result['secure_url']
  
def fetch_and_analyze_data(product, year, option):
    df = fetch_reddit_data(product, year)
    if df.empty:
        raise ValueError("No data found for the given product and year.")

    image_url = generate_graph(df, product, year, option)
    return f"Analysis complete for {product} in {year}.", image_url

