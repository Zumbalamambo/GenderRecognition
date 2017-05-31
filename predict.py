from scipy import misc, ndimage
from scipy.ndimage.interpolation import zoom
import os
import random
import shutil
import keras
from keras import backend as K
from keras.utils.data_utils import get_file
from keras.models import Sequential, Model
from keras.layers.core import Flatten, Dense, Dropout, Lambda
from keras.layers import Input
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD, RMSprop, Adam
from keras.preprocessing import image
import json
import numpy as np

def ConvBlock(layers, model, filters):
    for i in range(layers): 
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(filters, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))


def FCBlock(model):
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
vgg_mean = np.array([123.68, 116.779, 103.939]).reshape((3,1,1))

def vgg_preprocess(x):
    x = x - vgg_mean     # subtract mean
    return x[:, ::-1]    # reverse axis bgr->rgb
def VGG_16():
    model = Sequential()
    model.add(Lambda(vgg_preprocess, input_shape=(3,224,224)))

    ConvBlock(2, model, 64)
    ConvBlock(2, model, 128)
    ConvBlock(3, model, 256)
    ConvBlock(3, model, 512)
    ConvBlock(3, model, 512)

    model.add(Flatten())
    FCBlock(model)
    FCBlock(model)
    model.add(Dense(1000, activation='softmax'))
    return model

K.set_image_dim_ordering('th')
model = VGG_16()

model.pop()
for layer in model.layers: layer.trainable=False
model.add(Dense(2, activation='softmax'))
lr = 0.001
model.compile(optimizer=Adam(lr=lr), loss='categorical_crossentropy', metrics=['accuracy'])

model.load_weights("gender_recognition_weights.h5")

gen=image.ImageDataGenerator()
def predict():
    test_batches = gen.flow_from_directory('images/webapp',target_size=(224,224), 
                                           shuffle=False, batch_size=5, class_mode=None)
    preds = model.predict_generator(test_batches, test_batches.nb_sample)
    predictions = preds[:,0]
    labels= np.round(1-preds[:,0])
    return labels
