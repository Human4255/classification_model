import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import tensorflow as tf
import cv2 as cv
import numpy as np
import matplotlib as plt
from test_cv2_2 import RemoveBackgroundFolder,SingleRemoveBackground
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPool2D
from sklearn.model_selection import train_test_split

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

def Load_directory_sub(rootpath): #{label:[이미지리스트]}
    f_lists = os.listdir(rootpath)
    print(f_lists)
    y_labels = []
    x_files = []
    for label,fpath in enumerate(f_lists):
        print(".", end="")
        f_name = r"{}\{}".format(rootpath,fpath)
        f_names = os.listdir(f_name)
        #print(f_names)
        for p in f_names:
            y_labels.append(label)
            f_img = cv.imread(r"{}\{}".format(f_name,p))
            f_img = cv.cvtColor(f_img,cv.COLOR_BGR2RGB)
            f_img = cv.resize(f_img,(64,64))
            x_files.append(f_img)

        # print(len(data_sets[label]), end="")
        # print(data_sets[label][0][128][128]) #픽셀값 확인 -> 3채널의 픽셀로 나옴
        # print(type(data_sets.values()))
    return f_lists, np.array(list(y_labels)), np.array(list(x_files))

#훈련,검증데이터 그림그리기
def GetTrainData(dpath):
    label_lists, y_data, x_data = Load_directory_sub(dpath)  # 정답
    print(y_data.shape)  # (3153,)
    print(x_data.shape)  # (3153, 256, 256, 3)
    print(len(label_lists))  # 11
    print(label_lists[0])  # Bear

    # suffle
    x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.2, random_state=10, stratify=y_data)
    print(x_train.shape)  # (2522, 256, 256, 3)
    print(y_train.shape)  # (2522,)
    print(x_test.shape)  # (631, 256, 256, 3)
    print(y_test.shape)  # (631,)
    print(y_train[:10])  # [4 3 0 5 1 4 9 6 9 9]
    return {"label_lists":label_lists,
            "train":(x_train,y_train),
            "test":(x_test,y_test) } #



if __name__ == "__main__": #이게 메인함수라면 ReadImage, 다른파일에서 받을경우 이름으로만 받는대
    ReadImage(r"D:\imgs")#데이터증강호출

np.random.seed(SEED)
tf.random.set_seed(SEED)

