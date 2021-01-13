
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.db_golf_diary  # 'db_golf_diary'라는 이름의 db를 만들거나 사용합니다.

print(db.courses.find({'ccName': '오션힐스포항CC'})[3])