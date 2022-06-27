# https://sleepless-se.net/2018/11/17/hwo-to-get-tweepy-accesstoken-on-python3/

import tweepy
import urllib
from key import CONSUMER_KEY, CONSUMER_SECRET

def get_oauth_token(url: str) -> str:
	querys = urllib.parse.urlparse(url).query
	querys_dict = urllib.parse.parse_qs(querys)
	return querys_dict["oauth_token"][0]

if __name__ == "__main__":
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	try:
		redirect_url = auth.get_authorization_url()
	except tweepy.errors.TweepError:
		print("Error! Failed to get request token.")

	oauth_token = get_oauth_token(redirect_url)
	print("oauth_token:", oauth_token)
	auth.request_token["oauth_token"] = oauth_token
	print("Redirect URL:")
	print(redirect_url)

	verifier = input("You can check Verifier on url parameter. Please input Verifier:")
	auth.request_token["oauth_token_secret"] = verifier

	try:
		auth.get_access_token(verifier)
	except tweepy.errors.TweepError:
		print("Error! Failed to get access token.")

	print("access token key:", auth.access_token)
	print("access token secret:", auth.access_token_secret)
