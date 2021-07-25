from create_api import create_api
from forumpost import forumpost

def post_tweet(event="", context=""):
    api = create_api()

    post = forumpost()
    post.get_relevant_posts()
    post.get_existing_tweets(api)
    post.select_post()
    tweet = post.write_tweet()
    try:
        if tweet: 
            api.update_status(status=tweet)
    except Exception as e:
        raise e


post_tweet()