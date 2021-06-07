import requests
import io
from bs4 import BeautifulSoup
import mysql.connector as mysql
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("start", help="echo the start number")
parser.add_argument("end", help="echo the end number")
args = parser.parse_args()

def realContent(tag):
    rlt = ''
    for content in tag.contents:
        if(content.name == None):
            rlt = rlt + content
    return rlt
def scrappy(id, url):
    print(id)
    print(url)
    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    titleBar = soup.find(class_="titleBar")
    if(titleBar):
        spans = titleBar.h1.find_all("span")
        
        query = "UPDATE data SET "
        k = 0
        for span in spans:
            k = k + 1
            if(k > 1): 
                query = query + ", "
            query = query + "info" + str(k) + " = '" + span.string + "' "

        
        query = query + ", info7 = '" + realContent(titleBar.h1).replace("'", "\\'") + "'"
 
        msgContent = soup.find(class_="messageContent")
        if(msgContent):
            # print(msgContent.find('dd'))
            if(msgContent.find('dd')):
                query = query + ", info8 = '" + ''.join([text for text in msgContent.find('dd').stripped_strings]).replace("'", "\\'") + "'"

            # print(msgContent.find('blockquote'))
            query = query + ", info9 = '" + msgContent.find('blockquote').prettify().replace("'", "\\'") + "'"

        highrisk = soup.find("em", class_="my-style-highrisk")
        if(highrisk):
            query = query + ", info10 = 'highrisk'"

        suspended = soup.find("em", class_="my-style-suspended")
        if(suspended):
            query = query + ", info11 = 'suspended'"
        query = query + ", new=1"
        query = query + " WHERE id = " + str(id)
        print(query)
        try:
            cursor.execute(query)
            cnx.commit()
        except Exception:
            print('error')
        else:
            print('success')
    else:
        print('not found')
    return

cnx = mysql.connect(user='root', password='', host='127.0.0.1', database='scrappy_data')
cursor = cnx.cursor()

cursor.execute("SELECT * FROM data WHERE id>=" + args.start + " AND id<" + args.end)

rows = cursor.fetchall() ## it returns list of tables present in the database

## showing all the tables one by one
# scrappy(400, 'https://www.playerup.com/threads/rent-an-account.4877817/')
for row in rows:
    if(row[2] == 'Hafeez'):
        scrappy(row[0], row[1])
cursor.close()
cnx.close()