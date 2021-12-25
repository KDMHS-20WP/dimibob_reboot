import requests
from bs4 import BeautifulSoup
import datetime
import json

def check_date(date):
  today = datetime.date.today()
  today -= datetime.timedelta(days=today.weekday())
  
  found_date = datetime.date(1, 1, 1)

  for i in range(7):
    if date.find(today.strftime("%m월 %d일")) != -1:
      found_date = today
    today += datetime.timedelta(days=1)
  return found_date
  
req = requests.get('https://www.dimigo.hs.kr/index.php?mid=school_cafeteria&page=1')
html = req.text
soup = BeautifulSoup(html, 'html.parser')

bob_articles = soup.select(
  '#dimigo_post_cell_2 > tr'
)

result_data = {
  'meals': []
}

for bob_article in bob_articles:
  #dimigo_post_cell_2 > tr:nth-child(1) > td.title > a
  bob_title = bob_article.find('td', {'class': 'title'}).find('a').text
  bob_link = bob_article.find('td', {'class': 'title'}).find('a').get('href')

  if bob_title.find('식단') != -1:
    found_date = check_date(bob_title)
    if(found_date.year != 1):
      bob_req = requests.get(bob_link)
      bob_html = bob_req.text
      bob_soup = BeautifulSoup(bob_html, 'html.parser')

      bob_menu = bob_soup.select('#siDoc > ul:nth-child(5) > li > div.scConDoc.clearBar > div')[0]
      bob_menu = bob_menu.text.replace('\n', '')
      
      josik = bob_menu.partition('*조식 : ')[2].partition('*중식 : ')[0].strip() #.replace('/', '\n')
      jungsik = bob_menu.partition('*중식 : ')[2].partition('*석식 : ')[0].strip() #.replace('/', '\n')
      soksik = bob_menu.partition('*석식 : ')[2].strip() #.replace('/', '\n')

      data = {
        'date' : found_date.strftime("%Y-%m-%d"),
        'josik' : josik,
        'jungsik' : jungsik,
        'soksik' : soksik
      }

      result_data['meals'].append(data)

today = datetime.date.today()
today -= datetime.timedelta(days=today.weekday())
with open('datas/'+ today.strftime('%m-%d') + '.json', 'w', encoding='utf-8') as f:
  res = json.dump(result_data, f, ensure_ascii=False, indent='\t')
  print('OK')
