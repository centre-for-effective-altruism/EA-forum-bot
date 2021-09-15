from bs4 import BeautifulSoup
from create_api import create_api
import requests 
import time
import random
import tweepy

#><a href="/posts/dZjHvaDprCsc7ogF6/predicting-open-phil-grants"><span><span>Predicting Open Phil Grants </span></span></a><span class="PostsTitle-hideSmDown"><span class="PostsItemIcons-iconSet"></span></span></span>


class forumpost:    

    def __init__(self):
        self.url = "https://forum.effectivealtruism.org/allPosts"

    
    def get_relevant_posts(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, "lxml")

        self.relevant_posts = []
        
        # find all posts by selecting the appropriate class
        posts = soup.find_all("div", {"class": "PostsItem2-postsItem PostsItem2-withGrayHover PostsItem2-dense"})
        
        # iterate over all posts and find the ones that have enough karma
        for post in posts:

            # find out when the post was posted and discard if it older than 6 days 
            # that's done because Twitter only gives you 7 days of past tweets to compare against
            try:             
                timeposted = post.find("span", {"class": "Typography-root Typography-body2 PostsItem2MetaInfo-metaInfo PostsItemDate-postedAt"}).text
            except: 
                continue
            # if post is older than a day, filter
            if "d" in timeposted: 
                timeposted = int(timeposted.replace("d", ""))
                if timeposted > 6: 
                    continue            

            # select the appropriate span and from that the subspan and get its text
            karma = post.find("span", {"class": "Typography-root Typography-body2 PostsItem2MetaInfo-metaInfo PostsItem2-karma"})
            karma = karma.select_one("span", {"title": "LWTooltip-root"}).text

            authors = post.find("span", {"class": "Typography-root Typography-body2 PostsItem2MetaInfo-metaInfo PostsItem2-author"})
            authors = authors.find_all("a")
            authorlist = []
            for author in authors:
                authorlist.append(author.contents[0])

            author = " & ".join(authorlist)

            # identify high impact posts, get their url and title
            if int(karma) > 40: 
                impactpost = post.find("span", {"class": "PostsTitle-root"})
                
                link = impactpost.find('a')                
                url = "https://forum.effectivealtruism.org" + link['href']
                
                title = link.contents[0]
                title = title.find("span").text             
                
                self.relevant_posts.append([url, title, int(karma), author])
            

    def get_existing_tweets(self, api):
        self.tweeted_posts = []
        for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended').items():

            tweet_text = status._json["full_text"]
            
            # remove first part befor title and clean ampersand

            post_title = tweet_text.replace('New top post from the EA Forum: \n  \n"', '')
            post_title = post_title.split('" by', 1)[0]
            post_title = post_title.replace("&amp;", "&")

            urls = status._json["entities"]["urls"]

            if len(urls) == 0: 
                return

            post_url = next(item["expanded_url"] for item in urls if "https://forum.effectivealtruism.org/posts" in item['expanded_url'])
            self.tweeted_posts.append(post_url)
            
            

    def select_post(self): 
        # only keep if the title is not among the already tweeted posts

        print("relevant posts:\n")
        print(self.relevant_posts)

        print("\n tweeted posts:\n")
        print(self.tweeted_posts)

        # check whether URL for relevant post was already tweeted
        new_posts = [item for item in self.relevant_posts if item[0] not in self.tweeted_posts]

        # if no new posts, just do nothing. 
        if not new_posts:
            self.title = None
            return None

        # get the element with the highest karma
        highest_post = max(new_posts, key=lambda item:item[2])

        # title is second element, URL is first one
        self.posturl = highest_post[0]
        self.title = highest_post[1]
        self.author = highest_post[3]

    def write_tweet(self):
        
        # if no new post, do nothing
        if not self.title:
            return None 

        message = [
            "New top post from the EA Forum:",
            " ",
            f'"{self.title}" ' 
            f"by {self.author}", 
            f"{self.posturl}"
        ]
        message = " \n".join(message)
        return message

api = create_api()