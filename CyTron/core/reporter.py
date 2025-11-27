# aiva_core/reporter.py
from datetime import datetime, timedelta

class Reporter:
    def __init__(self, memory, cfg):
        self.memory = memory
        self.cfg = cfg

    def generate(self, typ='daily'):
        # simple aggregator: read last N notes
        conn = self.memory.conn
        c = conn.cursor()
        if typ == 'daily':
            c.execute("SELECT role,text,ts FROM notes WHERE ts >= datetime('now','-1 day') ORDER BY ts DESC")
        elif typ == 'weekly':
            c.execute("SELECT role,text,ts FROM notes WHERE ts >= datetime('now','-7 day') ORDER BY ts DESC")
        else:
            c.execute("SELECT role,text,ts FROM notes ORDER BY ts DESC LIMIT 100")
        rows = c.fetchall()
        if not rows:
            return "Không có dữ liệu."
        lines = [f"{r[2]} [{r[0]}] {r[1]}" for r in rows]
        header = f"Report {typ} - {datetime.now().isoformat()}\n"
        return header + "\n".join(lines)
