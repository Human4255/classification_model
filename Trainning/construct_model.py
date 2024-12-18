import os
os.environ['TF_ENABLE_ONEDNN_OPTS']='0'
import numpy as np
import random
import pickle
import seaborn
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import Sequential, Input
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPool2D, Flatten
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import confusion_matrix, classification_report
from seaborn import heatmap

# image confirm
def Train_fit_run(train_count,label_lists,x_train,y_train,x_test,y_test):
    rlist = [random.randint(0,len(x_train)-1) for _ in range(10)]
    print(rlist)
    for ix,num in enumerate(rlist):
        plt.subplot(2,5,ix+1)
        plt.imshow(x_train[ix])
        plt.title(label_lists[np.argmax(y_train[ix])])
        plt.xticks([])
        plt.yticks([])
    plt.show()
    print(type(y_train))

    #onehot encoding
    y_train = tf.cast(y_train, tf.int32)
    y_test = tf.cast(y_test, tf.int32)
    y_train = tf.one_hot(y_train,10)
    y_test = tf.one_hot(y_test,10)
    print(y_train.shape)
    print(y_test.shape)
    print(y_train[0])

    #model config
    model = Sequential()
    model.add(Input(shape=(64,64,3)))
    model.add(Conv2D(filters=64,kernel_size=5,strides=2,padding="same",activation="relu"))
    model.add(MaxPool2D(pool_size=(3,2),padding="same"))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=128,kernel_size=5,strides=1,padding="same",activation="relu"))
    model.add(MaxPool2D(pool_size=(3,2),padding="same"))
    model.add(Dropout(0.3))
    model.add(Conv2D(filters=256,kernel_size=5,strides=1,padding="same",activation="relu"))
    model.add(MaxPool2D(pool_size=(3,2),padding="same"))
    model.add(Dropout(0.3))
    model.add(Flatten())
    model.add(Dropout(0.2))
    model.add(Dense(256,activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(128,activation="relu"))
    model.add(Dropout(0.3))
    model.add(Dense(32,activation="relu"))
    model.add(Dense(10,activation="softmax"))
    model.summary()
    optimizer = Adam(learning_rate=0.0001) #과대적합이 보여 learning_rate조절
    model.compile(optimizer=optimizer,loss="categorical_crossentropy",metrics=["acc"])
    #max-acc-baseline기준이상, min-loss-baseline기준이하
    cb = tf.keras.callbacks.EarlyStopping(monitor='val_acc',patience=10,verbose=1,mode='max',restore_best_weights=True)
    fit_his = model.fit(x_train,y_train,batch_size=100,validation_data=(x_test,y_test),epochs=train_count,callbacks=[cb])
    with open("../classification_image.history", "wb") as fp:
        pickle.dump(fit_his,fp)
    model.save("classification_image.keras")

    input("훈련 종료! 모델과 결과 저장이 완료되었습니다.\n"
          "엔터키를 눌러 손실도와 정확도를 확인하세요")
    losses,acces = model.evaluate(x_test,y_test)
    print("손실도:",losses," ::: ","정확률:","{:.2f}",format(acces*100),"%")

    input("엔터키를 눌러 훈련 결과, 손실도, 정확도 그래프 시각화를 확인하세요")
    plt.subplot(1, 2, 1)
    plt.plot(fit_his.history["acc"], label="Train Acc")
    plt.plot(fit_his.history["val_acc"], label="Valid Acc")
    plt.title("ACCURACY")
    plt.legend()
    plt.subplot(1, 2, 2)
    plt.plot(fit_his.history["loss"], label="Train Loss")
    plt.plot(fit_his.history["val_loss"], label="Valid Loss")
    plt.title("Loss")
    plt.legend()
    plt.show()

    # 모델평가
    input("시각화 창을 닫고 엔터키를 눌러주세요, 테스트파일 예측을 시각화하겠습니다.")
    y_pred = model.predict(x_test)
    rindex = [random.randint(0, len(x_test)) for ix in range(10)]  # 랜덤하게 10개 뽑아서 인덱스로 활용
    for i in range(len(rindex)):
        plt.subplot(2, 5, i + 1)
        plt.imshow(x_test[rindex[i]])
        plt.title(label_lists[np.argmax(y_test[rindex[i]])])
        plt.xlabel(f"predict: {label_lists[np.argmax(y_pred[rindex[i]])]}")
        plt.xticks([]);plt.yticks([])
    plt.show()

    #혼돈행렬 확인
    input("엔터키를 눌러주세요, 혼동행렬을 작성하여 시각화하겠습니다.")
    y_conv_true = np.array([label_lists[np.argmax(ll)] for ll in y_test])
    y_conv_pred = np.array([label_lists[np.argmax(ll)] for ll in y_pred])
    print(y_conv_true)
    print(y_conv_pred)
    print(y_conv_true[1:10])
    print(y_conv_pred[1:10])
    cm = confusion_matrix(y_conv_true, y_conv_pred)

    input("창을 닫고 엔터키를 눌러주세요, 최종훈련결과 리포트를 출력하겠습니다.")
    print(classification_report(y_conv_true,y_conv_pred))
    # 히트맵-혼돈행렬넣어주기
    seaborn.heatmap(cm, cmap="Blues", annot=True, fmt=".1f", xticklabels=label_lists, yticklabels=label_lists)
    plt.show()