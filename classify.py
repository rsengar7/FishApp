# python classify.py --model pokedex.model --labelbin lb.pickle --image examples/charmander_counter.png

from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import pickle
import cv2
import os


def image_predict(image_path,model_name='fish.model',labelbin='lb.pickle'):

	image = cv2.imread(image_path)
	output = image.copy()
 
	image = cv2.resize(image, (96, 96))
	image = image.astype("float") / 255.0
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	print("[INFO] loading network...")
	model = load_model(model_name)
	lb = pickle.loads(open(labelbin, "rb").read())

	proba = model.predict(image)[0]
	idx = np.argmax(proba)
	label = lb.classes_[idx]

	filename = image_path[image_path.rfind(os.path.sep) + 1:]

	label = "{}: {:.2f}".format(label, proba[idx] * 100)

	return label


