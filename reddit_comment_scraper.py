import Scraper_config as cfg
import praw
from praw.models import MoreComments
import pandas as pd
import time
from calendar import timegm
from tqdm import tqdm
import math


r = praw.Reddit(client_id=cfg.client_id, client_secret=cfg.client_secret, user_agent=cfg.bot_username)


def get_comments(url, date, limit=32):
    eod = "T23:59:59"  # end of the day at 23:59:59
    deadline = timegm(time.strptime(date+eod, "%Y-%m-%dT%H:%M:%S")) + 14400 # convert to eastern time
    submission = r.submission(url=url)
    submission.comments.replace_more(limit=limit)
    df = pd.DataFrame(columns=["timestamp_utc", "comment", "score"])
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        if top_level_comment.created_utc > deadline:
            # print("reject", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(top_level_comment.created_utc)))
            continue
        row = [top_level_comment.created_utc, top_level_comment.body, top_level_comment.score]
        df.loc[len(df)] = row
    return df


def extract_comments_from_links(DIR, limit=32):
    links = pd.read_csv(DIR)
    all_comments = pd.DataFrame(columns=["thread_date", "timestamp_utc", "comment", "score"])
    for index, row in tqdm(links.iterrows()):
        date, url = row["date"], row["url"]
        if type(url) == float:
            continue
        df = get_comments(url, date, limit=limit)
        df["thread_date"] = date
        all_comments = pd.concat([all_comments, df], ignore_index=True)
    return all_comments


if __name__ == '__main__':
    DIR = "testfile.csv"#"daily_discussion_thread_urls.csv"
    all_comments = extract_comments_from_links(DIR, limit=15)
    all_comments.to_csv("test_comments.csv")


    # url = "https://www.reddit.com/r/wallstreetbets/comments/rcfcod/daily_discussion_thread_for_december_09_2021/"
    # date = "2021-12-09"
    # df = get_comments(url, date, limit=1)
    # print(len(df))
    # print(df.head())
    # print(df.tail())
