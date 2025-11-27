# aiva_core/nlp_engine.py
class NLPEngine:
    def __init__(self, cfg, memory, tts=None):
        self.memory = memory
        self.tts = tts
        self.use_cloud = cfg.get('use_cloud_llm', False)

    def reply(self, text):
        # naive pipeline:
        # 1. search memory for related notes
        related = self.memory.search(text, k=3)
        context = "\n".join([r['text'] for r in related])
        # 2. very simple rule-based or local small LLM (placeholder)
        if 'dạy' in text or 'giải thích' in text:
            return "Mình sẽ dạy bạn: (ví dụ) Đây là ý chính: " + (context or "Không có nội dung liên quan trong ký ức.")
        if 'tình hình sức khỏe' in text or 'báo cáo' in text:
            return "Mình đang tổng hợp báo cáo sức khỏe... (xem dữ liệu trong memory)."
        # fallback: simple echo with context
        return f"Bạn hỏi: {text}. Mình tìm được: {context or 'Không có dữ liệu liên quan.'}"
