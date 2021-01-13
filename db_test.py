from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.db_golf_diary

all_cc = list(db.courses.find())
# print(all_cc[0])
# print(all_cc[0]['ccName'])
#
# for cc in all_cc:
#     print(cc)

#충청권 골프장 검색

# cc_cc = list(db.courses.find({'location': '충청도'}))
# for cc in cc_cc:
#     print(cc['ccName'])

selectedCC = db.courses.find_one({'ccName': '델피노CC'}, {'_id':False})
print(selectedCC)