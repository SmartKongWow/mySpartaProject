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
    return render_template('searchCC.html')

@app.route('/search', methods=['GET'])
def search_cc():
    # print("search cc start!")
    ccName_receive = request.args.get('ccName_sent')
    ccLocation_receive = request.args.get('location_sent')
    # print(ccName_receive, ccLocation_receive)

    if ccName_receive is not None:
        ccs = list(db.courses.find(
            {'ccName': {'$regex':ccName_receive}},
            {'_id':0, 'location': 1, 'ccName': 1, 'ccAddress':1, 'noOfHoles': 1, 'ccURL': 1, 'courseInfo': 1}
            ))
    else:
        ccs = list(db.courses.find(
            {'location':ccLocation_receive},
            {'_id':0,'location': 1, 'ccName': 1, 'ccAddress':1, 'noOfHoles': 1, 'ccURL': 1, "courseInfo": 1}
        ).sort('ccName', 1))

    return jsonify(({'result': 'success', 'ccs': ccs}))

if __name__ == '__main__':
   app.run('127.0.0.1', port=5000, debug=True)

