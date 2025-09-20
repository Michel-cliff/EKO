import pvporcupine
import sounddevice as sd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class WakeWordDetector:
    def __init__(self, keyword="jarvis"):
        access_key = os.getenv("PICO_VOICE")
        if not access_key:
            raise ValueError("Missing PICO_VOICE in .env")

        self.porcupine = pvporcupine.create(
            access_key=access_key,
            keywords=[keyword]
        )
        self.sample_rate = 16000
        self.block_size = self.porcupine.frame_length
        self.on_wake = None

        # 👇 Force devices (0 = pulse input, 1 = default output)
        # sd.default.device = (0, 1)
        # print("✅ Default devices set to:", sd.default.device)

    def listen(self):
        print("🎤 Listening for wake word...")
        

        def callback(indata, frames, time, status):
            if status:
                print("SoundDevice error:", status)

            pcm = indata[:, 0].astype(np.int16)
            result = self.porcupine.process(pcm)
            if result >= 0 and self.on_wake:
                print("Wake word detected!")
                self.on_wake(indata.tobytes())

        with sd.InputStream(device=(0, 1),
                            samplerate=self.sample_rate,
                            channels=1,
                            blocksize=self.block_size,
                            dtype="int16",
                            callback=callback):
            sd.sleep(60 * 60 * 1000)  # 1h run
