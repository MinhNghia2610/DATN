# aiva_core/controller.py
import threading
import time
from .stt import STTEngine
from .tts import TTSEngine
from .nlp_engine import NLPEngine
from .memory import Memory
from .collector import Collector
from .reporter import Reporter

class AivaController:
    def __init__(self, config):
        self.config = config
        self.tts = TTSEngine(config['tts'])
        self.stt = STTEngine(config['stt'])
        self.memory = Memory(config['memory'])
        self.nlp = NLPEngine(config['nlp'], self.memory, tts=self.tts)
        self.collector = Collector(config['collector'], self.memory)
        self.reporter = Reporter(self.memory, config['report'])
        self.running = False

    def start_interactive_loop(self):
        print(f"Starting {self.config['assistant']['name']} interactive loop...")
        self.running = True
        # start background collector
        if self.config['assistant'].get('auto_collect', True):
            t = threading.Thread(target=self.collector.start_schedule, daemon=True)
            t.start()
        try:
            while self.running:
                print("\nLắng nghe (gõ 'exit' để thoát, 'listen' để capture voice, 'cmd:' để gửi lệnh):")
                cmd = input("> ").strip()
                if not cmd:
                    continue
                if cmd.lower() in ('exit','quit'):
                    self.running = False
                    break
                if cmd.startswith('listen'):
                    print("Đang nghe giọng (nói vào micro)...")
                    text = self.stt.listen_once()
                    print("Bạn nói:", text)
                    self.memory.add_conversation("user", text)
                    resp = self.nlp.reply(text)
                    print("AIVA:", resp)
                    self.tts.speak(resp)
                elif cmd.startswith('cmd:'):
                    code = cmd[len('cmd:'):].strip()
                    # very simple eval (you can extend with safe sandbox)
                    try:
                        exec(code, {'controller': self, 'memory': self.memory})
                    except Exception as e:
                        print("Lỗi khi chạy lệnh:", e)
                else:
                    # free text chat
                    self.memory.add_conversation("user", cmd)
                    resp = self.nlp.reply(cmd)
                    print("AIVA:", resp)
                    self.tts.speak(resp)
        except KeyboardInterrupt:
            print("Stopped.")

    def run_report(self, typ='daily'):
        print("Generating report:", typ)
        text = self.reporter.generate(typ)
        print(text)
