import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import random
import pickle
import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from test_cv2_2 import RemoveBackgroundFolder,SingleRemoveBackground
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from classification_model import Load_directory
from sklearn.model_selection import train_test_split

label_lists, y_data, x_data = Load_directory("D:\\imgs") #정답
print(y_data.shape) #(3153,)
print(x_data.shape) #(3153, 256, 256, 3)
print(len(label_lists)) #11
print(label_lists[0]) #Bear

#suffle
x_train,x_test,y_train,y_test = train_test_split(x_data,y_data,test_size=0.2,random_state=10,stratify=y_data)
print(x_train.shape) #(2522, 256, 256, 3)
print(y_train.shape) #(2522,)
print(x_test.shape) #(631, 256, 256, 3)
print(y_test.shape) #(631,)
print(y_train[:10]) #[4 3 0 5 1 4 9 6 9 9]

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
model.add(MaxPool2D(pool_size=(3,3),padding="same"))
model.add(Dropout(0.2))
model.add(Conv2D(filters=128,kernel_size=5,strides=1,padding="same",activation="relu"))
model.add(MaxPool2D(pool_size=(3,3),padding="same"))
model.add(Dropout(0.2))
model.add(Conv2D(filters=256,kernel_size=5,strides=1,padding="same",activation="relu"))
model.add(MaxPool2D(pool_size=(3,3),padding="same"))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dropout(0.4))
model.add(Dense(256,activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(64,activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(32,activation="relu"))
model.add(Dense(10,activation="softmax"))
model.summary()
model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["acc"])
#max-acc-baseline기준이상, min-loss-baseline기준이하
cb = tf.keras.callbacks.EarlyStopping(monitor='val_acc',patience=20,verbose=1,mode='max',restore_best_weights=True)
fit_his = model.fit(x_train,y_train,batch_size=100,validation_data=(x_test,y_test),epochs=100,callbacks=[cb])
with open("classification_image.history","wb") as fp:
    pickle.dump(fit_his,fp)
model.save("classification_image.keras")