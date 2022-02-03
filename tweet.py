import os
import tweepy
from util import get_jst_HM, get_jst_YMDHM

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
	statuses = [{} for _ in range(len(raw_statuses))]
	for i, s in enumerate(raw_statuses):
		statuses[i]['id'] = s.id_str
		statuses[i]['created_at'] = get_jst_HM(s.created_at)
		statuses[i]['name'] = s.user.name
		statuses[i]['screen_name'] = s.user.screen_name
		try: # Retweet
			rs = s.retweeted_status
			statuses[i]['is_rt'] = True
			statuses[i]['rt_created_at'] = get_jst_YMDHM(rs.created_at)
			statuses[i]['rt_name'] = rs.user.name
			statuses[i]['rt_screen_name'] = rs.user.screen_name
			statuses[i]['text'] = rs.full_text
		except AttributeError:  # Not a Retweet
			statuses[i]['is_rt'] = False
			statuses[i]['text'] = s.full_text
	return statuses

def create_favorite(id):
	tweepy_api.create_favorite(id)

def retweet():
	tweepy_api.retweet(id)

def show_image():
	pass
