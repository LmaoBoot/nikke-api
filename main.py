from flask import Flask
from flask import request
import json
from characters import GetChar
app = Flask(__name__)

@app.route('/', methods=['GET'])

def home_page():
    char_name = str(request.args.get('character'))
    if char_name != "None":
        return json.dumps(GetChar(char_name))
    else:
        return json.dumps({"output":"None"})



