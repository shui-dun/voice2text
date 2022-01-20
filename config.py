import PySimpleGUI as sg

# 主题
sg.theme("Default1")

# 字体
sg.set_options(font=('Consolas', 10))

START_RECORD = "开始录制"
STOP_RECORD = "停止录制"

START_PLAY = "播放音频"
STOP_PLAY = "停止播放"

# 音频保存位置
audioName = "temp.wav"

SYSTEM_AUDIO = "系统音频"
MIC_AUDIO = "麦克风"

# 默认录制设备
defaultRecordSource = SYSTEM_AUDIO

BAIDU_API = "百度api"
XUNFEI_API = "讯飞api"

# 默认语音识别api
defaultTextRecognition = BAIDU_API
