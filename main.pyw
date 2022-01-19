from baiduapi import voice2text
from record import Recorder
import pyperclip

import PySimpleGUI as sg

# 状态变量，表示当前正在录制音频
RECORDING = 0
# 状态变量，表示当前没有录制音频
STOPPED = 1

# 当前状态
curStatus = STOPPED

layout = [[sg.Button("开始录制", key='record')],
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
        if curStatus == STOPPED:
            recorder = Recorder()
            recorder.start()
            window.Element('record').Update("停止录制")
            curStatus = RECORDING
        elif curStatus == RECORDING:
            recorder.save(audioName)
            result = voice2text(audioName)
            pyperclip.copy(result[0])
            window.Element('record').Update("开始录制")
            recorder = None
            curStatus = STOPPED
    # 离开
    elif event == 'quit':
        break
