from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.db_golf_diary
db.courses.delete_many({}) #추후 업데이트로 바꿀 것. 지금은 정보를 모두 지우고 새롭게 저장.

def course_info_scrap():
    # 페이지소스를 html에 담고, BeautifulSoup로 파싱하여 soup에 담는다.
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 골프장 정보를 각 변수에 담는다.

    cc_location = soup.select_one('.list_info_tit  strong').text
    cc_name = soup.select_one('.list_info_tit  a').text
    if "-" in cc_name:
        cc_name = cc_name.split("-")[0].replace(" ", "")
        print(cc_name)
    else:
        cc_name.strip()
        print("else:", cc_name)
    cc_detail = soup.select('.detail table tr:nth-child(1) td')
    cc_no_hole = cc_detail[0].text
    cc_length = cc_detail[1].text
    cc_basic_info = soup.select('.basic_info td')
    cc_address = cc_basic_info[0].text
    cc_url = cc_basic_info[1].text
    cc_phone = cc_basic_info[2].text
    cc_fax = cc_basic_info[3].text

    hole_info = soup.select('.hall_info > h5 > strong')
    hole_table = soup.select('.hall_info > table')

    # print(hole_table)
    # 골프장에 있는 코스 수 만큼 루프를 돌리며, 필요한 정보를 크롤링한다.

    for i in range(0, len(hole_info)):
        # 코스이름 정보를 course_name에 담는다.
        course_name = hole_info[i].text
        print(course_name)

        # 각 코스별 파 정보를 hole_par에 담는다.
        hole_par = hole_table[i].select('thead > tr:nth-child(2) > th')
        # print(hole_par)

        # hole_par 정보에 붙어 있는 tag를 제거하여 par_list에 저장한다.
        par_list = []

        for par in hole_par:
            par_list.append(par.text)

        # print(par_list)

        # par_list에 있는 첫번째 항목인 'PAR'를 par_dic의 키값으로, 나머지 홀정보를 정수로 변환하여 리스트 밸류로 담는다.
        par_dic = {par_list[0]: list(map(int, par_list[1:]))}
        # print(par_dic)

        # 각 tee 별 거리 정보를 추출한다.
        # 각 tee 이름은 tees_type에, 각 tee별 전장은 tees_length에 크롤링한다.
        tees_type = hole_table[i].select('tbody > tr > th')
        tees_length = hole_table[i].select('tbody > tr > td')

        # tee type 크롤링 후 tag를 제거하여 tees_type_list에 리스트로 저장한다.
        tees_type_list = []
        for tee_type in tees_type:
            tees_type_list.append(tee_type.text)

        # tee length 크롤링하여 tees_length_list에 리스트로 담는다.
        # 만약 anchor tag가 있으면, src만 저장하고, 그렇지 않으면, 마지막 문자를 제거하고 정수로 변환하여 담는다.

        tees_length_list = []
        for tee_length in tees_length:
            if tee_length.select_one('a') is not None:
                tees_length_list.append(tee_length.select_one('img')['src'])
            else:
                tees_length_list.append(int(tee_length.text[:-1]))

        # Map_image_dic 딕셔너리를 만들고, tees_type_list의 제일 마지막 값인 'MAP'을 키값으로, tee_length_list에서 각 타입별 거리정보가 끝난 지점부터 끝까지 정보를 밸류로 담는다)
        map_image_dic = {
            tees_type_list[len(tees_type_list) - 1]: tees_length_list[(9 * (len(tees_type_list) - 1)):]}
        # print(map_image_dic)

        # tee_type_list에서 마지막 요소를 삭제한다.
        tees_type_list.pop()
        # print('tee type:', tees_type_list)
        # tee_type_length에서 마지막 아홉개의 이미지를 삭제한다.
        del tees_length_list[-9:]
        # print('tee length: ', tees_length_list)

        # hole_dic를 만들어 par정보를 먼저 담는다.
        hole_dic = {}
        hole_dic = dict(hole_dic, **par_dic)

        # tee_type 개수만큼 루프를 돌려, 각 티별 딕셔너리를 hole_dic에 추가한다.
        for tee_type in tees_type_list:
            hole_dic.setdefault(tees_type_list[i])
            for j in range(0, len(tees_type_list), 9):
                hole_dic[tee_type] = tees_length_list[j:j + 9]
        # 마지막으로 hole_dic에 map_image_dic을 추가한다.
        # hole_dic.update(map_image_dic)

        doc = {
            'location': cc_location,
            'ccName': cc_name,
            'noOfHole홀수': cc_no_hole,
            'totalLength': cc_length,
            'ccAddress': cc_address,
            'ccURL': cc_url,
            'ccPhone': cc_phone,
            'ccFax': cc_fax,
            'courseName': course_name,
            'holeInfo': hole_dic,
            'mapImg': map_image_dic
        }

        db.courses.insert_one(doc)

def pagination_click(p):
    target = driver.find_element_by_link_text('{}'.format(p))
    target.click()
    time.sleep(2)

def page_scraping():
    # 그 페이지의 모든 골프장을 리스트에 담는다.
    ccs = driver.find_elements_by_css_selector("#datalist .course_posi > a")
    # 각 골프장 마다 새로운 탭으로 오픈한다.
    for cc in ccs:
        cc.send_keys(Keys.CONTROL + "\n")
    time.sleep(5)

    # 각 탭의 핸들의 갯수만큼 다음을 반복한다.
    # 스크래핑할 탭으로 이동하고 스크래핑을 한 후 db에 저장하고 해당 탭을 닫는다.
    win_handle = driver.window_handles
    for i in range(1, len(win_handle)):
        driver.switch_to.window(win_handle[i])
        course_info_scrap()
        driver.close()
    driver.switch_to.window(win_handle[0])


#웹드라이버를 구동한다.
driver = webdriver.Chrome(executable_path="../venv/Scripts/chromedriver.exe")
#첫페이지를 연다.
driver.get("http://www.golfzon.com/course/list/R")

for page in range(1, 27):
    print('page=', page)
    d = page%10
    if d == 1: #나머지가 1이면 곧바로 page_scraping을 시작한다.
        page_scraping()
    elif d == 0: #나머지가 0이면 페이지 d를 클릭하고 스크래핑한다 그리고, '다음'을 클릭한다.
        pagination_click(page)
        page_scraping()
        next_move = driver.find_element_by_css_selector('#miniround_paging > a.next_pageGroup > img')
        next_move.click()
        time.sleep(1)
    else: #0이 아니면 반복해서 페이지를 클릭해서 열고 scraping한다.
        p = page
        pagination_click(p)
        page_scraping()

driver.close()



