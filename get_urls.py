import requests
import io
from bs4 import BeautifulSoup
import mysql.connector as mysql

cnx = mysql.connect(user='root', password='', host='127.0.0.1', database='scrappy_data')
cursor = cnx.cursor(buffered=True)
# url = '1threads/https-www-playerup-com-middleman-page-id-5-form-cart-p-key-10947602-24853.5001506/'
# cursor.execute("SELECT * FROM data WHERE url LIKE '%" + url + "%'")
# print(cursor.fetchall())
# if(cursor.rowcount == 0):
#     print(url)
# exit()


for pageno in list(range(83)):
    
    if(pageno): 
        url = 'https://www.playerup.com/accounts/freelanceraccount/page-' + str(pageno+1) 
    else: 
        url = 'https://www.playerup.com/accounts/freelanceraccount/'

    while True:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find("div", class_='PageNav')
        if(results): break
    
    results = soup.find_all("li", class_='discussionListItem')
    for row in results:
        aTag = row.find('a', class_='PreviewTooltip')
        # fo.write(aTag['href']+'\n')    
        
        cursor.execute("SELECT * FROM data WHERE url='https://www.playerup.com/" + aTag['href'] + "'")
        
        if(cursor.rowcount == 0):
            print(aTag['href'])
        



    print(pageno+1)