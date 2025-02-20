import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = 'data/albion.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    os.makedirs('data', exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Criar tabelas se não existirem
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hunts_solo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            personagem TEXT NOT NULL,
            tipo_hunt TEXT NOT NULL,
            lucro_itens REAL NOT NULL,
            descricao TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS hunts_grupo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            personagens TEXT NOT NULL,
            valor_total REAL NOT NULL,
            observacoes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mortes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE NOT NULL,
            personagem TEXT NOT NULL,
            valor_perdido REAL NOT NULL,
            descricao TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit() 