#이미지 처리 + 윤곽선 따는 법 = 전처리부분
import cv2 as cv
import numpy as np
import matplotlib as plt

#원본이미지 가져오기
timg = cv.imread(r"d:\test.jpg",cv.IMREAD_COLOR)
timg = cv.resize(timg,[256,256])
cv.imshow("ori",timg)
#그레이스케일로 바꿔주기
gray_img = cv.cvtColor(timg,cv.COLOR_RGB2GRAY)
gray_img = cv.GaussianBlur(gray_img,(3,3),0)
# cv.imshow("ori_gau",gray_img)

#이진화
g3adapt= cv.adaptiveThreshold(gray_img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY_INV,5,2)
# retval,biimg= (cv.threshold(gray_img,130,255,cv.THRESH_BINARY_INV))
cv.imshow("binary ",g3adapt)

contours,hieracy = cv.findContours(g3adapt,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
#면적이 적은 잡음 제거 - 면적이 1보다 큰 부분만 넣어주기
# print(cv.contourArea(contours[9])) #0.0 0~9까지 0으로 나옴
# print(len(contours)) #269
contours = tuple(contour for contour in contours if cv.contourArea(contour)>0.5)
print(len(contours))
testimg = cv.drawContours(timg.copy(), contours, -1, (0,0,255))
cv.imshow("test", testimg)

#256으로 길이 맞추기
xy_data=[]

for ix in range(256):
    xy_min = [300,300]
    xy_max = [0,0]
    for i, data in enumerate(contours):
        #print(contours[ix][i][0][1]) #y의 위치
        for n, indata in enumerate(data):
            #print(indata[0][1]) #y좌표
            if indata[0][1] == ix:
                if xy_min[0]>indata[0][0]:
                    xy_min = indata[0]
                if xy_max[0]<indata[0][0]:
                    xy_max = indata[0]
    #추출이 안되고 있는곳 처리
    if xy_min[0]==300:
        xy_min=[-1,-1] #왼쪽값
    if xy_max[0]<0:
        xy_max=[300,300]
    xy_data.append([xy_min,xy_max])
print(len(xy_data)) #256
print(xy_data[0])
print(type(xy_data[0]))

"""
이미지가 제대로 캐치되지 않음
부드럽게 선을 따기 위해 가장짧은것 2개를 제외하고 나머지평균을 구해서 평균보다 작으면 길이를 늘려준다.
"""
#마스킹 레이어 안티앨리어싱(계단현상제거)
#타입확인
for xy in xy_data:
    print(type(xy[0]))
#왼쪽
for ix in range(len(xy_data)):
    print(type(xy_data[ix]))
    print(xy_data[ix][0][0]) #[[0,0],[0,0]]
    if xy_data[ix][0][0] == 0:
        continue
    if ix+5>=256:
        break
    # 왼쪽 
    # 위쪽5개
    if xy_data[ix][0][0] <0 or xy_data[ix][1][0]<0: continue
    cur = 0
    cur_1 =xy_data[ix - 1][0][0] if ix >=1 and xy_data[ix - 1][0][0]>=0 else 300 #검사를 통해 값이 없으면 300으로? - 이중에서 가장 작은수치 구하고 있음
    cur_2 =xy_data[ix - 2][0][0] if ix >=2 and xy_data[ix - 2][0][0]>=0 else 300
    cur_3 =xy_data[ix - 3][0][0] if ix >=3 and xy_data[ix - 3][0][0]>=0 else 300
    cur_4 =xy_data[ix - 4][0][0] if ix >=4 and xy_data[ix - 4][0][0]>=0 else 300
    cur_5 =xy_data[ix - 5][0][0] if ix >=5 and xy_data[ix - 5][0][0]>=0 else 300
    if ix==0: print("ix==0:",cur_1)
    #아래5개
    # cur1 = xy_data[ix][0][0]
    # print("======")
    # print(cur1)
    cur1 =xy_data[ix + 1][0][0] if ix <=254 and xy_data[ix + 1][0][0]<0 else 300
    cur2 =xy_data[ix + 2][0][0] if ix <=253 and xy_data[ix + 2][0][0]<0 else 300
    cur3 =xy_data[ix + 3][0][0] if ix <=252 and xy_data[ix + 3][0][0]<0 else 300
    cur4 =xy_data[ix + 4][0][0] if ix <=251 and xy_data[ix + 4][0][0]<0 else 300
    cur5 =xy_data[ix + 5][0][0] if ix <=250 and xy_data[ix + 5][0][0]<0 else 300
    least_low_min = min(cur1,cur2,cur3,cur4,cur5)
    least_top_min = min(cur_1, cur_2, cur_3, cur_4, cur_5)
    if least_low_min<0 or least_top_min<0 or least_low_min>=300 or least_top_min>=300:
        continue
    cur = (least_low_min+least_top_min)//2
    if least_low_min>=300 and least_top_min<300:
        cur = least_top_min
    elif least_top_max>=300 and least_low_max<300:
        cur = least_low_max
    else:
        cur = (least_low_max + least_top_max) // 2
    if ix == 5: print(cur_1, ":", cur_2, ":", cur_3, ":", cur_4, ":", cur_5)
    if least_low_min >=300: # 값이 없으면 좌표를 0으로
        cur=0
    if ix==13: print(cur,":")

    xy_data[ix][0][0]=cur
    #오른쪽
    #위쪽5개
    if xy_data[ix][0][0] == 0 or xy_data[ix][1][0] == 0: continue
    cur = 0
    cur_1 =xy_data[ix - 1][1][0] if ix >=1 and xy_data[ix - 1][1][0]<300 else -1 #검사를 통해 값이 없으면 300으로? - 이중에서 가장 작은수치 구하고 있음
    cur_2 =xy_data[ix - 2][1][0] if ix >=2 and xy_data[ix - 2][1][0]<300 else -1
    cur_3 =xy_data[ix - 3][1][0] if ix >=3 and xy_data[ix - 3][1][0]<300 else -1
    cur_4 =xy_data[ix - 4][1][0] if ix >=4 and xy_data[ix - 4][1][0]<300 else -1
    cur_5 =xy_data[ix - 5][1][0] if ix >=5 and xy_data[ix - 5][1][0]<300 else -1
    #아래5개
    cur1 =xy_data[ix + 1][1][0] if ix <=254 and xy_data[ix + 1][1][0]<300 else -1
    cur2 =xy_data[ix + 2][1][0] if ix <=253 and xy_data[ix + 2][1][0]<300 else -1
    cur3 =xy_data[ix + 3][1][0] if ix <=252 and xy_data[ix + 3][1][0]<300 else -1
    cur4 =xy_data[ix + 4][1][0] if ix <=251 and xy_data[ix + 4][1][0]<300 else -1
    cur5 =xy_data[ix + 5][1][0] if ix <=250 and xy_data[ix + 5][1][0]<300 else -1
    least_low_max = max(cur1,cur2,cur3,cur4,cur5)
    least_top_max = max(cur_1, cur_2, cur_3, cur_4, cur_5)
    if least_low_max<0 and least_top_max>=0:
        cur = least_top_max
    elif least_top_max<0 and least_low_max>=0:
        cur = least_low_max
    else:
        cur = (least_low_max+least_top_max)//2
    if ix==13: print(cur,"::",ix)
    xy_data[ix][1][0]=cur

for ix in range(len(xy_data)):
    print(type(xy_data[ix]))
    print(xy_data[ix][0][0]) #[[0,0],[0,0]]
    if xy_data[ix][0][0] == 0:
        continue
    if ix+5>=256:
        break
    # 왼쪽
    # 위쪽5개
    if xy_data[ix][0][0] <0 or xy_data[ix][1][0]<0: continue
    cur = 0
    cur_1 =xy_data[ix - 1][0][0] if ix >=1 and xy_data[ix - 1][0][0]>=0 else 300 #검사를 통해 값이 없으면 300으로? - 이중에서 가장 작은수치 구하고 있음
    cur_2 =xy_data[ix - 2][0][0] if ix >=2 and xy_data[ix - 2][0][0]>=0 else 300
    cur_3 =xy_data[ix - 3][0][0] if ix >=3 and xy_data[ix - 3][0][0]>=0 else 300
    cur_4 =xy_data[ix - 4][0][0] if ix >=4 and xy_data[ix - 4][0][0]>=0 else 300
    cur_5 =xy_data[ix - 5][0][0] if ix >=5 and xy_data[ix - 5][0][0]>=0 else 300
    if ix==0: print("ix==0:",cur_1)
    #아래5개
    # cur1 = xy_data[ix][0][0]
    # print("======")
    # print(cur1)
    cur1 =xy_data[ix + 1][0][0] if ix <=254 and xy_data[ix + 1][0][0]<0 else 300
    cur2 =xy_data[ix + 2][0][0] if ix <=253 and xy_data[ix + 2][0][0]<0 else 300
    cur3 =xy_data[ix + 3][0][0] if ix <=252 and xy_data[ix + 3][0][0]<0 else 300
    cur4 =xy_data[ix + 4][0][0] if ix <=251 and xy_data[ix + 4][0][0]<0 else 300
    cur5 =xy_data[ix + 5][0][0] if ix <=250 and xy_data[ix + 5][0][0]<0 else 300
    least_low_min = min(cur1,cur2,cur3,cur4,cur5)
    least_top_min = min(cur_1, cur_2, cur_3, cur_4, cur_5)
    if least_low_min<0 or least_top_min<0 or least_low_min>=300 or least_top_min>=300:
        continue
    cur = (least_low_min+least_top_min)//2
    if least_low_min>=300 and least_top_min<300:
        cur = least_top_min
    elif least_top_max>=300 and least_low_max<300:
        cur = least_low_max
    else:
        cur = (least_low_max + least_top_max) // 2
    if ix == 5: print(cur_1, ":", cur_2, ":", cur_3, ":", cur_4, ":", cur_5)
    if least_low_min >=300: # 값이 없으면 좌표를 0으로
        cur=0
    if ix==13: print(cur,":")

    xy_data[ix][0][0]=cur
    #오른쪽
    #위쪽5개
    if xy_data[ix][0][0] == 0 or xy_data[ix][1][0] == 0: continue
    cur = 0
    cur_1 =xy_data[ix - 1][1][0] if ix >=1 and xy_data[ix - 1][1][0]<300 else -1 #검사를 통해 값이 없으면 300으로? - 이중에서 가장 작은수치 구하고 있음
    cur_2 =xy_data[ix - 2][1][0] if ix >=2 and xy_data[ix - 2][1][0]<300 else -1
    cur_3 =xy_data[ix - 3][1][0] if ix >=3 and xy_data[ix - 3][1][0]<300 else -1
    cur_4 =xy_data[ix - 4][1][0] if ix >=4 and xy_data[ix - 4][1][0]<300 else -1
    cur_5 =xy_data[ix - 5][1][0] if ix >=5 and xy_data[ix - 5][1][0]<300 else -1
    #아래5개
    cur1 =xy_data[ix + 1][1][0] if ix <=254 and xy_data[ix + 1][1][0]<300 else -1
    cur2 =xy_data[ix + 2][1][0] if ix <=253 and xy_data[ix + 2][1][0]<300 else -1
    cur3 =xy_data[ix + 3][1][0] if ix <=252 and xy_data[ix + 3][1][0]<300 else -1
    cur4 =xy_data[ix + 4][1][0] if ix <=251 and xy_data[ix + 4][1][0]<300 else -1
    cur5 =xy_data[ix + 5][1][0] if ix <=250 and xy_data[ix + 5][1][0]<300 else -1
    least_low_max = max(cur1,cur2,cur3,cur4,cur5)
    least_top_max = max(cur_1, cur_2, cur_3, cur_4, cur_5)
    if least_low_max<0 and least_top_max>=0:
        cur = least_top_max
    elif least_top_max<0 and least_low_max>=0:
        cur = least_low_max
    else:
        cur = (least_low_max+least_top_max)//2
    if ix==13: print(cur,"::",ix)
    xy_data[ix][1][0]=cur

xy_data=np.array(xy_data)
xy_data = xy_data.reshape(256,1,2,2)
extract_img = cv.drawContours(timg.copy(), xy_data, -1, (0, 0, 255))
cv.imshow("ext",extract_img)

print("===========")
cnt=0
new_img = np.zeros((timg.shape))+0
for ix, valarr in enumerate(timg):
    for iy,val in enumerate(timg[ix]): #ix=x좌표
        if xy_data[ix,0,0,0]<=iy and xy_data[ix,0,1,0]>=iy and xy_data[ix,0,0,1]==ix: #[[125 111][131 111]] 이런형태 iy=y좌표
            cnt+=1
            new_img[ix,iy]=timg[ix,iy] #125 131 사이에 있는 숫자가 들어가진다.
print(new_img.shape)#(256, 256, 3)
new_img = new_img.astype(np.uint8)
cv.imshow("last_data",new_img)


# xy_data_first = xy_data[:,0,0,:]
# xy_data_second = (xy_data[:,0,1])
# #print(xy_data_second.shape) #(256, 2)
# pts = np.concatenate((xy_data_first,xy_data_second))
# print(np.shape(pts))  # pts의 차원을 확인->(512,)
# pts = pts.reshape(-1, 1, 2)  # (512,) -> (256,1, 2) 형태로 변경
# print(pts.shape)#(256, 2)
# extrac_img = cv.drawContours(timg.copy(),pts,-1,(0,0,255))
# cv.imshow("a",extrac_img)
#
# sorted_contoure = sorted(contours,key=cv.contourArea,reverse=True)
# contour = sorted_contoure[i]
# epsilon = 0.01*cv.arcLength(contour,True)
# approx = cv.approxPolyDP(contour, epsilon, True)
# testimg = cv.drawContours(timg,[approx],-1,(0,0,255))
# #testimg = cv.approxPolyDP(contour, epsilon, True)
# cv.imshow("gray2",testimg)

cv.waitKey(0)
cv.destroyAllWindows()

#이건 안 하는걸로, 이것도 있다고 이해하기
#cv.polylines()
