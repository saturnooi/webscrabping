from bs4 import BeautifulSoup
import requests
import re
from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
@app.route('/')
def home():
    url = "https://www.sanook.com/news/archive/"
    res = requests.get(url)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, 'html.parser')

    all = []
    crime = []
    politics = []
    medical = []
    accident = []

    data = soup.find_all("article", {"class": "jsx-4051291596 PostListWithDetail"})
    for i in data:
        title = i.find_all("a")
        img = i.find_all("img")
        dictdata = {
            "title" : title[1].get_text(),
            "subtitle":(re.findall("(?:<p.*?class=\"jsx-2430232205 jsx-1621000947 description\".*?>)(.*?)(?:<\\/p>)", str(i))),
            "link": re.findall('href[ ]{0,1}=[ ]{0,1}"([^\"]{0,})"', str(title[0]), re.I)[0],
            "img":re.findall('src[ ]{0,1}=[ ]{0,1}"([^\"]{0,})"', str(img[0]), re.I)[0],
            
        }
        
     
        all.append(dictdata )
        if "โหด" in dictdata["title"] or "แทง" in dictdata["title"] or "ยิง" in dictdata["title"] or "ร้าย" in dictdata["title"]  or "คลั่ง" in dictdata["title"] or "ปล้น" in dictdata["title"] or "ชิง" in dictdata["title"]:
            crime.append(dictdata )
        if "โรค" in dictdata["title"] or "แพทย์" in dictdata["title"] or "โควิท" in dictdata["title"]  or "หมอ" in dictdata["title"]:
            medical.append(dictdata )
        if "ราคา" in dictdata["title"] or "ทอง" in dictdata["title"] or "น้ำมัน" in dictdata["title"]  or "หวย" in dictdata["title"] or "รางวัล" in dictdata["title"]:
            accident.append(dictdata )
        if "ส.ส." in dictdata["title"] or "พรรค" in dictdata["title"]  or "การเมือง" in dictdata["title"]:
            politics.append(dictdata )

    return {"All" : all ,"Crime" : crime,"Politics" : politics,"Medical" : medical ,"Accident" : accident}
if __name__ == '__main__':
    app.run(debug=True)