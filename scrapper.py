import praw
import os
import pandas as pd
import time

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

reddit = praw.Reddit(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    user_agent=os.getenv("USER_NAME"),
)

subreddits = [
  'Anxiety', 
  'Anxietyhelp', 
  'depression', 
  'MentalHealth', 
  'ADHD', 
  'ADHDers', 
  'bipolar', 
  'bipolar2', 
  'OCD', 
  'hoarding', 
  'CPTSD', 
  'Traumatoolbox', 
  'BPD', 
  'personalitydisorders', 
  'insomnia', 
  'sleepdisorders', 
  'ODD', 
  'Anger', 
  'stopdrinking', 
  'addiction',
  'aspd',
  'GetDisciplined',
  'NPD',
  'BipolarReddit',
  'BipolarSOs',
  'AskReddit',
  'dataisbeautiful'
]

#[ 'depression', 'bipolar', 'anxiety', 'borderline', 'dementia', 'schizophrenia', 'anorexia', 'bulimia']
# Others: ['ADHD', 'OppositionalDefiant', 'autism']

categories = ['hot', 'new', 'rising']
top_times = ['day', 'week', 'month', 'year', 'all']

posts = []
seen_ids = set()

for sub in subreddits:
    subreddit = reddit.subreddit(sub)
    print(f"\nSubreddit: r/{sub}")
    for cat in categories:
        print(f"  Scraping {cat} posts ...")
        try:
            submissions = getattr(subreddit, cat)(limit=1000)
            for post in submissions:
                if post.id not in seen_ids:
                    posts.append({
                        'subreddit': sub,
                        # 'category': cat,
                        'id': post.id,
                        # 'title': post.title,
                        'selftext': post.selftext,
                        # 'author': str(post.author),
                        # 'score': post.score,
                        # 'num_comments': post.num_comments,
                        # 'created_utc': post.created_utc,
                        # 'flair': getattr(post, 'link_flair_text', None),
                        # 'url': post.url
                    })
                    seen_ids.add(post.id)
            time.sleep(1)
        except Exception as e:
            print(f"    Failed to scrape {cat}: {e}")

    for time_filter in top_times:
        print(f"  Scraping top posts for {time_filter} ...")
        try:
            submissions = subreddit.top(time_filter=time_filter, limit=1000)
            for post in submissions:
                if post.id not in seen_ids:
                    posts.append({
                        'subreddit': sub,
                        # 'category': 'top_' + time_filter,
                        'id': post.id,
                        # 'title': post.title,
                        'selftext': post.selftext,
                        # 'author': str(post.author),
                        # 'score': post.score,
                        # 'num_comments': post.num_comments,
                        # 'created_utc': post.created_utc,
                        # 'flair': getattr(post, 'link_flair_text', None),
                        # 'url': post.url
                    })
                    seen_ids.add(post.id)
            time.sleep(1)
        except Exception as e:
            print(f"    Failed to scrape top/{time_filter}: {e}")

    print(f"  Total posts collected so far: {len(posts)}")
    if len(posts) >= 80000:
        break

df = pd.DataFrame(posts).drop_duplicates(subset=['id'])
if len(df) > 80000:
    df = df.sample(n=80000, random_state=42)  

df.to_csv('mentalhealth_reddit_posts_ds.csv', index=False)
print(f"\nSaved {len(df)} unique posts to mentalhealth_reddit_posts_ds.csv")