import os
import re
import tweepy
from dateutil import get_datetime_str

TWITTER_KEYS = os.getenv('CUSTOMCONNSTR_TWITTER_KEYS')
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = TWITTER_KEYS.split(';')
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

def reformat_status(raw):
	formatted = {}
	formatted['id'] = raw.id_str
	formatted['created_at'] = get_datetime_str(raw.created_at)
	formatted['name'] = raw.user.name
	formatted['screen_name'] = raw.user.screen_name
	formatted['has_no_reply'] = False

	if hasattr(raw, 'retweeted_status'): # is retweet
		raw = raw.retweeted_status
		formatted['is_rt'] = True
		formatted['rt_created_at'] = get_datetime_str(raw.created_at)
		formatted['rt_name'] = raw.user.name
		formatted['rt_screen_name'] = raw.user.screen_name
	else:
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

def get_reply_upstream(id):
	statuses = []
	for _ in range(20):
		if not id:
			break
		s = tweepy_api.get_status(id, tweet_mode='extended')
		if hasattr(s, 'retweeted_status'):
			s = s.retweeted_status
		statuses.append(reformat_status(s))
		id = s.in_reply_to_status_id_str
	return statuses

def get_reply_downstream(id):
	s = tweepy_api.get_status(id, tweet_mode='extended')
	if hasattr(s, 'retweeted_status'):
		s = s.retweeted_status
		id = s.id_str
	screen_name = s.user.screen_name
	statuses = [reformat_status(s)]
	for _ in range(20):
		replies = []
		search_results = tweepy.Cursor(
			tweepy_api.search_tweets,
			since_id = id,
			q = 'to:{}'.format(screen_name),
			tweet_mode = 'extended').items()
		print('to:' + screen_name, id)
		while True:
			try:
				r = search_results.next()
				print(r.id, '->', r.in_reply_to_status_id_str)
				if r.in_reply_to_status_id_str == id:
					print('reply of tweet:{}'.format(r.full_text))
					replies.append(r)
			except tweepy.TooManyRequests as e:
				print('Twitter api rate limit reached'.format(e))
				continue
			except tweepy.HTTPException as e:
				print('Tweepy error occured:{}'.format(e))
				break
			except StopIteration:
				break
			except Exception as e:
				print('Failed while fetching replies {}'.format(e))
				break

		if len(replies) == 0:
			statuses[0]['has_no_reply'] = True
			break
		elif len(replies) > 1:
			for r in replies:
				statuses.insert(0, reformat_status(r))
			break
		else:
			statuses.insert(0, reformat_status(replies[0]))
			id = replies[0].id
			screen_name = replies[0].user.screen_name
	return statuses

def create_favorite(id):
	try:
		tweepy_api.create_favorite(id)
		return True
	except Exception:
		return False

def destroy_favorite(id):
	try:
		tweepy_api.destroy_favorite(id)
		return True
	except Exception:
		return False

def retweet(id):
	try:
		tweepy_api.retweet(id)
		return True
	except Exception:
		return False

def get_image_url(id, index=None):
	s = tweepy_api.get_status(id, tweet_mode='extended')
	if hasattr(s, 'retweeted_status'):
		s = s.retweeted_status
	media = s.extended_entities['media']
	if index is None:
		return [media[i]['media_url'] for i in range(len(media))]
	else:
		if index < 0 or index >= len(media):
			raise IndexError(index)
		return media[index]['media_url']
