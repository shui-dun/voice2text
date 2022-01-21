import PySimpleGUI as sg

# 主题
sg.theme("Default1")

# 字体
sg.set_options(font=('Consolas', 10))

START_RECORD = "开始录制"
STOP_RECORD = "停止录制"

# 音频保存位置
audioName = r"audio\temp.wav"

SYSTEM_AUDIO = "系统音频"
MIC_AUDIO = "麦克风"

# 默认录制设备
defaultRecordSource = SYSTEM_AUDIO

BAIDU_API = "百度api"
XUNFEI_API = "讯飞api"

# 默认语音识别api
defaultTextRecognition = XUNFEI_API

COPY_TEXT_AFTER_RECORD = "复制文本"
COPY_AUDIO_AFTER_RECORD = "复制音频"
NOTHING_AFTER_RECORD = "不执行操作"

# 在录制结束后自动执行的操作
defaultBehaviorAfterRecord = COPY_TEXT_AFTER_RECORD
