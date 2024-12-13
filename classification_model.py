import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib as plt
from test_cv2_2 import RemoveBackgroundFolder,SingleRemoveBackground

from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Conv2D
