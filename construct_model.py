import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import random
import pickle
import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from classification_model import GetTrainData
from matplotlib.pyplot import imshow
from test_cv2_2 import RemoveBackgroundFolder,SingleRemoveBackground
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.preprocessing.image import ImageDataGenerator

data_sets = GetTrainData(r"D:\imgs")
label_lists = data_sets["label_lists"]
x_train,y_train = data_sets["train"]
x_test,y_test = data_sets["test"]

#데이터전처리-표준화
x_train = x_train/255.
x_test = x_test/255.

#image confirm
rlist = [random.randint(0,len(x_train)-1) for _ in range(10)]
print(rlist)

for ix,num in enumerate(rlist):
    plt.subplot(2,5,ix+1)
    plt.imshow(x_train[ix])
    plt.title(label_lists[y_train[ix]])
    plt.xticks([])
    plt.yticks([])
plt.show()
print(type(y_train))

#onehot encoding
y_train = tf.one_hot(y_train,10)
y_test = tf.one_hot(y_test,10)
print(y_train.shape)
print(y_test.shape)
print(y_train[0])

#model config
model = Sequential()
model.add(Input(shape=(64,64,3)))
model.add(Conv2D(filters=64,kernel_size=5,strides=1,padding="same",activation="relu"))
model.add(MaxPool2D(pool_size=(3,2),padding="same"))
model.add(Dropout(0.3))
model.add(Conv2D(filters=128,kernel_size=5,strides=1,padding="same",activation="relu"))
model.add(MaxPool2D(pool_size=(3,2),padding="same"))
model.add(Dropout(0.3))
model.add(Conv2D(filters=256,kernel_size=5,strides=2,padding="same",activation="relu"))
model.add(MaxPool2D(pool_size=(3,2),padding="same"))
model.add(Dropout(0.3))
model.add(Flatten())

model.add(Dropout(0.4))
model.add(Dense(256,activation="relu"))
model.add(Dropout(0.4))
model.add(Dense(64,activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(32,activation="relu"))
model.add(Dense(10,activation="softmax"))
model.summary()
model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["acc"])
#max-acc-baseline기준이상, min-loss-baseline기준이하
cb = tf.keras.callbacks.EarlyStopping(monitor='val_acc',patience=10,verbose=1,mode='max',restore_best_weights=True)
fit_his = model.fit(x_train,y_train,batch_size=100,validation_data=(x_test,y_test),epochs=100,callbacks=[cb])
with open("classification_image.history","wb") as fp:
    pickle.dump(fit_his,fp)
model.save("classification_image.keras")