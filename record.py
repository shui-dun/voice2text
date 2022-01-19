import os.path
import threading

import numpy as np
import soundcard as sc
import soundfile as sf


class Recorder:
    # 采样频率
    samplerate = 16000

    # 是否完成
    isFinished = False

    # 音频片段列表
    voices = []

    def _record(self):
        mic = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
        while True:
            newVoice = mic.record(samplerate=self.samplerate, numframes=self.samplerate)[:, 0]
            self.voices.append(newVoice)
            if self.isFinished:
                break

    # 开始录制
    def start(self):
        thread = threading.Thread(target=self._record)
        # 设置此线程被主线程回收
        thread.setDaemon(True)
        thread.start()

    # 结束录制、保存文件
    def save(self, path):
        self.isFinished = True
        if len(self.voices) == 0:
            return
        data = np.hstack(self.voices)
        if os.path.exists(path):
            os.remove(path)
        sf.write(path, data, self.samplerate)
