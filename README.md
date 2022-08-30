# Submission-Robotics-IOT
Submission in "Class: Robotics IOT"
# FINGER CALC
　mediapipeの指認識機能及びMaker Nanoを組み合わせて一桁と一桁の和・積を行うアプリケーション
 ![image](https://user-images.githubusercontent.com/70005022/187378290-650a5be6-89dd-4a1a-a9a9-c14b42d8d576.png)
# システム環境
- Python (3.8)
  - pyfirmata
  - tensorflow
  - opencv-python
  - mediapipe
- Maker Nano (Arduino 1.8.19)
  - exsample>Firmata>StandardFirmata を利用
# システム構成図
![image](https://user-images.githubusercontent.com/70005022/187378348-3e83b284-c83f-46a7-9319-f89fb1beb197.png)
# 指認識機能
 mediapipeのhand認識機能を用いて各指の座標を取得し、それらから各指の開閉を取得する。  
 指の状態は5本*2パターンの計32通り存在する。  
 例  
 ![image](https://user-images.githubusercontent.com/70005022/187379411-70400412-26d9-419b-984a-68a7ad2e5805.png)
# 数字変換機能
　取得した手の状態のうち9つを数字と紐付けて数を取得する。  
 それぞれの状態における数は下記の通りである。  
 ![image](https://user-images.githubusercontent.com/70005022/187379731-ddf7d1ac-5f3e-4491-8f26-735550f66c8f.png)
# 確定機能
 誤入力防止のため、該当の数字および選択を50フレームキープしていると入力として判断する機能。
# 選択機能
　設置した四角形においてその座標内に右手の人差し指がある場合、ハイライトを施し該当の四角形を選択する機能。  
 和積の計算及び、計算を再度行う際のResetボタンに利用している。  
![image](https://user-images.githubusercontent.com/70005022/187380015-5fcd7816-ca7b-4c91-8712-59b8ae9aae50.png)
# 計算機能
　入力した数式を計算する機能
# 2進数変換機能
　計算した結果を二進数に変換する機能
# Maker Nano表示機能
　変換した２進数を用いて、StandardFirmataを適用させたMaker NanoのLEDを光らせることで解の数字を２進数として表示させている
#　工夫した点
- 確定機能を用いて誤入力防止に務めた
- 選択機能において選択している事を明示している
- リセットすることをアプリ内で可能にした点
