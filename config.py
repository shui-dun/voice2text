import PySimpleGUI as sg
from record import Recorder

# 主题
sg.theme("Default1")

# 字体
sg.set_options(font=('Consolas', 10))

START_RECORD = "开始录制"
STOP_RECORD = "停止录制"

START_PLAY = "开始播放"
STOP_PLAY = "停止播放"

# 音频保存位置
audioName = "temp.wav"

# 默认录制设备
defaultRecordSource = Recorder.SYSTEM_AUDIO
