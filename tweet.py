import os
import tweepy
from util import get_jst_str

TWITTER_KEYS = os.getenv('CUSTOMCONNSTR_TWITTER_KEYS')
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = TWITTER_KEYS.split(';')
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

def update_status(body=None):
	if not body:
		return False
	tweepy_api.update_status(body)
	return True

def home_timeline():
	statuses = tweepy_api.home_timeline(count=200, tweet_mode='extended')
	statuses_str = ['' for _ in range(len(statuses))]
	for i, status in enumerate(statuses):
		status_str = get_jst_str(status.created_at) + ' ' +\
			status.user.name + ' @' + status.user.screen_name + '<br>'
		try: # Retweet
			status_str += status.retweeted_status.full_text
		except AttributeError:  # Not a Retweet
			status_str += status.full_text
		statuses_str[i] = status_str
	return statuses_str
