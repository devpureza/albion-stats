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
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            arma TEXT NOT NULL,
            secundaria TEXT,
            cabeca TEXT,
            peito TEXT,
            botas TEXT,
            capa TEXT,
            potion TEXT,
            food TEXT,
            notas TEXT,
            personagem TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()

def upgrade_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('ALTER TABLE builds ADD COLUMN secundaria TEXT')
            conn.commit()
        except sqlite3.OperationalError:
            # Coluna já existe
            pass 