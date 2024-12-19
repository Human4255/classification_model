"""
비디오프레임제거
cv.bgsegm.createBackgroundSubtractor
cv.bgsegm.createBackgroundSubtractorMOG()
ex) fgbg = cv.bgsegm.createBackgroundSubtractorMOG().apply(timg)
    cv2.imshow("test", fgbg)

https://github.com/xuebinqin/U-2-Net : 또다른 배경제거 오픈소스
"""
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot  as plt
from rembg import remove

def RemoveBackgroundFolder(rpath): #여러개 제거
    #폴더 불러오기
    #rpath = r"D:\imgs"
    f_lists = os.listdir(rpath)
    print(f_lists)
    #폴더 내 폴더 불러오기
    for folder in f_lists:
        f_names = os.listdir(rpath+"\\"+folder)
        print(folder,":",end="")
        for f_name in f_names:
            timg = cv.imread(rpath + "\\" + folder +"\\"+ f_name)
            timg = cv.resize(timg,(256,256))
            # cv.imshow("origin "+f_name,timg)
            rmbg_img = remove(timg)
            cv.imwrite(rpath + "\\" + folder +"\\"+ f_name,rmbg_img)
            #libpng warning: iCCP: known incorrect sRGB profile : PNG파일을 처리할 때 나타나는 오류래
            # cv.imshow("remimg ",rmbg_img)
            # cv.waitKey(0)
            # cv.destroyAllWindows()
            print(".",end="")
        print()
    print("모든파일의 배경제거가 완료되었습니다.")

def SingleRemoveBackground(imagePathName): #단일제거
    timg = cv.imread(imagePathName)
    timg = cv.resize(timg, (256, 256))
    rmbg_img = remove(timg)
    #cv.imwrite(imagePathName,rmbg_img)
    print("배경이미지 제거가 완료되었씁니다.")
    return rmbg_img

if __name__ == "__main__": #이게 메인함수라면 ReadImage, 다른파일에서 받을경우 이름으로만 받는대
    print("preprocessing_running 파일에서 실행하세요")
else:
    pass #다른 파일에서 import 시 작동되는 코드