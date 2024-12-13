#이미지 처리 + 윤곽선 따는 법 = 전처리부분
import cv2 as cv
import numpy as np


timg = cv.imread(r"d:\test.jpg",cv.IMREAD_COLOR)

timg = cv.resize(timg,[256,256])
cv.imshow("orig",timg)
#
# bimg = cv.blur(timg,(3,3))
# cv.imshow("blur",bimg)
#
# gimg1 = cv.GaussianBlur(timg,(3,3),0.1)
# cv.imshow("gauss1"
#           "",gimg1)
#
# gimg2 = cv.GaussianBlur(timg,(3,3),0.5)
# cv.imshow("gauss2",gimg2)
#
gimg3 = cv.bilateralFilter(timg,9,75,75)
#cv.imshow("bilar3",gimg3)

# #경계임계값 - 그레이스케일 변경, 단순한 건 이걸로 빼는게 낫다.
gimg3_gray = cv.cvtColor(gimg3,cv.COLOR_BGR2GRAY)
retval, gimg4 = cv.threshold(gimg3_gray,127,255,cv.THRESH_BINARY)
# cv.imshow("thres", gimg4 )
# print(gimg3_gray) #좌표가 숫자출력
#
gimg5 = cv.adaptiveThreshold(gimg3_gray,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,15,2)
# cv.imshow("adaptthres1_mean", gimg5)
#
gimg6 = cv.adaptiveThreshold(gimg3_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,15,2)
cv.imshow("adaptthres2_gauss", gimg6)
#
# #otsu
retval, gimg7 = cv.threshold(gimg3_gray,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
# cv.imshow("otsu", gimg7)

#fillter
## g_flatten = gimg7.flatten()
## gmask = g_flatten>=255 #255보다 크면 True, 255보다 작으면 False
## i_flatten = gimg3_gray.flatten() #그레이 이미지를 평탄화
## ix_np = np.where(gmask) #True의 인덱스 위치값을 반환
## i_flatten[ix_np]=255 #해당 위치의 값을 설정-0은 검정색, 255는 흰색
## cvtimg = i_flatten.reshape(256,256) #원본이미지 사이즈와 동일한 사이즈로 맞춰줌, 이미지모양으로변경
# mask = np.where(gimg7>=255)
# timg[mask]=255
# cv.imshow("fillterimg2",timg)

"""
<이미지추출단계>
1. 이미지 불러오기
2. 블러처리로 노이즈제거
3. 그레이스케일로 컬러를 변경
4. 이미지 이진화 처리 ex) adaptthreshold,threshold,... 
5. 이미지 경계값 출력
6. 이미지 경계선 그리기
7. 경계선 안쪽 이미지 추출
"""
# contours, hierarchy = cv.findContours(gimg6,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
# print(contours[0]) #[[[ 89 192]]] ->x,y좌표
# print(hierarchy.shape)
# print(len(contours))
# cont_img = cv.drawContours(timg.copy(),contours,-1,(0,0,255),1) #BGR튜플형태
# cv.imshow("contour img",cont_img)


contours, hierarchy = cv.findContours(gimg6,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#CHAIN_APPROX_SIMPLE이 원래 4개의 점만 나와야하는데, 그렇지 않아 무식하게 루프로 빼냄
#튜플내부의 넘파이배열의 크기가 다 달라서 반복문으로 빼내기
max_x=0; min_x=300;max_y=0; min_y=300
for contour in contours:
    for con in contour:
        if max_x < con[0][0]:
            max_x = con[0][0]
        elif min_x > con[0][0]:
            min_x = con[0][0]
        if max_y < con[0][1]:
            max_y = con[0][1]
        elif min_y > con[0][1]:
            min_y = con[0][1]
print(max_x)
print(min_x)
print(max_y)
print(min_y)
print(len(contours))
print(type(contours))
print(contours[0].shape)
min_data = np.array([[[min_x,min_y]]])
max_data = np.array([[[max_x,max_y]]])
contours_rect = (min_data,max_data) #직접 만든 외곽선 데이터
res_rect = [cv.boundingRect(cont) for cont in contours_rect]
print(res_rect)

#print(type(contours)) #튜플
# print(contours[:5])
# #print(contours[0][0])
# print(type(contours[0])) #넘파이
# print(contours[0])
# print(contours[0][0][0][0])
# print(contours[0][:,:,0])
# print(contours[0][:,:,1])
#max(iterable, *, key=None)에서 key에 람다식이 들어갈 수 있음
max(contours, key=lambda x:x[0][0][0])
cnt_img2 = cv.rectangle(timg.copy(),(min_x,min_y),(max_x,max_y),(0,0,255),1)
# cont_img2 = cv.drawContours(timg.copy(),res_rect,-1,(0,0,255),1) #BGR튜플형태
cv.imshow("contour img2",cnt_img2)

print(timg.shape) #(256, 256, 3)
new_img = np.zeros((timg.shape))+0 #255-흰색
#new_img = np.zeros((timg.shape))*255
print(new_img.shape) #(256, 256, 3)
for ix,xele in enumerate(timg):
    for iy,yele in enumerate(xele):
        #if iy==0: print(yele.shape)
        if ix>min_x and ix < max_x and min_y<iy and max_y>iy: #이미지안쪽
            new_img[ix,iy] = yele

new_img = new_img.astype(np.uint8)
print(new_img[128,128])
print(timg[128,128])

cv.imshow("ori",timg)
cv.imshow("new_img",new_img)

cv.waitKey(0)
cv.destroyAllWindows()

