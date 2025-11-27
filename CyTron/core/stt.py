# aiva_core/stt.py
import queue
import sounddevice as sd
import vosk
import json
import os

class STTEngine:
    def __init__(self, cfg):
        self.engine = cfg.get('engine','vosk')
        self.model_path = cfg.get('model_path','models/vosk/vn-model')
        if self.engine == 'vosk':
            if not os.path.exists(self.model_path):
                raise RuntimeError(f"VOSK model not found at {self.model_path}")
            self.model = vosk.Model(self.model_path)
        self.samplerate = 16000

    def listen_once(self, timeout=8):
        q = queue.Queue()
        rec = vosk.KaldiRecognizer(self.model, self.samplerate)

        def callback(indata, frames, time, status):
            if status:
                print(status, flush=True)
            q.put(bytes(indata))

        with sd.RawInputStream(samplerate=self.samplerate, blocksize = 8000, dtype='int16',
                               channels=1, callback=callback):
            print("Listening...")
            full = b''
            t0 = sd.get_stream().time
            while True:
                try:
                    data = q.get(timeout=timeout)
                except queue.Empty:
                    break
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    if res.get('text'):
                        return res['text']
                else:
                    # partial = json.loads(rec.PartialResult())
                    pass
            final = json.loads(rec.FinalResult())
            return final.get('text','')
