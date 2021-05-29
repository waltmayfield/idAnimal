#source ~/.virtualenvs/cv/bin/activate

import cv2
import numpy as np
import time
from tflite_runtime.interpreter import Interpreter

from FunctionsS3RSS import *


def load_labels(path): # Read the labels from the text file as a Python list.
  with open(path, 'r') as f:
    return [line.strip() for i, line in enumerate(f.readlines())]

def set_input_tensor(interpreter, image):
  tensor_index = interpreter.get_input_details()[0]['index']
  input_tensor = interpreter.tensor(tensor_index)()[0]
  input_tensor[:, :] = image

def classify_image(interpreter, image, top_k=1):
  set_input_tensor(interpreter, image)

  interpreter.invoke()
  output_details = interpreter.get_output_details()[0]
  output = np.squeeze(interpreter.get_tensor(output_details['index']))

  scale, zero_point = output_details['quantization']
  output = scale * (output - zero_point)

  ordered = np.argpartition(-output, 1)
  return [(i, output[i]) for i in ordered[:top_k]][0]

#/home/pi/tflite_models/inception_v4_299_quant_20181026/
data_folder = '/home/pi/tflite_models/inception_v4_299_quant_20181026/'
model_path = data_folder + "inception_v4_299_quant.tflite"
#label_path = data_folder + "labels_mobilenet_quant_v1_224.txt"

data_folder = '/home/pi/tflite_models/mobilenet_v1_1.0_224_quant_and_labels/'
#model_path = data_folder + "mobilenet_v1_1.0_224_quant.tflite"
label_path = data_folder + "labels_mobilenet_quant_v1_224.txt"


interpreter = Interpreter(model_path)
print("Model Loaded Successfully.")

interpreter.allocate_tensors()
_, height, width, _ = interpreter.get_input_details()[0]['shape']
print("Input Image Shape (", width, ",", height, ")")

#Load the target labels
labels = load_labels(label_path)

cam = cv2.VideoCapture(0)

#cv2.namedWindow("test")

img_counter = 0

numPredictionsHonored = 1
LastXTracker = [("dummy",0)]*numPredictionsHonored

lastTime = time.time()
lastFrame = None
mseMotion = None

while True:
	ret, frame = cam.read()
	
	if lastFrame is not None:
		mseMotion = np.square(np.subtract(frame, lastFrame)).mean()
	lastFrame = frame
	
	if not ret:
		print("failed to grab frame")
		break
	
	#Resize image to to imput tensor size.
	image = cv2.resize(frame,(height,width))
	
	#Classify Image
	label_id, prob = classify_image(interpreter, image)
	classification_label = labels[label_id]
	print(f"Image Label is :{classification_label}, with Accuracy :{np.round(prob*100, 2)}%, Motion mse: {mseMotion}.")
	
	LastXTracker = [(classification_label, prob)] + LastXTracker[0:-1]
	
	#Check if all labels are the same
	LastXLabels = [x[0] for x in LastXTracker]
	labelsAllSame = LastXLabels.count(LastXLabels[0])==len(LastXLabels)
	if labelsAllSame:
		LastXprobs = [x[1] for x in LastXTracker]
		if min(LastXprobs) > 0.96 and classification_label == 'hummingbird':
			print(f"Image Classified as {classification_label}")
			
			imgPath = '/home/pi/Documents/idAnimal/temp.jpg'
			cv2.imwrite(imgPath,frame)
			
			UploadToS3AndDDB('testuser',imgPath,{"source": model_path, "score": str(prob), "species":classification_label},prob,'MobileNetV1')
			
			createRSSFeed()
			
			#Reset the tracker
			LastXTracker = [("dummy",0)]*numPredictionsHonored
			print('Wait 20 seconds after uploading image')
			time.sleep(20)
			
	#cv2.imshow("test", frame)
	
	k = cv2.waitKey(1)
	if k%256 == 27:
		# ESC pressed
		print(f'Image size: {frame.shape}')
		print(f'Frame type: {type(frame)}')
		print("Escape hit, closing...")
		break
	
	
	classification_time = np.round(time.time()-lastTime, 3)
	print(f"Frame Time = {classification_time} seconds")
	lastTime = time.time()

cam.release()

cv2.destroyAllWindows()
