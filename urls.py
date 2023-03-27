from bs4 import BeautifulSoup
import requests
import sqlite3
import smtplib
from email.mime.text import MIMEText


db_connection = sqlite3.connect('valdemarsro.sqlite')
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS valdemar (opskriftTitle TEXT, opskriftLink TEXT)')

def article_is_not_db(opskriftTitle, opskriftLink):
    db.execute("SELECT * from valdemar WHERE opskriftTitle=? AND opskriftLink=?", (opskriftTitle, opskriftLink))
    if not db.fetchall():
        return True
    else:
        return False

def add_article_to_db(opskriftTitle, opskriftLink):
    db.execute("INSERT INTO valdemar VALUES (?, ?)", (opskriftTitle, opskriftLink))
    db_connection.commit()


def read_articles():
   with open('myfile.txt', 'r') as url_file:
      for line in url_file:
         opskriftLink = line.strip()
         response = requests.get(opskriftLink)
         data = response.text
         soup = BeautifulSoup(data,'lxml')

         opskriftTitle = soup.find_all("div", {"class": "title"})[1].text.strip()
         opskriftTid = soup.find_all("div", {"class": "recipe-stat"})[0].text.strip("Tid i alt ")
         opskriftArbejdstid = soup.find_all("div", {"class": "recipe-stat"})[1].text.strip("Arbejdstid ")
         opskriftAntal = soup.find_all("div", {"class": "recipe-stat"})[2].text.strip("Antal ")
         opskriftIngrediens = soup.find_all("ul")[7]

         #needs a fix for encoding
         opskriftFremgang = soup.find("div", {"itemprop": "recipeInstructions"})
         opskriftFremgang2 = str(opskriftFremgang.encode('utf-8'))
         opskriftTips = soup.find_all("ul")[8].encode('utf-8')

         #print("-----------------------------------------------------------")
         #print(opskriftTitle)
         #print("-----------------------------------------------------------")
         #print("Tid i alt: "+opskriftTid)
         #print("Arbejdstid: "+opskriftArbejdstid)
         #print("Antal: "+opskriftAntal)
         #print(opskriftLink)
         #print("Ingredienser: "+opskriftIngrediens)
         #print("Fremgangsmåde: "+opskriftFremgang2)
         #print("\n")

         if article_is_not_db(opskriftTitle, opskriftLink):
            add_article_to_db(opskriftTitle, opskriftLink)
            ### Email notification
            send_notification(opskriftTitle, opskriftLink, opskriftIngrediens)

def send_notification(opskriftTitle, opskriftLink, opskriftIngrediens):
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login('spiltipsbot@gmail.com', 'leazjykkdvctbwaw')
    msg = MIMEText(f'\n{opskriftTitle}. \n{opskriftIngrediens}. \n{opskriftLink}')
    msg['Subject'] = opskriftTitle
    msg['From'] = 'spiltipsbot@gmail.com'
    msg['To'] = 'zere0.mail@gmail.com'

    #fix html opskriftIngrediens
    #msg.add_header('Content-Type','text/html')
    smtp_server.send_message(msg)
    smtp_server.quit()
    print("email sent - "+msg["Subject"])


if __name__ == '__main__':
    read_articles()
    db_connection.close()
