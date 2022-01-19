import os.path

import numpy as np
import soundcard as sc
import soundfile as sf
from scipy.io.wavfile import write
import threading
import time


class Recorder:
    samplerate = 16000
    isFinished = False
    voices = []

    def _record(self):
        mic = sc.get_microphone(sc.default_speaker().name, include_loopback=True)
        while True:
            newVoice = mic.record(samplerate=self.samplerate, numframes=self.samplerate)[:, 0]
            self.voices.append(newVoice)
            if self.isFinished:
                break

    def start(self):
        thread = threading.Thread(target=self._record)
        thread.start()

    def save(self, path):
        self.isFinished = True
        data = np.hstack(self.voices)
        if os.path.exists(path):
            os.remove(path)
        sf.write(path, data, self.samplerate)
