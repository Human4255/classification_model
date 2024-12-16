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
model.evaluate()









