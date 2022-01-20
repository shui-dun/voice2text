from baiduapi import voice2text
from record import Recorder
import pyperclip
import os
import PySimpleGUI as sg
import copy2clip

START_RECORD = "开始录制"
STOP_RECORD = "停止录制"

layout = [[sg.Button(START_RECORD, key='record'),
           sg.Combo([Recorder.SYSTEM_AUDIO, Recorder.MIC_AUDIO], default_value=Recorder.SYSTEM_AUDIO, key='audioSource',
                    readonly=True, size=(8, 1))],
          [sg.Button("复制文本", key='copyText'), sg.Button("退出", key="quit")]]

window = sg.Window('window name', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True, finalize=True)

# 音频记录器
recorder = None

# 音频保存位置
audioName = "temp.wav"

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
        result = voice2text(audioName)
        pyperclip.copy(result[0])
    # 离开
    elif event == 'quit':
        break
