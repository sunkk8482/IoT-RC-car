import cv2
import mediapipe as mp
import numpy as np
import mysql.connector
import datetime
from firebase import firebase
from datetime import datetime
import time
import pytz


max_num_hands = 1
gesture = {
    0: 'fist', 1: 'right', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'left', 7: 'rock', 8: 'spiderman', 9: 'yeah', 10: 'ok', 11: 'back'
}
rps_gesture = {0: 'go', 5: 'stop', 6: 'left', 1: 'right', 8: 'mid', 11:'back'}  # 우리가 사용할 제스처 라벨만 가져옴

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=max_num_hands,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# 제스처 인식 모델
file = np.genfromtxt('gesture_train_fy.csv', delimiter=',')
angle = file[:, :-1].astype(np.float32)
label = file[:, -1].astype(np.float32)
knn = cv2.ml.KNearest_create()
knn.train(angle, cv2.ml.ROW_SAMPLE, label)

cap = cv2.VideoCapture(0)

db = mysql.connector.connect(host='3.39.234.126', user='mincoding', password='1234', database='minDB',
                             auth_plugin='mysql_native_password')
cur = db.cursor()

prev_gesture = None
prev_gesture_time = datetime.now()
query_sent = False  # 쿼리를 보냈는지 여부를 추적하는 변수


korea_timezone = pytz.timezone("Asia/Seoul")
# Project Host URL
firebase_url = "https://kfcproject-cf35a-default-rtdb.firebaseio.com/"
firebase = firebase.FirebaseApplication(firebase_url, None)



def insertCommand(cmd_string, arg_string):
    time = datetime.now()
    is_finish = 0

    query = "insert into command(time, cmd_string, arg_string, is_finish) values (%s, %s, %s, %s)"
    value = (time, cmd_string, arg_string, is_finish)

    cur.execute(query, value)
    db.commit()

    # Sending data to Firebase
    current_time = datetime.now(korea_timezone)
    time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    commandData = {
        "cmd_string": cmd_string,
        "arg_string": arg_string,
        "is_finish": is_finish
    }
    firebase.put("/commandTable", time_str, commandData)

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        continue

    img = cv2.flip(img, 1)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    result = hands.process(img)

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks is not None:
        for res in result.multi_hand_landmarks:
            joint = np.zeros((21, 3))
            for j, lm in enumerate(res.landmark):
                joint[j] = [lm.x, lm.y, lm.z]

            v1 = joint[[0, 1, 2, 3, 0, 5, 6, 7, 0, 9, 10, 11, 0, 13, 14, 15, 0, 17, 18, 19], :]
            v2 = joint[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], :]
            v = v2 - v1

            v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

            angle = np.arccos(np.einsum('nt,nt->n',
                                        v[[0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 18], :],
                                        v[[1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19], :]))  # [15,]

            angle = np.degrees(angle)

            data = np.array([angle], dtype=np.float32)
            ret, results, neighbours, dist = knn.findNearest(data, 3)
            idx = int(results[0][0])

            if idx in rps_gesture.keys():
                cv2.putText(img, text=rps_gesture[idx].upper(),
                            org=(int(res.landmark[0].x * img.shape[1]), int(res.landmark[0].y * img.shape[0] + 20)),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)

                current_time = datetime.now()

                if rps_gesture[idx] != prev_gesture:
                    prev_gesture_time = current_time
                    prev_gesture = rps_gesture[idx]
                    query_sent = False

                time_diff = (current_time - prev_gesture_time).total_seconds()

                if time_diff >= 0.3 and not query_sent:
                    insertCommand(rps_gesture[idx].upper(), "0")
                    query_sent = True

            mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Game', img)
    if cv2.waitKey(1) == ord('q'):
        break
        