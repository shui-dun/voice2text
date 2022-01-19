import requests
import json
import time
import os
import base64
from baiduKey import *


def newToken():
    tokenUrl = "https://openapi.baidu.com/oauth/2.0/token"
    para = {"grant_type": "client_credentials", "client_id": apiKey, "client_secret": secretKey}
    response = requests.post(tokenUrl, params=para)
    return response.json()["access_token"]


def getToken():
    with open("baiduToken.json") as f:
        tokenJson = json.load(f)
    curTime = time.time()
    secondInterval = curTime - tokenJson["time"]
    dayInterval = secondInterval / 60 / 60 / 24
    if dayInterval > 20:
        token = newToken()
        newJson = {"token": token, "time": curTime}
        with open("baiduToken.json", "w") as f:
            json.dump(newJson, f)
        return token
    else:
        return tokenJson["token"]


def voice2text(voiceFile):
    with open(voiceFile, "rb") as f:
        voice = f.read()
    json = {
        "format": voiceFile.rsplit(".", maxsplit=1)[1],
        "rate": 16000,
        "channel": 1,
        "cuid": "0ea138e3-aa68-405b-9253-36d6c8e6a31a",
        "token": getToken(),
        "dev_pid": 80001,
        "len": os.path.getsize(voiceFile),
        "speech": base64.b64encode(voice).decode('utf-8')
    }
    url = "https://vop.baidu.com/pro_api"
    response = requests.post(url, json=json)
    return response.json()["result"]
