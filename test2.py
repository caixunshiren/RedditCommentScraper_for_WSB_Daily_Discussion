import Scraper_config as cfg
import praw
from praw.models import MoreComments


r = praw.Reddit(client_id=cfg.client_id, client_secret=cfg.client_secret, user_agent=cfg.bot_username)


def get_comments(url, limit = 32):
    submission = r.submission(url=url)
    submission.comments.replace_more(limit=limit)
    print(submission.num_comments)

    comment_list = []
    for top_level_comment in submission.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        comment_list.append(top_level_comment)
    print(len(comment_list))

    for i in range(10):
        top_level_comment = comment_list[i]
        print("debug:")
        print(top_level_comment.created_utc, top_level_comment.body, top_level_comment.score)
        print(type(top_level_comment.created_utc), type(top_level_comment.body), type(top_level_comment.score))
        print("-----")
    # submission.comments.replace_more(limit=None, threshold=0)





if __name__ == '__main__':
    url = "https://www.reddit.com/r/wallstreetbets/comments/rcfcod/daily_discussion_thread_for_december_09_2021/"
    get_comments(url, limit=1)
