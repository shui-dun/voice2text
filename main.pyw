import baiduapi
import xunfeiapi
from record import Recorder
import pyperclip
import os
import copy2clip
from config import *

layoutFull = [[sg.Button(START_RECORD, key='record', size=(10, 1)),
               sg.Combo([SYSTEM_AUDIO, MIC_AUDIO], default_value=DEFAULT_RECORD_SOURCE, key='audioSource', readonly=True,
                        size=(10, 1))],
              [sg.Button("复制文本", key='copyText', size=(10, 1)),
               sg.Combo([XUNFEI_API, BAIDU_API], default_value=DEFAULT_TEXT_RECOGNITION, key='textSource', readonly=True,
                        expand_x=True)],
              [sg.Button("复制音频", key='copyAudio', size=(10, 1)),
               sg.Button("播放音频", key="play", expand_x=True)],
              [sg.Text("录制结束后", size=(10, 1)),
               sg.Combo([COPY_TEXT_AFTER_RECORD, COPY_AUDIO_AFTER_RECORD, NOTHING_AFTER_RECORD],
                        default_value=DEFAULT_BEHAVIOR_AFTER_RECORD, key="behaviorAfterRecord",
                        readonly=True, expand_x=True)],
              [sg.Button("迷你模式", key="mini", expand_x=True)]]

layoutMini = [[sg.Button(START_RECORD, key='miniRecord'), sg.Button("完整模式", key="full")]]

layout = [[sg.Column(layoutFull, key='fullLayout', visible=False), sg.Column(layoutMini, key='miniLayout')]]

window = sg.Window('V2T', layout, keep_on_top=True,use_custom_titlebar=True, grab_anywhere=True, finalize=True,
                   location=(20, 70))

# 音频记录器
recorder = None

# 音频播放器
player = None


# 语音识别成文字并复制
def copyText(source):
    sg.popup_quick_message("开始识别")
    if source == BAIDU_API:
        result = baiduapi.voice2text(AUDIO_PATH)
    elif source == XUNFEI_API:
        result = xunfeiapi.voice2text(AUDIO_PATH)
    pyperclip.copy(result)
    sg.popup_quick_message("识别结果已复制到剪切板")


# 复制音频文件
def copyAudio():
    filePath = os.getcwd() + "\\" + AUDIO_PATH
    copy2clip.clip_files([filePath])
    sg.popup_quick_message("音频文件已复制到剪切板")


while True:
    event, value = window.Read()
    # 按下了录制按钮
    if event == 'record' or event == 'miniRecord':
        if window.Element(event).get_text() == START_RECORD:
            recorder = Recorder(value['audioSource'])
            recorder.start()
            window.Element(event).Update(STOP_RECORD)
        elif window.Element(event).get_text() == STOP_RECORD:
            recorder.save(AUDIO_PATH)
            recorder = None
            window.Element(event).Update(START_RECORD)
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
        os.startfile(AUDIO_PATH)
    # 复制音频
    elif event == 'copyAudio':
        copyAudio()
    elif event == 'mini':
        window.Element('fullLayout').update(visible=False)
        window.Element('miniLayout').update(visible=True)
        window.Element('miniRecord').Update(window.Element('record').get_text())
    elif event == 'full':
        window.Element('fullLayout').update(visible=True)
        window.Element('miniLayout').update(visible=False)
        window.Element('record').Update(window.Element('miniRecord').get_text())
    elif event == sg.WIN_CLOSED:
        break
