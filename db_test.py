from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.db_golf_diary

#searched_courses = list(db.courses.find({"ccName":{$regex : "골든베이_"}))
searched_courses = list(db.courses.find({"ccName": "골든베이"}))

print(len(searched_courses))

print(searched_courses)
