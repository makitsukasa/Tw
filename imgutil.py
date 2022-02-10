import requests
from io import BytesIO

def get_image(img_url):
	return BytesIO(requests.get(img_url).content).getvalue()
