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
	f_statuses = [{'info':'', 'rt_info':'' 'text':''} for _ in range(len(statuses))]
	for i, status in enumerate(statuses):
		f_statuses[i].info = get_jst_str(status.created_at) + ' ' +\
			status.user.name + ' @' + status.user.screen_name
		try: # Retweet
			r = status.retweeted_status
			f_statuses[i].rt_info = get_jst_str(r.created_at) + ' ' +\
				r.user.name + ' @' + r.user.screen_name
			f_statuses[i].text = r.full_text
		except AttributeError:  # Not a Retweet
			f_statuses[i].text = status.full_text
	return statuses_str
