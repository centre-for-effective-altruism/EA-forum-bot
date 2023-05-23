from create_client import create_client
from forumpost import forumpost

def post_tweet(event="", context=""):
    client = create_client()
    print("API created")

    post = forumpost()
    posts = post.fetch_relevant_posts()

    bot_user = client.get_user(username="eaforumposts")

    # get the last ~week of tweets to check for duplicates
    tweets = client.get_users_tweets(
        id=bot_user.data.id,
        tweet_fields=["entities"],
        max_results=6*7)

    # expanded_url is buried in the tweet object like this: tweets.data.entities->urls.expanded_url
    # get the url of each post (posts[i][0]) and check it doesn't appear in expanded_url
    deduped_posts = []
    for top_post in posts:
        posturl = top_post[0]
        if not posturl:
            continue
        for tweet in tweets.data:
            if not tweet.entities:
                continue
            if 'urls' not in tweet.entities:
                continue
            for url in tweet.entities['urls']:
                if 'expanded_url' not in url:
                    continue
                if posturl in url['expanded_url']:
                    print("Found duplicate, skipping")
                    break
            else:
                continue
            break
        else:
            deduped_posts.append(top_post)

    for top_post in deduped_posts:
        posturl = top_post[0]
        title = top_post[1]
        author = top_post[3]

        tweet = post.write_tweet(title, author, posturl)
        try:
            if tweet:
                # client.create_tweet(text=tweet)
                print(tweet)
                # only post the top post
                break
        except Exception as e:
            print(e)
            print("Error creating tweet, continuing to next best...")


post_tweet()