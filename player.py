import os.path
import threading
import time

import numpy as np
import soundcard as sc
import soundfile as sf


class Player:

    def __init__(self, path):
        self.isFinished = False
        self.path = path

    def __speak(self):
        speaker = sc.default_speaker()
        data, samplerate = sf.read(self.path)
        with speaker.player(samplerate=samplerate) as player:
            second = 0
            while True:
                subDate = data[second * samplerate:(second + 1) * samplerate]
                if len(subDate) == 0:
                    break
                player.play(subDate)
                if self.isFinished:
                    break
                second += 1

    def start(self):
        thread = threading.Thread(target=self.__speak)
        # 设置此线程被主线程回收
        # thread.setDaemon(True)
        thread.start()

    def stop(self):
        self.isFinished = True
