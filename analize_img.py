#이미지 확인하고 지우는 작업
import os
import cv2 as cv

path = r"d:\imgs"
list_dirs = os.listdir(path)
for directory in list_dirs:
    img_file_lists = os.listdir(path+"\\"+directory)
    for img in img_file_lists:
        #파일인지 검사 - 폴더면 안되니까
        #isdir-디렉터리검사, isfile-파일검사 --> print(os.path.isfile(path+"\\"+directory+"\\"+img))
        if os.path.isfile(path + "\\" + directory + "\\" + img):
            img_mat = cv.imread(path + "\\" + directory + "\\" + img, cv.IMREAD_COLOR)
            img_mat = cv.resize(img_mat,[256,256],img_mat, interpolation=cv.INTER_AREA)
            cv.imshow(img+":delete is press d", img_mat)
            key = cv.waitKey(0)
            #print(key)
            cv.destroyAllWindows() #키보드 키를 누르면 몇 번인지 알려줌 enter-13, d-100
            if key==100:
                os.remove(path+"\\"+directory+"\\"+img)
