import os
from flask import request
import hashlib
import tweepy

TWITTER_KEYS = os.getenv("CUSTOMCONNSTR_TWITTER_KEYS")
CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = TWITTER_KEYS.split(";")
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
tweepy_api = tweepy.API(AUTH)

def tweet(body = None):
	if not body:
		return False
	tweepy_api.update_status(body)
	return True
