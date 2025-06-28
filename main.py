import os
import praw
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

print("Executing Scraping...")

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_NAME"),
)

print(reddit.read_only)

for submission in reddit.subreddit("test").hot(limit=10):
    print(submission.title)

# Depression, Mental Health
# Keywords:

"""
import pandas as pd

reddit = praw.Reddit(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    username='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    user_agent='MentalHealthScraperBot/0.1'
)

subreddits = ['depression', 'mentalhealth', 'anxiety']
posts = []

for sub in subreddits:
    for post in reddit.subreddit(sub).hot(limit=500):  # or .new(limit=500)
        posts.append({
            'title': post.title,
            'text': post.selftext,

"""