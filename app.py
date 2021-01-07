from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.db_golf_diary  # 'db_golf_diary'라는 이름의 db를 만들거나 사용합니다.

#HTML
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/plan')
def rounding_plan():
    return  render_template('roundingPlan.html')

@app.route('/plan', methods=['GET'])
def get_CC_():
    # 클라이언트로부터 골프장이름을 받는다.
    ccName = request.args['ccName']

    # DB를 골프장이름으로 검색한다.
    result = list(db.courses.find({"ccName":ccName}, {'_id':0}))
    print(result)
    return jsonify({'result': 'success', 'ccs': result})



#@app.route('/api')
#def api():

#API: course information

#@app.route('/api/course')
#def showCourseInfo_get():


#API: rounding_plan information
#@app.route('api/rounding-plan')



#API: rounding_result information

#


if __name__ == '__main__':
   app.run('127.0.0.1', port=5000, debug=True)