!pip install praw
import praw
import pandas as pd
import time

reddit = praw.Reddit(
    client_id='',
    client_secret='',
    user_agent='MentalHealthScraper by u/Grand',
    username='',
    password=''
)

subreddits = [
    'mentalhealth', 'depression', 'Anxiety', 'SuicideWatch',
    'BPD', 'BipolarReddit', 'OCD', 'ptsd', 'lonely', 'socialanxiety'
]

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
                        'category': cat,
                        'id': post.id,
                        'title': post.title,
                        'selftext': post.selftext,
                        'author': str(post.author),
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'flair': getattr(post, 'link_flair_text', None),
                        'url': post.url
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
                        'category': 'top_' + time_filter,
                        'id': post.id,
                        'title': post.title,
                        'selftext': post.selftext,
                        'author': str(post.author),
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'flair': getattr(post, 'link_flair_text', None),
                        'url': post.url
                    })
                    seen_ids.add(post.id)
            time.sleep(1)
        except Exception as e:
            print(f"    Failed to scrape top/{time_filter}: {e}")

    print(f"  Total posts collected so far: {len(posts)}")
    if len(posts) >= 20000:
        break

df = pd.DataFrame(posts).drop_duplicates(subset=['id'])
if len(df) > 20000:
    df = df.sample(n=20000, random_state=42)  

df.to_csv('mentalhealth_reddit_posts_20k.csv', index=False)
print(f"\nSaved {len(df)} unique posts to mentalhealth_reddit_posts_20k.csv")
