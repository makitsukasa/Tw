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
	raw_statuses = tweepy_api.home_timeline(count=200, tweet_mode='extended')
	statuses = [{} for _ in range(len(statuses))]
	for i, status in enumerate(statuses):
		status[i]['created_at'] = get_jst_HM(status.created_at)
		status[i]['name'] = status.user.name
		status[i]['screen_name'] = status.user.screen_name
		try: # Retweet
			rs = status.retweeted_status
			status[i]['is_rt'] = True
			status[i]['rt_at'] = get_jst_YMDHM(rs.created_at)
			status[i]['rt_name'] = status.user.name
			status[i]['rt_screen_name'] = status.user.screen_name
			statuses[i]['text'] = rs.full_text
		except AttributeError:  # Not a Retweet
			status[i]['is_rt'] = False
			statuses[i]['text'] = status.full_text
	return statuses
