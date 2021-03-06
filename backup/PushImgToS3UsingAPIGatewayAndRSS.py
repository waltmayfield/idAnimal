import requests
import base64
import json

ENCODING = 'utf-8'
filePath = r"C:\Users\Walt\Pictures\ostrich.jpg"
fileName = r"ostrich.jpg"

with open(filePath, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

# print(len(encoded_string))

url = 'https://gv1yedhm7b.execute-api.us-west-2.amazonaws.com/prod/UploadToS3'

myobj = json.dumps({
	'name': fileName,
	'taxonomy': {'species': 'Pterodactyl'},
	'file': encoded_string.decode(ENCODING)
	},
	indent = 2)

x = requests.post(url, data = myobj)

print(f'Upload to S3 Response: {x.text}')


# Now call the API to create the RSS feed
url = 'https://gv1yedhm7b.execute-api.us-west-2.amazonaws.com/prod/makerssfeed'

myobj = json.dumps({
	'name': 'APICallToMakeRSSFeed'
	},
	indent = 2)

x = requests.post(url, data = myobj)

print(f'Create RSS Feed Response: {x.text}')
### data:image/jpeg;base64,