from baiduapi import voice2text
from record import Recorder
import pyperclip

import PySimpleGUI as sg

START_RECORD = "开始录制"
STOP_RECORD = "停止录制"

layout = [[sg.Button(START_RECORD, key='record')],
          [sg.Button("退出", key="quit")]]

window = sg.Window('window name', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True, finalize=True)

# 音频记录器
recorder = None

# 音频保存位置
audioName = "temp.wav"

while True:
    event, value = window.Read()
    # 按下了按钮
    if event == 'record':
        if window.Element('record').get_text() == START_RECORD:
            recorder = Recorder()
            recorder.start()
            window.Element('record').Update(STOP_RECORD)
        elif window.Element('record').get_text() == STOP_RECORD:
            recorder.save(audioName)
            result = voice2text(audioName)
            pyperclip.copy(result[0])
            window.Element('record').Update(START_RECORD)
            recorder = None
    # 离开
    elif event == 'quit':
        break
