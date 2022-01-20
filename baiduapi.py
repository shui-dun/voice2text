import requests
import json
import time
import os
import base64
from baiduKey import *
import PySimpleGUI as sg

baiduTokenPath = "baiduToken.json"

# 获得新的token，token过期时调用
def newToken():
    tokenUrl = "https://openapi.baidu.com/oauth/2.0/token"
    para = {"grant_type": "client_credentials", "client_id": apiKey, "client_secret": secretKey}
    try:
        response = requests.post(tokenUrl, params=para)
        token = response.json()["access_token"]
        newJson = {"token": token, "time": time.time()}
        with open(baiduTokenPath, "w") as f:
            json.dump(newJson, f)
        return token
    except Exception as e:
        sg.popup("error in newToken", e)


# 获取token
def getToken():
    if not os.path.exists(baiduTokenPath):
        return newToken()
    with open(baiduTokenPath) as f:
        tokenJson = json.load(f)
    curTime = time.time()
    secondInterval = curTime - tokenJson["time"]
    dayInterval = secondInterval / 60 / 60 / 24
    if dayInterval > 20:
        return newToken()
    else:
        return tokenJson["token"]


def voice2text(voiceFile):
    """
    将音频转化为文本
    :param voiceFile: 音频文件的路径
    :return: 转化为的文本
    """
    with open(voiceFile, "rb") as f:
        voice = f.read()
    json = {
        "format": voiceFile.rsplit(".", maxsplit=1)[1],
        "rate": 16000,
        "channel": 1,
        "cuid": "0ea138e3-aa68-405b-9253-36d6c8e6a31a",
        "token": getToken(),
        "len": os.path.getsize(voiceFile),
        "speech": base64.b64encode(voice).decode('utf-8')
    }
    url = "http://vop.baidu.com/server_api"
    try:
        response = requests.post(url, json=json).json()
        if response["err_no"] != 0:
            sg.popup("error in voice2text", response["err_msg"])
            return [""]
        return response["result"]
    except Exception as e:
        sg.popup("error in voice2text", e)
        return [""]
