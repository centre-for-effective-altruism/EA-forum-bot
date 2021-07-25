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
            timeposted = post.find("span", {"class": "Typography-root Typography-body2 PostsItem2MetaInfo-metaInfo PostsItemDate-postedAt"}).text
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
        for status in tweepy.Cursor(api.user_timeline).items():
            tweet_text = status._json["text"]
            
            # remove first part befor title
            post_title = tweet_text.replace('New top post from the EA Forum: \n  \n"', '')
            post_title = post_title.split('" by', 1)[0]

            self.tweeted_posts.append(post_title)
            

    def select_post(self): 
        # only keep if the title is not among the already tweeted posts
        new_posts = [item for item in self.relevant_posts if item[1] not in self.tweeted_posts]

        # get the element with the highest karma
        highest_post = max(new_posts, key=lambda item:item[2])

        # title is second element, URL is first one
        self.posturl = highest_post[0]
        self.title = highest_post[1]
        self.author = highest_post[3]

    def write_tweet(self):
        
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












""" def get_ssc_links(self):
            # load html and parse using bs4
            req = Request(self.ssc_url, headers={'User-Agent': 'Mozilla/5.0'})
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")
            # create empty list with links and fill
            links = []
            for link in soup.findAll('a'):
                current_link = link.get('href')
                # check that the link satisfies some conditions
                condition = (
                    (current_link is not None) and
                    ("wp-login.php" not in current_link) and
                    ("slatestarcodex" in current_link) and
                    ("#comment" not in current_link) and
                    ("open-thread" not in current_link) and
                    ("open-thresh" not in current_link))
                if condition:
                    # add more flltering to get rid of some summary page links
                    manual_filter = [
                        "https://slatestarcodex.com/",
                        "https://slatestarcodex.com/",
                        "https://slatestarcodex.com/about/",
                        "https://slatestarcodex.com/archives/",
                        "https://slatestarcodex.com/2021/",
                        "https://slatestarcodex.com/2020/",
                        "https://slatestarcodex.com/2019/",
                        "https://slatestarcodex.com/2018/",
                        "https://slatestarcodex.com/2017/",
                        "https://slatestarcodex.com/2016/",
                        "https://slatestarcodex.com/2015/",
                        "https://slatestarcodex.com/2014/",
                        "https://slatestarcodex.com/2013/"
                        ]
                    if current_link not in manual_filter:
                        links.append(current_link)
            return links

        logger.info("Looking up the full list of Astral Codex Ten articles")

        def get_acx_links(self):
            # set up a headless selenium browser
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
            self.driver.get(self.acx_url)
            self.driver.maximize_window()
            # scroll to the bottom of the page
            # first get current scroll height
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                # Wait to load page
                time.sleep(3)
                # Calculate new scroll height and compare with last height
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight")
                if new_height == last_height:
                    time.sleep(10)
                    break
                last_height = new_height
            # get the fully loaded page and parse it
            html_page = self.driver.page_source
            soup = BeautifulSoup(html_page, "lxml")
            links = []
            # find all div containers that are a post preview
            preview_class = "post-preview portable-archive-post "\
                            "has-image has-author-line"
            divs = [divs for divs in soup.findAll(
                "div", {"class": preview_class})]
            # iterate over all post previews to get the link and to
            # check whether the link is behind a paywall
            for div in divs:
                linkdiv = div.find(
                    "a", {"class": "post-preview-title newsletter"})
                link = linkdiv.get('href')
                article_attributes = div.find(
                    "table", {"class": "post-meta post-preview-meta custom"})
                paywalled = article_attributes.find(
                    "td", {"class": "post-meta-item audience-lock"})
                if ((paywalled is None) and ("open-thread" not in link)):
                    links.append(link)

            self.driver.close()
            return links

        self.all_links = get_acx_links(self) + get_ssc_links(self)
        logger.info("Randomly selecting a link to post")
        self.link = random.choice(self.all_links)
        print(self.link)

    def write_tweet(self):
        logger.info("Creating a message with the random article link")
        message = [
            "Here is your daily article from Astral Codex Ten "
            "/ Slate Star Codex:",
            f"{self.link}"
        ]
        message = " \n".join(message)
        return message """