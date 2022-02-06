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

		try:                          # is retweet
			s = s.retweeted_status
			statuses[i]['is_rt'] = True
			statuses[i]['rt_created_at'] = get_jst_YMDHM(s.created_at)
			statuses[i]['rt_name'] = s.user.name
			statuses[i]['rt_screen_name'] = s.user.screen_name
		except AttributeError:        # is not retweet
			statuses[i]['is_rt'] = False

		statuses[i]['text'] = s.full_text
		statuses[i]['can_fav'] = not s.favorited
		statuses[i]['can_rt'] = not s.user.protected
		statuses[i]['in_reply_to'] = s.in_reply_to_status_id_str # id_str or None
		statuses[i]['has_img'] = 'media' in s.entities

	return statuses

def create_favorite(id):
	try:
		tweepy_api.create_favorite(id)
		return True
	except Exception as e:
		return False

def destroy_favorite(id):
	try:
		tweepy_api.destroy_favorite(id)
		return True
	except Exception as e:
		return False

def retweet(id):
	try:
		tweepy_api.retweet(id)
		return True
	except Exception as e:
		return False

def get_image_url(id):
	s = tweepy_api.get_status(id, tweet_mode='extended')
	try:                   # is retweet
		s = s.retweeted_status
	except AttributeError: # is not retweet
		pass
	media = s.extended_entities['media']
	return [media[i]['media_url'] for i in range(len(media))]
