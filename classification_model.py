import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib as plt
from test_cv2_2 import RemoveBackgroundFolder,SingleRemoveBackground
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPool2D

SEED = 10
# pre_model = Sequential()

#이미지 증강함수
def imageAugment_sub(timg):
    rn = np.random.randint(2,6)
    rn = round(rn/10,1)
    #이미지 밝기
    testimg1 = tf.image.random_brightness(timg, rn)
    # cv.imshow("1",np.array(testimg1))

    # #이미지 무작위 자르기
    # testimg3 = tf.image.random_crop(timg, size=(150,150,3))
    # testimg3 = tf.image.resize(testimg1,(256,256),"nearest",True)
    # cv.imshow("3", np.array(testimg3))

    # #이미지 무작위 좌우반전
    # testimg4 = tf.image.random_flip_left_right(timg)
    # cv.imshow("4", np.array(testimg4))

    # #이미지 무작위 상하반전
    # tf.image.random_flip_up_down(timg)

    # 이미지 무작위 회전
    # layers를 거치면서 float(실수) 즉,소수점으로 바뀜--> rbv는 0~255임 타입을 바꿔줘야 함
    # tf.float32로 계산을 하기에 cv를 할 땐 uint8를 해줘야 이미지가 복원됨
    # 시각적으로 보이기엔 이상했으나 값은 있어서 모델에 넣었어도 이상은 없엇다고 함
    pre_model = tf.keras.layers.RandomRotation(factor=(-0.2,0.3))#(fill_mode='reflect',fill_value=0.0,interpolation='nearest')
    testimg1 = pre_model(testimg1)
    # cv.imshow("6", testimg6.numpy().astype(np.uint8))

    #이미지 무작위 상하좌우 반전
    pre_model = tf.keras.layers.RandomFlip(mode="HORIZONTAL_AND_VERTICAL")
    testimg1 = pre_model(testimg1)
    # cv.imshow("7", testimg7.numpy().astype(np.uint8))

    #이미지 무작위 확대/축소
    pre_model = tf.keras.layers.RandomZoom((-0.15,0.15),(-0.15,0.15))
    testimg1 = pre_model(testimg1)
    return testimg1.numpy().astype(np.uint8)

def ReadImage(rpath):
    cnt = 0
    f_lists = os.listdir(rpath)
    #폴더 내 폴더 불러오기
    for folder in f_lists:
        f_names = os.listdir(rpath+"\\"+folder)
        print(folder,":",end="")
        for f_name in f_names:
            timg = cv.imread(rpath + "\\" + folder +"\\"+ f_name)
            timg = cv.resize(timg,(256,256))
            for ix in range(5):
                arg_img = imageAugment_sub(timg)
                cv.imwrite(rpath + "\\" + folder +"\\"+ str(cnt)+f_name,arg_img)
                cnt+=1 #파일이름 중복 피하기
            print(".",end="")
        print()

ReadImage(r"D:\imgs")#데이터증강호출

np.random.seed(SEED)
tf.random.set_seed(SEED)

