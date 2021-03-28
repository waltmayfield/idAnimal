import requests
import base64
import json
import time

ENCODING = 'utf-8'
#filePath = r"C:\Users\Walt\Pictures\ostrich.jpg"
#fileName = r"ostrich.jpg"



# print(len(encoded_string))

def UploadToS3AndDDB(filePath, taxonomy, score, source):
	url = 'https://gv1yedhm7b.execute-api.us-west-2.amazonaws.com/prod/UploadToS3'

	with open(filePath, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	
	myobj = json.dumps({
		'name': filePath,
		'taxonomy': taxonomy,
		'file': encoded_string.decode(ENCODING)
		},
		indent = 2)

	x = requests.post(url, data = myobj)

	print(f'Upload to S3 Response: {x.text}')

def createRSSFeed():
	# Now call the API to create the RSS feed
	url = 'https://gv1yedhm7b.execute-api.us-west-2.amazonaws.com/prod/makerssfeed'

	myobj = json.dumps({
		'name': f'APICallToMakeRSSFeed{hash(time.time())}'
		},
		indent = 2)

	x = requests.post(url, data = myobj)

	print(f'Create RSS Feed Response: {x.text}')
	### data:image/jpeg;base64,
