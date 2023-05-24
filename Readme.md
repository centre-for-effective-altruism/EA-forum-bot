# A Twitter Bot that regularly tweets the current top posts from the EA Forum

This bot monitors the [effective altruism forum](https://forum.effectivealtruism.org/) and continuosly tweets that reached 40 karma within the first 6 days of publication. 

## Running the bot

- clone this repository by running `git clone https://github.com/nikosbosse/ea-forum-bot`
- create a virtual python environment `python -m venv env` and activate it `source env/bin/activate`
- install dependencies `pip install -r requirements.txt`
- setup a new Twitter account and developer account. Instructions from a similar project [here](https://followtheargument.org/how-to-create-a-twitter-bot-that-posts-a-random-daily-article). Store your credentials in a file called .env
- make a tweet by running `python main.py`

The bot is deployed to google servers. Some instructions on how to do that [here](https://github.com/nikosbosse/DailyElectroSet)

## Update 2023-05-24:

This repo was forked from Nikos' original to get it working again. The bot is currently (2023-05-24) running as a google cloud function in my ([Will Howard's](https://github.com/Will-Howard)) account. The changes made to get it working were roughly:
 - Updating the classes which are selected on in `fetch_relevant_posts` (these had changed due to the forum being redesigned)
 - Switching to using v2 of the twitter API rather than v1.1 (v1.1 appears to have been deprecated for new users, or at least I couldn't get it to work)
 - Changing the name of the project in `deploy.sh` and `schedule.sh` to match what was in my Google Cloud account
