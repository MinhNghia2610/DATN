# aiva_core/memory.py
import sqlite3
import os
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle

class Memory:
    def __init__(self, cfg):
        self.db_path = cfg.get('db_path','data/aiva_memory.db')
        self.index_path = cfg.get('faiss_index_path','data/faiss.index')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._ensure_tables()
        self.model = SentenceTransformer(cfg.get('embedding_model','paraphrase-MiniLM-L6-v2'))
        self.dim = self.model.get_sentence_embedding_dimension()
        if os.path.exists(self.index_path):
            self.index = faiss.read_index(self.index_path)
            with open(self.index_path + '.meta','rb') as f:
                self.meta = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.meta = []  # parallel list of metadata

    def _ensure_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, text TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)''')
        self.conn.commit()

    def add_conversation(self, role, text):
        c = self.conn.cursor()
        c.execute('INSERT INTO notes (role,text) VALUES (?,?)',(role,text))
        self.conn.commit()
        # add to vector index
        emb = self.model.encode([text])
        self.index.add(np.array(emb).astype('float32'))
        self.meta.append({'role': role, 'text': text})
        self._save_index()

    def search(self, query, k=5):
        emb = self.model.encode([query]).astype('float32')
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(np.array(emb), k)
        results = []
        for idx in I[0]:
            if idx < len(self.meta):
                results.append(self.meta[idx])
        return results

    def _save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + '.meta','wb') as f:
            pickle.dump(self.meta, f)
