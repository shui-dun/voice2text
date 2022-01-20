import baiduapi
import xunfeiapi
from record import Recorder
from player import Player
import pyperclip
import os
import PySimpleGUI as sg
import copy2clip
from config import *

layout = [[sg.Button(START_RECORD, key='record', size=(10, 1)),
           sg.Combo([SYSTEM_AUDIO, MIC_AUDIO], default_value=defaultRecordSource, key='audioSource', readonly=True,
                    size=(10, 1))],
          [sg.Button("复制文本", key='copyText', size=(10, 1)),
           sg.Combo([XUNFEI_API, BAIDU_API], default_value=defaultTextRecognition, key='textSource', readonly=True,
                    size=(10, 1))],
          [sg.Button("复制音频", key='copyAudio', size=(10, 1)),
           sg.Button(START_PLAY, key="play", size=(10, 1))],
          [sg.Text("录制结束后", size=(10, 1)),
           sg.Combo([COPY_TEXT_AFTER_RECORD, COPY_AUDIO_AFTER_RECORD, NOTHING_AFTER_RECORD],
                    default_value=defaultBehaviorAfterRecord, key="behaviorAfterRecord",
                    readonly=True, size=(10, 1))],
          [sg.Text("voice2text", size=(10, 1)),
           sg.Button("退出", key="quit", size=(10, 1))]]

window = sg.Window('window name', layout, no_titlebar=True, keep_on_top=True, grab_anywhere=True, finalize=True,
                   location=(20, 70))

# 音频记录器
recorder = None

# 音频播放器
player = None


# 语音识别成文字并复制
def copyText(source):
    if source == BAIDU_API:
        result = baiduapi.voice2text(audioName)
    elif source == XUNFEI_API:
        result = xunfeiapi.voice2text(audioName)
    pyperclip.copy(result)


# 复制音频文件
def copyAudio():
    filePath = os.getcwd() + "\\" + audioName
    copy2clip.clip_files([filePath])


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
            recorder = None
            window.Element('record').Update(START_RECORD)
            # 录制结束后执行的操作
            if value['behaviorAfterRecord'] == COPY_TEXT_AFTER_RECORD:
                copyText(value['textSource'])
            elif value['behaviorAfterRecord'] == COPY_AUDIO_AFTER_RECORD:
                copyAudio()
            elif value['behaviorAfterRecord'] == NOTHING_AFTER_RECORD:
                pass
    # 复制识别到的文本
    elif event == 'copyText':
        copyText(value['textSource'])
    # 播放
    elif event == 'play':
        if window.Element('play').get_text() == START_PLAY:
            player = Player(audioName)
            player.start()
            window.Element('play').Update(STOP_PLAY)
        elif window.Element('play').get_text() == STOP_PLAY:
            player.stop()
            player = None
            window.Element('play').Update(START_PLAY)
    # 复制音频
    elif event == 'copyAudio':
        copyAudio()
    # 离开
    elif event == 'quit':
        break
