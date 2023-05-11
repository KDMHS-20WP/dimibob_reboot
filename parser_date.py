import requests
from bs4 import BeautifulSoup
import datetime
import json
from dateutil.parser import parse as date_parse
import sys

target_date = date_parse(sys.argv[1])

def check_date(date: str):
    # 6월 17일 식단입니다.
    # 6월17일 식단입니다.
    # 6월 17일 식단입니다

    date = date.replace(" ", "")
    date = date.split("식단")[0]
    date = date.replace("월", "-")
    date = date.replace("일", "")

    td_first = target_date
    td_first -= datetime.timedelta(days=td_first.weekday())

    td_last = td_first + datetime.timedelta(days=6)

    try:
        fd = date_parse(date)
        # check target date is in range
        if fd < td_first or fd > td_last:
            fd = datetime.datetime(1, 1, 1)
    except:
        fd = datetime.datetime(1, 1, 1)
    

    return fd


req = requests.get("https://www.dimigo.hs.kr/index.php?mid=school_cafeteria&page=1")
html = req.text
soup = BeautifulSoup(html, "html.parser")

bob_articles = soup.select("#dimigo_post_cell_1 > tr")


result_data = {"meals": []}

for bob_article in bob_articles:
    # dimigo_post_cell_2 > tr:nth-child(1) > td.title > a
    bob_title = bob_article.find("td", {"class": "title"}).find("a").text
    bob_link = bob_article.find("td", {"class": "title"}).find("a").get("href")

    if bob_title.find("식단") != -1:
        print(bob_title)
        fd = check_date(bob_title)
        if fd.year != 1:
            bob_req = requests.get(bob_link)
            bob_html = bob_req.text
            bob_soup = BeautifulSoup(bob_html, "html.parser")

            bob_menu = bob_soup.select(
                "#siDoc > ul:nth-child(5) > li > div.scConDoc.clearBar > div"
            )[0]
            bob_menu = bob_menu.text.replace("\n", "")

            bob_menu.replace(" ", "")
            josik = bob_menu.partition("*조식:")[2].partition("*중식:")[0].strip()
            jungsik = bob_menu.partition("*중식:")[2].partition("*석식:")[0].strip()
            soksik = bob_menu.partition("*석식:")[2].strip()

            data = {
                "date": fd.strftime("%Y-%m-%d"),
                "josik": josik,
                "jungsik": jungsik,
                "soksik": soksik,
            }
            result_data["meals"].append(data)

td = target_date
td -= datetime.timedelta(days=td.weekday())
with open("datas/" + td.strftime("%m-%d") + ".json", "w", encoding="utf-8") as f:
    json.dump(result_data, f, ensure_ascii=False, indent="\t")
    print("OK")
