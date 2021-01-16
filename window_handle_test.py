
from pymongo import MongoClient
from bson.son import SON
client = MongoClient('localhost', 27017)
db = client.db_golf_diary

ccs = db.courses.find(
        {}, {"_id": 0, "ccName": 1, "location": 1, "courseInfo.courseName":1}
    )
for cc in ccs:
    print(cc)

print(ccs.count())

courses_by_cc = db.courses.aggregate([
            {"$group":      {
                '_id':      {'cc':"$ccName"},
                'count':    {"$sum": 1}
            }}
            ])
print(list(courses_by_cc))



# inserted_courses = list(db.courses.find(
#     {"ccName": cc_name},
#     {"courseInfo.courseName"}
# ))
#
# noOfHoles = len(inserted_courses) * 9
# db.courses.update_one(
#     {"ccName": cc_name},
#     {"$set": {"noOfHoles": noOfHoles}}
# )
# print(cc_name + "에" + str(len(inserted_courses)) + "개의 코스를 추가하였습니다")
# print(cc_name + "은/는 " + str(noOfHoles) + "홀 골프장입니다.")




