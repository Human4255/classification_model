from Preprocessing.remove_Background import RemoveBackgroundFolder,SingleRemoveBackground
from Preprocessing.Utill import ReadImage
#numpy설치 오류시, 패키지 파일에서 찾아 제거, rembg는 numpy랑 버전이 동일해야한다.

#배경제거호출
userSel = input("배경을 제거 할 대상을 선택하시오\n"
              " ->단일 제거 시 1을 눌러주세요\n"
              " ->여러파일 제거 시 아무키나 눌러주세요\n"
               " ->배경제거를 수행하지 않는다면 0을 눌러주세요\n"
                "입력: ")
if userSel!='0':
    if userSel == '1':
        print(":::::::::::::::::::::::::::::::")
        imagePathName = input("배경을 제거 할 파일 경로를 적어주세요(파일명과 확장자명까지 입력해주세요)\n"
                              " ex) d:\\img\\myimg.jpg\n"
                              "입력: ")
        SingleRemoveBackground(r"{}".format(imagePathName))
    else:
        print(":::::::::::::::::::::::::::::::")
        imagePathName =  input("배경을 제거 할 디렉터리 경로를 적어주세요\n"
                              "(해당경로에는 하위 디렉터리가 존재해야 합니다)\n"
                              " ex) d:\\imgs\\Tiger\\mytigimg.jpg\n"
                               "입력: ")
        RemoveBackgroundFolder(r"{}".format(imagePathName))

#이미지증강호출
while(1):
    userSel = input("이미지 증강 전처리를 수행할까요?\n"
                    " ->(y/n) ")
    if userSel =='n':
        break
    if userSel =='y':
        imgAug = input("수행 실행 시 디렉터리 경로와 증강수량을 콤마로 구분하여 넣어주세요\n"
                       " ex) d:/svimg,2\n"
                       "입력: ")
        prolist = imgAug.split(",")
        if len(prolist)<2:
            print("경로와 수량을 콤바로 구분하여 정확히 입력해주세요\n"
                  "입력: ")
            print("::::::::::::::::::::::::::::::::::::")
            continue
        #해당 경로가 존재하는지, 수량이 숫자로 바뀌나? - 일단은 성공만 보고 점검할 때 확인
        ReadImage(r"{}".format(prolist[0]),int(prolist[1]))
        break
    else:
        print("입력이 잘못됐어요")
        print("::::::::::::::::::::::::::::::::::::")
        continue
