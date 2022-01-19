from baiduapi import voice2text
from record import Recorder
import pyperclip

import PySimpleGUI as sg

RECORDING = 0
STOPPED = 1

curStatus = STOPPED

layout = [[sg.Button("start", key='button')]]

window = sg.Window('window name', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True, finalize=True)

window.bind("<q>", "quit")

recorder = None

audioName = "temp.wav"

while True:
    event, value = window.Read()
    if event == 'button':
        if curStatus == STOPPED:
            recorder = Recorder()
            recorder.start()
            window.Element('button').Update("stop")
            curStatus = RECORDING
        elif curStatus == RECORDING:
            recorder.save(audioName)
            result = voice2text(audioName)
            pyperclip.copy(result[0])
            window.Element('button').Update("start")
            recorder = None
            curStatus = STOPPED
    elif event == 'quit':
        break
