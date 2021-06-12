from flask import Flask, request, render_template  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource, fields  # Api 구현을 위한 Api 객체 import
import RPi.GPIO as GPIO
import time

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(21, GPIO.IN)
GPIO.setwarnings(False)

isAction = False 
states = ["0", "1", "2", "3"]
state = 0

@api.route('/door')
class OpenDoor(Resource):
    def put(self):
        global state
        return "OK"
        try:
            while True:
                inputIO = GPIO.input(21)
                #입력 받으면
                if inputIO == False:
                    state += 1
                    print("Opennig")
                    for i in range(0,12):
                        GPIO.output(6, GPIO.HIGH)
                        time.sleep(0.2)
                        GPIO.output(6,GPIO.LOW)
                        time.sleep(0.2)
                        i += 1
                    #열리는 중 반짝임

                    print("Open")
                    state += 1
                    GPIO.output(6, GPIO.HIGH)
                    time.sleep(3)
                    #개방 완료 빨간불

                    print("Closing")
                    state += 1
                    for i in range(0,12):
                        GPIO.output(6, GPIO.HIGH)
                        time.sleep(0.2)
                        GPIO.output(6,GPIO.LOW)
                        time.sleep(0.2)
                        i += 1
                    #닫히는 중 반짝임

                    print("Close")
                    state = 0
                    GPIO.output(6,GPIO.LOW)
                    #폐문 완료 불 꺼짐

        except KeyboardInterrupt:
            GPIO.cleanup()

@api.route('/state')
class Doorstate(Resource):
    def get(self):
        global states, state

        return {"Response" : states[state]}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=40000)
