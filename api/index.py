from flask import Flask
from flask import request
import json
from bs4 import BeautifulSoup
import requests
base_url = "https://www.prydwen.gg/nikke/characters"

def GetSoup(url):
    r = requests.get(url).content
    soup = BeautifulSoup(r, 'html.parser')
    return soup

def SearchName(str):
    soup = GetSoup(base_url)
    char_names = soup.find_all("span", {"class": "emp-name"})
    for i in char_names:
        name = i.get_text().lower()
        if str.lower() in name:
            return name
    return "No name found!"
def GetChar(str):
    name = SearchName(str)
    data = {}
    if name != "No name found!":
        data = {}
        char_url = f"{base_url}/{name}"
        soup = GetSoup(char_url)
        
        rating_tags = soup.find('div', {"class":"detailed-ratings nikke"})
        picture_tag = soup.find('div', {"class":"gatsby-image-wrapper gatsby-image-wrapper-constrained disable-transition"})
        picture_tag = picture_tag.find("picture").find("img")['data-src']
        data["rating"] = {}

        for i in rating_tags:
            rating_rank = i.find("span").find("div").getText()
            rating_category = i.find("p").getText()
            data["rating"][rating_category] = rating_rank
        data["img_url"] = f"https://www.prydwen.gg{picture_tag}"


        profile_data = soup.find('div', {"class":"info-list"})
        collections = profile_data.find_all("div", {"class": "col"})

        for i in collections:
            data[i.find("h5").getText()] = {}
            for entry in i.find_all('div', {"class":"info-list-row"}):
                category = entry.find("div", {"class": "category"}).getText()
                details = entry.find("div", {"class": "details"}).getText()
                data[i.find("h5").getText()][category] =  details

        data["Skills"] = {}

        skill_data = soup.find('div', {"class":"skills"})
        collections = skill_data.find_all("div", {"class": "col"})

        for i in collections:
            for skill in i.find_all("div", {"class":"skill-box"}):
                skill_header = skill.find("div", {"class":"skill-header"})
                skill_content = skill.find("div", {"class":"skill-content"})
                skill_name = skill.find("h5", {"class":"name"}).getText()
                data["Skills"][skill_name] = {}
                data["Skills"][skill_name]["Header"] = {}
                data["Skills"][skill_name]["Info"] = []

                if skill_name == "Normal Attack":
                    weaponType = skill_header.find("span", {"class":"pill"})
                    Ammo = weaponType.find_next("span", {"class":"pill"})
                    ReloadTime = Ammo.find_next("span", {"class":"pill"})
                    data["Skills"][skill_name]["Header"]["Type"] = weaponType.get_text()
                    data["Skills"][skill_name]["Header"]["Ammo"] = Ammo.get_text()
                    data["Skills"][skill_name]["Header"]["Reload Time"] = ReloadTime.get_text()
                else:
                    data["Skills"][skill_name]["Header"]["skill-type"] = skill_header.find("span", {"class":"skill-type"}).getText()
                    if skill_header.find("span", {"class":"skill-type"}).getText() == "Active":
                        data["Skills"][skill_name]["Header"]["cooldown"] = skill_header.find("span", {"class":"pill"}).getText()


                for entry in skill_content.find("div", {"class":"skill-description"}).find_all("p"):
                    data["Skills"][skill_name]["Info"].append(entry.getText())
    return data

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    if char_name != "None":
        return json.dumps(GetChar(char_name))
    else:
        return 'test'
