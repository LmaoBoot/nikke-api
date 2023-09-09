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
        print(f"{base_url}/{name}")
        rating_tags = soup.find('div', {"class":"detailed-ratings nikke"})
        picture_tag = soup.find('div', {"class":"gatsby-image-wrapper gatsby-image-wrapper-constrained disable-transition"})
        picture_tag = picture_tag.find("picture").find("img")['data-src']
        print(picture_tag)
        data["img_url"] = f"https://www.prydwen.gg{picture_tag}"

    return data

app = Flask(__name__)

@app.route('/', methods=['GET'])

def home_page():
    char_name = str(request.args.get('character'))
    if char_name != "None":
        return json.dumps(GetChar(char_name))
    else:
        return 'test'
