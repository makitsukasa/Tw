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
		statuses[i]['can_fav'] = not s.favorited
		statuses[i]['can_rt'] = not s.user.protected

		try:                          # is retweet
			rs = s.retweeted_status
			statuses[i]['is_rt'] = True
			statuses[i]['rt_created_at'] = get_jst_YMDHM(rs.created_at)
			statuses[i]['rt_name'] = rs.user.name
			statuses[i]['rt_screen_name'] = rs.user.screen_name
			statuses[i]['text'] = rs.full_text
		except AttributeError:        # is not retweet
			statuses[i]['is_rt'] = False
			statuses[i]['text'] = s.full_text

		if not 'media' in s.entities: # has no media
			statuses[i]['media'] = []
		else:                         # has media
			statuses[i]['media'] = [None for _ in range(len(s.entities['media']))]
			for j, media in enumerate(s.entities['media']):
				statuses[i]['media'][j] = media['media_url']

	return statuses

def create_favorite(id):
	try:
		tweepy_api.create_favorite(id)
		return True
	except Exception as e:
		return False

def retweet(id):
	try:
		tweepy_api.retweet(id)
		return True
	except Exception as e:
		return False
