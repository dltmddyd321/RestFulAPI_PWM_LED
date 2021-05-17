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


@api.route('/led/0')
class GetLedState(Resource):
    def get(self):
        GPIO.output(6,GPIO.LOW)
        GPIO.output(20,GPIO.LOW)
        return {"Response":0}

@api.route('/led/openning')
class GetLedState(Resource):
    def get(self):
        try:
            while True:
                inputIO = GPIO.input(21)

                if inputIO == False:
                    for i in range(0,12):
                        GPIO.output(6, GPIO.HIGH)
                        time.sleep(0.2)
                        GPIO.output(6,GPIO.LOW)
                        time.sleep(0.2)
                        i += 1
                    GPIO.output(6, GPIO.HIGH)
                    time.sleep(3)
                    GPIO.output(6,GPIO.LOW)


                else:
                    GPIO.output(6, GPIO.LOW)
                    #time.sleep(1)

        except KeyboardInterrupt:
            GPIO.cleanup()

@api.route('/led/2')
class GetLedState(Resource):
    def get(self):
        GPIO.output(20, GPIO.HIGH)
        return {"Response":2}

@api.route('/led/3')
class GetLedState(Resource):
    def get(self):
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(20, GPIO.HIGH)
        return {"Response":3}

@api.route('/led/<int:state>')
class SetLedState(Resource):
    def put(self, state):
        if state == 0 :
            GPIO.output(17,GPIO.LOW)
            GPIO.output(20,GPIO.LOW)
        elif state == 1 :
            GPIO.output(17, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(17,GPIO.LOW)
        elif state == 2 :
            GPIO.output(20, GPIO.HIGH)
        elif state == 3 :
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(20, GPIO.HIGH)
        else :
            print("다시 선택")
        return {"Response": state}

@api.route("/reset")
class Reset(Resource):
    def get(self):
        GPIO.cleanup()
        return {"Response":"OK"}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=60000)