describe : 웹크롤링을 이용해 원하는 이미지를 수집하고 전처리 후 CNNㅁ델을 구성하여 훈련 과정의 전체           

r"D:\imgs": 디렉터리 내의 폴더명은 정답으로 처리, 각 관련 이미지가 내부에 존재해야 한다.           

opencv0.y: def RemoveBackground 디렉터리 내의 모든 이미지 백그라운드 제거 및 이미지 256*256으로 리사이징           
           def SingleRemoveBackground 단일 이미지에 대한 256*256으로 리사이징           

classification_model.py : def imageAugment_sub 디렉터리 내의 이미지를 무작위로 밝기, 회전, 상하좌우 반전, 확대/축소 시켜 이미지를 증강시킴                      
                          def ReadImage 디렉터리 내의 이미지를 불러와 증강함수(imageAugment_sub)를 호출하여 이미지를 저장함           
                          def Load_directory_sub 증강된 이미지를 읽어 {label:[이미지리스트]}형태로 변환, 64*64으로 리사이징, 정답리스트, y_label리스트로 저장           
                          def GetTrainData Load_directory_sub함수를 호출하여 정답파일을 기준으로 훈련데이터(80%), 테스트데이터(20%)를 랜덤하게 분리           
                       
construct_model.py : 훈련데이터의 minmax표준화, 정답데이터의 원핫인코딩을 수행후, 이미지와 정답파일의 매칭을 확인           
                     Sequential모델로 구성된 CNN을 구현하고(다중분류) 훈련을 실행+조기종료 콜백함수 추가 후 훈련결과와 모델을 파일로 저장           
                    +) max-acc-baseline기준이상, min-loss-baseline기준이하           

classfication_analize.py : 테스트데이터와 테스트정답파일을 로딩한 후 훈련이 완료된 모델과 훈련결과를 로딩하여           
                           훈련모델의 예측값을 출력해 실제 정답과 이미지와 예측정답을 시각화표현 -matplotlib.pyplot사용           
                           혼돈행렬 진행 후 히트맵을 그려줌           
