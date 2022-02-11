import os
import tweepy
from util import get_jst_HM, get_jst_YMDHM

TWITTER_KEYS = os.getenv('CUSTOMCONNSTR_TWITTER_KEYS')
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = TWITTER_KEYS.split(';')
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

def reformat_status(raw):
	formatted = {}
	formatted['id'] = raw.id_str
	formatted['created_at'] = get_jst_HM(raw.created_at)
	formatted['name'] = raw.user.name
	formatted['screen_name'] = raw.user.screen_name

	try:                          # is retweet
		raw = raw.retweeted_status
		formatted['is_rt'] = True
		formatted['rt_created_at'] = get_jst_YMDHM(raw.created_at)
		formatted['rt_name'] = raw.user.name
		formatted['rt_screen_name'] = raw.user.screen_name
	except AttributeError:        # is not retweet
		formatted['is_rt'] = False

	formatted['text'] = raw.full_text
	formatted['can_fav'] = not raw.favorited
	formatted['can_rt'] = not raw.user.protected
	formatted['in_reply_to'] = raw.in_reply_to_status_id_str # id_str or None
	formatted['has_img'] = 'media' in raw.entities

	return formatted

def update_status(body=None):
	if not body:
		return False
	tweepy_api.update_status(body)
	return True

def get_timeline():
	raw_statuses = tweepy_api.home_timeline(count=200, tweet_mode='extended')
	statuses = [{} for _ in range(len(raw_statuses))]
	for i, s in enumerate(raw_statuses):
		statuses[i] = reformat_status(s)
	return statuses

def get_reply_chain(id):
	statuses = []
	while id:
		print(id, flush=True)
		s = tweepy_api.get_status(id, tweet_mode='extended')
		statuses.append(reformat_status(s))
		id = s.in_reply_to_status_id_str
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

def get_image_url(id, index=None):
	s = tweepy_api.get_status(id, tweet_mode='extended')
	try:                   # is retweet
		s = s.retweeted_status
	except AttributeError: # is not retweet
		pass
	media = s.extended_entities['media']
	if index is None:
		return [media[i]['media_url'] for i in range(len(media))]
	else:
		if index < 0 or index >= len(media):
			print(f'index:{index} >= len:{len(media)}')
			raise IndexError(index)
		return media[index]['media_url']
