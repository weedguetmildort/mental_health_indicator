import os
import json
import praw
import textwrap
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

max_line_length = 60 # Desired maximum line length for the string content

print("Executing Scraping...")

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_NAME"),
)

subreddits = ['depression', 'mentalhealth', 'anxiety']
posts = []

for sub in subreddits:
    for post in reddit.subreddit(sub).hot(limit=5):  # or .new(limit=500)
        posts.append({
            'title': post.title,
            'text': post.selftext,
        })

# Define the filename for your JSON file
json_file_path = "reddit_scrapped_data.json"

# Pre-process the long description
for post in posts:
    wrapped_title = textwrap.wrap(post["title"], width=max_line_length, break_long_words=False)
    post["title"] = wrapped_title # Now it's a list of strings
    wrapped_text = textwrap.wrap(post["text"], width=max_line_length, break_long_words=False)
    post["text"] = wrapped_text # Now it's a list of strings

# Open the file in write mode ('w')
# The 'indent' parameter makes the JSON file human-readable with indentation
# 'json.dump()' writes the dictionary to the file
try:
    with open(json_file_path, 'w') as json_file:
        json.dump(posts, json_file, indent=4)
    print(f"Dictionary successfully stored to '{json_file_path}'")
except IOError as e:
    print(f"Error writing to file: {e}")
except TypeError as e:
    print(f"Error serializing dictionary (contains unsupported types?): {e}")

"""
#print(reddit.read_only)

# for submission in reddit.subreddit("test").hot(limit=10):
#     print(submission.title)

# assume you have a praw.Reddit instance bound to variable `reddit`
subreddit = reddit.subreddit("redditdev")

print(subreddit.display_name)
# Output: redditdev
print(subreddit.title)
# Output: reddit development
print(subreddit.description)
# Output: a subreddit for discussion of ...

# assume you have a Subreddit instance bound to variable `subreddit`
for submission in subreddit.hot(limit=10):
    print(submission.title)
    # Output: the submission's title
    print(submission.score)
    # Output: the submission's score
    print(submission.id)
    # Output: the submission's ID
    print(submission.url)
    # Output: the URL the submission points to or the submission's URL if it's a self post

# Depression, Mental Health
# Keywords:
"""


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