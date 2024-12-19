import os
import cv2 as cv
import numpy as np
import pickle
import matplotlib.pyplot as plt
from Preprocessing.remove_Background import SingleRemoveBackground
from Preprocessing.Utill import getPred_processing
from tensorflow.keras.models import load_model
from Preprocessing.Utill import SaveConfig

# ROOTPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# label_list = os.listdir(r"d:/imgs")
curpath = os.path.dirname(os.path.abspath(__file__))
path_list = curpath.split("\\")[:-1]
rootpath = "\\".join(path_list)
# SaveConfig(label_list,rootpath)
with open(f"{rootpath}\\config","rb") as fp:
    label_list = pickle.load(fp)
print("라벨리스트확인:",label_list)
sample_data = input("라벨리스트가 불러와 졌는지 확인후\n"
                    "샘플데이터의 파일경로와 파일명을 지정해주세요\n")

origin_img = cv.imread(sample_data,cv.COLOR_BGR2RGB)
origin_img = cv.resize(origin_img,(256,256))
rembg_img = SingleRemoveBackground(r"{}".format(sample_data))
rembg_img = getPred_processing(rembg_img)
rembg_img = np.array([rembg_img])

print(rembg_img.shape)
print(rembg_img[0][32][32])

# rembg_img = (rembg_img*255).astype(np.uint8)
# cv.imshow("sample_img",rembg_img)
# cv.waitKey(0)
# cv.destroyAllWindows()

#모델로딩
model = load_model(f"{rootpath}\\Trainning\\classification_image.keras")
model.summary()
print(model.input_shape)  #(None, 64, 64, 3)
y_pred = model.predict(rembg_img)
#모델그리기
plt.imshow(origin_img)
plt.xlabel("pred:"+label_list[np.argmax(y_pred)])
plt.xticks([]); plt.yticks([])
plt.show()