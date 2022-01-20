import baiduapi
import xunfeiapi
from record import Recorder
from player import Player
import pyperclip
import os
import PySimpleGUI as sg
import copy2clip
from config import *

layout = [[sg.Button(START_RECORD, key='record'),
           sg.Combo([Recorder.SYSTEM_AUDIO, Recorder.MIC_AUDIO], default_value=defaultRecordSource, key='audioSource',
                    readonly=True, size=(8, 1))],
          [sg.Button("复制文本", key='copyText'), sg.Button(START_PLAY, key="play")],
          [sg.Button("退出", key="quit", size=(16, 1))]]

window = sg.Window('window name', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True, finalize=True,
                   location=(20, 70))

# 音频记录器
recorder = None

# 音频播放器
player = None

while True:
    event, value = window.Read()
    # 按下了录制按钮
    if event == 'record':
        if window.Element('record').get_text() == START_RECORD:
            recorder = Recorder(value['audioSource'])
            recorder.start()
            window.Element('record').Update(STOP_RECORD)
        elif window.Element('record').get_text() == STOP_RECORD:
            recorder.save(audioName)
            filePath = os.getcwd() + "\\" + audioName
            copy2clip.clip_files([filePath])
            recorder = None
            window.Element('record').Update(START_RECORD)
    # 复制识别到的文本
    elif event == 'copyText':
        # result = baiduapi.voice2text(audioName)
        result = xunfeiapi.voice2text(audioName)
        pyperclip.copy(result)
    elif event == 'play':
        if window.Element('play').get_text() == START_PLAY:
            player = Player(audioName)
            player.start()
            window.Element('play').Update(STOP_PLAY)
        elif window.Element('play').get_text() == STOP_PLAY:
            player.stop()
            player = None
            window.Element('play').Update(START_PLAY)
    # 离开
    elif event == 'quit':
        break
