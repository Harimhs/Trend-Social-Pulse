import praw
import matplotlib.pyplot as plt
from datetime import datetime
from textblob import TextBlob
from collections import defaultdict, Counter
import time

# --- CONFIGURATION ---
REDDIT_CLIENT_ID = "wUR7wpsl8jo4BoV8p--oUA"
REDDIT_SECRET = "HJskPfNVyjW7kZqCTo_cWlwUEYOVLQ"
REDDIT_USER_AGENT = "TrendPulseExplorer/0.1 by RedditUser"

# --- SETUP REDDIT API ---
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def fetch_reddit_data(keyword, year):
    print("\nFetching Reddit data... Please wait.")
    posts = []
    for submission in reddit.subreddit("all").search(keyword, limit=1000):
        try:
            post_year = datetime.utcfromtimestamp(submission.created_utc).year
            if post_year == year:
                posts.append({
                    "title": submission.title,
                    "created_utc": submission.created_utc
                })
        except Exception:
            continue
    return posts

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def plot_overall_sentiment(posts):
    sentiments = [analyze_sentiment(post['title']) for post in posts]
    positive = len([s for s in sentiments if s > 0.1])
    negative = len([s for s in sentiments if s < -0.1])
    neutral = len([s for s in sentiments if -0.1 <= s <= 0.1])

    plt.figure(figsize=(6, 6))
    plt.pie([positive, negative, neutral], labels=['Positive', 'Negative', 'Neutral'], autopct='%1.1f%%')
    plt.title("Overall Sentiment Distribution")
    plt.show()

def plot_monthly_sentiment(posts):
    monthly_scores = defaultdict(list)
    for post in posts:
        month = datetime.utcfromtimestamp(post['created_utc']).strftime('%B')
        score = analyze_sentiment(post['title'])
        monthly_scores[month].append(score)

    months_ordered = [datetime.strptime(m, "%B") for m in monthly_scores.keys()]
    sorted_months = sorted(months_ordered)
    labels = [m.strftime("%B") for m in sorted_months]
    values = [sum(monthly_scores[m.strftime("%B")])/len(monthly_scores[m.strftime("%B")]) for m in sorted_months]

    plt.figure(figsize=(10, 5))
    plt.plot(labels, values, marker='o')
    plt.title("Monthly Sentiment Trend")
    plt.xlabel("Month")
    plt.ylabel("Average Sentiment Score")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_monthly_mentions(posts):
    mentions = Counter()
    for post in posts:
        month = datetime.utcfromtimestamp(post['created_utc']).strftime('%B')
        mentions[month] += 1

    months_ordered = [datetime.strptime(m, "%B") for m in mentions.keys()]
    sorted_months = sorted(months_ordered)
    labels = [m.strftime("%B") for m in sorted_months]
    values = [mentions[m.strftime("%B")] for m in sorted_months]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='skyblue')
    plt.title("Monthly Product Mentions")
    plt.xlabel("Month")
    plt.ylabel("Number of Mentions")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def best_worst_period(posts):
    month_sentiments = defaultdict(list)
    for post in posts:
        month = datetime.utcfromtimestamp(post['created_utc']).strftime('%B')
        sentiment = analyze_sentiment(post['title'])
        month_sentiments[month].append(sentiment)

    avg_sentiment = {month: sum(scores)/len(scores) for month, scores in month_sentiments.items() if scores}

    if not avg_sentiment:
        print("No sentiment data available to determine best/worst period.")
        return

    best_month = max(avg_sentiment, key=avg_sentiment.get)
    worst_month = min(avg_sentiment, key=avg_sentiment.get)

    print(f"\nBest Performing Period: {best_month} with positive buzz")
    print(f"Worst Performing Period: {worst_month} with negative buzz")

    plt.figure(figsize=(8, 4))
    plt.bar(avg_sentiment.keys(), avg_sentiment.values(), color='lightgreen')
    plt.title("Average Sentiment by Month")
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel("Month")
    plt.ylabel("Average Sentiment")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# --- MAIN CONSOLE ---
def main():
    print("Welcome to Trend Pulse Explorer")
    keyword = input("Enter the product keyword to analyze: ")
    try:
        year = int(input("Enter the year (e.g., 2023): "))
    except ValueError:
        print("Invalid year. Please enter a valid number.")
        return

    posts = fetch_reddit_data(keyword, year)
    if not posts:
        print("No data found for the given product and year.")
        return

    while True:
        print("\nOptions:")
        print("1. Overall Sentiment Distribution")
        print("2. Monthly Sentiment Trend (Improved Visualization)")
        print("3. Monthly Peak Product Mentions")
        print("4. Best Performing Period (Positive Sentiment)")
        print("5. Worst Performing Period (Negative Sentiment)")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            plot_overall_sentiment(posts)
        elif choice == '2':
            plot_monthly_sentiment(posts)
        elif choice == '3':
            plot_monthly_mentions(posts)
        elif choice == '4':
            best_worst_period(posts)
        elif choice == '5':
            best_worst_period(posts)
        elif choice == '6':
            print("Exiting... Thank you for using Trend Pulse Explorer!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
