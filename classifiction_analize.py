import os

import seaborn

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
from classification_model import GetTrainData
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from seaborn import heatmap

data_sets = GetTrainData(r"D:\imgs")
label_lists = data_sets["label_lists"]
x_train,y_train = data_sets["train"]
x_test,y_test = data_sets["test"]
#원핫인코딩 다시하기
y_test = tf.one_hot(y_test,10)

with open("classification_image.history","rb") as fp:
    fit_his = pickle.load(fp)
print(fit_his.history.keys())

#모델 그려보기
plt.subplot(1,2,1)
plt.plot(fit_his.history["acc"],label="Train Acc")
plt.plot(fit_his.history["val_acc"],label="Valid Acc")
plt.title("ACCURACY")
plt.legend()
plt.subplot(1,2,2)
plt.plot(fit_his.history["loss"],label="Train Loss")
plt.plot(fit_his.history["val_loss"],label="Valid Loss")
plt.title("Loss")
plt.legend()
plt.show()

#모델평가
model=tf.keras.models.load_model("classification_image.keras")
loss,acc = model.evaluate(x_test,y_test)
print("손실값:",loss,"::  정확도:",acc)
y_pred = model.predict(x_test)
rindex = [random.randint(0,len(x_test)) for ix in range(10)] #랜덤하게 10개 뽑아서 인덱스로 활용
for i in range(len(rindex)):
    plt.subplot(2,5,i+1)
    plt.imshow(x_test[rindex[i]])
    plt.title(label_lists[np.argmax(y_test[rindex[i]])])
    plt.xlabel(f"predict: {label_lists[np.argmax(y_pred[rindex[i]])]}")
    plt.xticks([]);plt.yticks([])
plt.show()

#혼돈행렬
y_conv_true = np.array([np.argmax(ll) for ll in y_test])
y_conv_pred = np.array([np.argmax(ll) for ll in y_pred])
print(y_conv_true)
print(y_conv_pred)
print(y_conv_true[1:10])
print(y_conv_pred[1:10])
# confusion_matrix()

#히트맵-혼돈행렬넣어주기
# seaborn.heatmap()




