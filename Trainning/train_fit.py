from Preprocessing.Utill import GetTrainData
from Trainning.construct_model import Train_fit_run
label_lists = x_train = x_test = y_train = y_test = None
#훈련파일생성호출
userSel = input("디렉터리에서 훈련파일을 생성하여 가져오겠습니까? 취소하시려면 0를 눌러주세요\n"
                " ->아래와 같은 형태로 디렉터리명을 입력하세요.\n"
                " ->tiger, Rabbit, Bear는 정답파일의 이름 리스트입니다. \n"
                " ->ex) d:\\img\\tiger.jpg, d:\\img\\Rabbit.jpg, d:\\img\\Bear.jpg\n"
                "입력: ")

if userSel !='0':
    data_sets = GetTrainData(r"{}".format(userSel))

    label_lists = data_sets["label_lists"]
    x_train,y_train = data_sets["train"]
    x_test,y_test = data_sets["test"]
    print("x_train(",len(x_train),")", "y_train(",len(y_train),")")
    print("x_test(", len(x_test), ")", "y_test(", len(y_test), ")")
    user_Sel = input("   훈련횟수를 입력하면 최적의 검증데이터 정확도에 맞춰 조기종료됩니다.\n"
            "   classification_image.history 파일로 훈련과정이 저장되며,\n"
            "   classification_imge.keras 파일로 훈련 모델이 저장됩니다.\n"
            " (훈련을 진행하지 않을거면 0을 입력해주세요)\n"
            "입력: ")
    if user_Sel!='0' and len(x_train)>0 and len(y_train)>0 and len(x_test)>0 and len(y_test)>0:
        input("엔터키를 누르면 10개의 이미지를 확인합니다. 정답과 일치하는지 확인하세요\n"
                "창을 닫으면 훈련이 시작됩니다.")
        print("훈련을 시작합니다...")
        Train_fit_run(int(user_Sel), label_lists, x_train, y_train, x_test, y_test)
    elif user_Sel=='0':
        print("훈련을 건너뛰고 종료합니다.")
        exit()

elif userSel=='0':
    exit()


