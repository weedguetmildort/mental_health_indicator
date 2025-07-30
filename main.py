import os
import json
import praw
import textwrap
import re
import pandas as pd
import matplotlib.pyplot as plt

from dotenv import load_dotenv, find_dotenv
from wordcloud import WordCloud
 

def scrape_reddit():
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

def clean_data():
    data = pd.read_csv('mentalhealth.csv')
    print(data.head())


    print()

    my_data = data[['subreddit','title', 'selftext']]
    my_data.columns = ['subreddit', 'title', 'post']

    print(my_data.head())

    posts = my_data['post'].tolist()

    cleaned_posts = [clean_text(str(post)) for post in posts]

    my_data['cleaned_post'] = cleaned_posts

    my_data.to_csv('cleanmentalhealth.csv')

    #print(my_data['cleaned_post'].str.split().explode().value_counts().head(30))

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(my_data['cleaned_post']))

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off') # Hide axes
    plt.show()

    #print(my_data.head(50))
    return

def clean_text(text):
    
    text = re.sub(r"[^\w\s]", " ", text)

    text = re.sub(r"\b[a-zA-Z]\b", " ", text)

    text = re.sub(r"<[^>]*>", " ", text)

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text


if __name__=="__main__":
    clean_data()