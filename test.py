
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.db_golf_diary  # 'db_golf_diary'라는 이름의 db를 만들거나 사용합니다.

course = db.courses.find(
    {'ccName': "오션힐스포항CC"},
    {'_id':0, "courseInfo": 1}
)
print(course.count())
for doc in course:
    print(doc['courseInfo'])
    print(len(doc['courseInfo']))

    







# course_list = []
# for course in courses:
#     print(course['courseName'])
#     course_list.append(course['courseName'])
#
# print(course_list)



# list_courses = []
# for course in courses:
#     print(course['courseName'])
#     list_courses.append(course['courseName'])
#
# print(list_courses)
#
# courses = list(db.courses.find(
#     {'ccName': {'$regex': ccName_receive}},
#     {'_id': 0, "courseInfo.courseName": 1}
# ))[0]['courseInfo']
#
# courseNames = []
# for course in courses:
#     courseNames.append(course['courseName'])