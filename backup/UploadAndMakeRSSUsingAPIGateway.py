import requests
import base64
import json

ENCODING = 'utf-8'
filePath = r"C:\Users\Walt\Pictures\ostrich.jpg"
fileName = r"ostrich2.jpg"

with open(filePath, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

# print(len(encoded_string))

url = 'https://gv1yedhm7b.execute-api.us-west-2.amazonaws.com/prod/execution'

# myobj = json.dumps({
# 	'name': fileName,
# 	'taxonomy': {'species': 'Flamingo'},
# 	'file': encoded_string.decode(ENCODING),
# 	"input": "{}",
# 	"stateMachineArn": "arn:aws:states:us-west-2:057004871391:stateMachine:UploadImgAndCreateRss"
# 	},
# 	indent = 2)

myobj = json.dumps({
	'name': fileName,
	"input": '{	"name": "fileName", "file":' + encoded_string.decode(ENCODING) +' }',
	"stateMachineArn": "arn:aws:states:us-west-2:057004871391:stateMachine:UploadImgAndCreateRss"
	},
	indent = 2)


x = requests.post(url, data = myobj)

print(x.text)

### data:image/jpeg;base64,