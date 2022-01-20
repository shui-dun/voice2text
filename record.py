import os.path
import threading
import time

import numpy as np
import soundcard as sc
import soundfile as sf

from config import SYSTEM_AUDIO, MIC_AUDIO


class Recorder:
    # 采样频率
    samplerate = 16000

    def __init__(self, source):
        self.source = source
        # 是否完成
        self.isFinished = False
        # 音频片段列表
        self.voices = []

    def __record(self):
        if self.source == SYSTEM_AUDIO:
            mic = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
        elif self.source == MIC_AUDIO:
            mic = sc.default_microphone()
        with mic.recorder(samplerate=self.samplerate) as recorder:
            while True:
                # 只取第一个channel
                newVoice = recorder.record(numframes=self.samplerate)[:, 0]
                self.voices.append(newVoice)
                if self.isFinished:
                    break

    # 开始录制
    def start(self):
        thread = threading.Thread(target=self.__record)
        # 设置此线程被主线程回收
        thread.setDaemon(True)
        thread.start()

    # 结束录制、保存文件
    def save(self, path):
        time.sleep(0.5)
        self.isFinished = True
        if len(self.voices) == 0:
            return
        data = np.hstack(self.voices)
        if os.path.exists(path):
            os.remove(path)
        sf.write(path, data, self.samplerate)
