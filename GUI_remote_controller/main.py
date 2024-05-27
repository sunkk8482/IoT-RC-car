from PySide6.QtWidgets import *
from PySide6.QtCore import *
from mainUI import Ui_MainWindow

import mysql.connector
import pytz
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# 한국 시간대 (Asia/Seoul)로 설정
korea_timezone = pytz.timezone("Asia/Seoul")

class OpenAIWorker(QThread):
    response_ready = Signal(str)

    def __init__(self, input_text):
        super().__init__()
        self.input_text = input_text

    def run(self):
        # OpenAI에 명령 전송
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": self.input_text}],
            stream=True,
        )

        response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                response += chunk.choices[0].delta.content
        self.response_ready.emit(response)

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init()

    def init(self):
        print("INIT")
        #MySQL 접속 코드
        #본인이 만든 AWS EC2 URL 주소를 사용합니다.
        self.db = mysql.connector.connect(host='YOUR_HOST', user='YOUR_USER', password='YOUR_PASSWORD', database='YOUR_DATABASE', auth_plugin='mysql_native_password')
        self.cur = self.db.cursor(buffered=True)

        #timer setting
        self.timer = QTimer()
        self.timer.setInterval(500) #500ms
        self.timer.timeout.connect(self.pollingQuery)

    def start(self):
        print("Start")
        self.timer.start()

    def pollingQuery(self):
        # 최근 15개 정보만 가져오기
        self.cur.execute("select * from command order by time desc limit 15")
        self.logText.clear()
        for (id, time, cmd_string, arg_string, is_finish) in self.cur:
            str = "%5d | %s | %6s | %6s | %4d" % (id, time.strftime("%Y%m%d %H:%M:%S"), cmd_string, arg_string, is_finish)
            self.logText.appendPlainText(str)

    def insertCommand(self, cmd_string, arg_string):
        time = QDateTime().currentDateTime().toPython()
        is_finish = 0

        query = "insert into command(time, cmd_string, arg_string, is_finish) values (%s, %s, %s, %s)"
        value = (time, cmd_string, arg_string, is_finish)

        self.cur.execute(query, value)
        self.db.commit()

        self.nowcmd.setText(cmd_string)


    def stop(self):
        print("stop")
        self.insertCommand("STOP", "0")

    def go(self):
        print('go')
        self.insertCommand("GO", "0")

    def mid(self):
        print('mid')
        self.insertCommand("MID", "0")

    def back(self):
        print('back')
        self.insertCommand("BACK", "0")

    def left(self):
        print('left')
        self.insertCommand("LEFT", "0")

    def right(self):
        print('right')
        self.insertCommand("RIGHT", "0")

    def closeEvent(self, event):
        event.accept()
        #접속 종료
        self.cur.close()
        self.db.close()


    def enter(self):
        # 사용자가 입력한 내용 가져오기
        input_text = self.textinput.toPlainText()

        # 입력한 내용이 비어있지 않을 경우에만 처리
        if input_text.strip():
            # ansText에 "loading..." 표시
            self.ansText.setPlainText("loading...")

            # OpenAIWorker 스레드 생성 및 시작
            self.worker = OpenAIWorker(input_text)
            self.worker.response_ready.connect(self.update_ansText)
            self.worker.start()

            # 입력 필드 초기화
            self.textinput.clear()

    def update_ansText(self, response):
        self.ansText.setPlainText(response)


if __name__ == '__main__':
    app = QApplication()
    win = MyApp()
    win.show()
    app.exec()