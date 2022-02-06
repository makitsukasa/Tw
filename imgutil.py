from PIL import Image
import requests
from io import BytesIO
import base64

# https://teratail.com/questions/89341
def base64ify(img_url):
	print(img_url)
	response = requests.get(img_url)
	img = Image.open(BytesIO(response.content))

	buffer = BytesIO()
	img.save(buffer, 'jpg')
	base64string = base64.b64encode(buffer.getvalue())
	return 'data:image/jpg;base64,' + base64string.decode('utf-8')
