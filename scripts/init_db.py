import sqlite3
import os

def init_database():
    # Garantir que o diretório data existe
    os.makedirs('data', exist_ok=True)
    
    # Conectar ao banco de dados (cria se não existir)
    conn = sqlite3.connect('data/albion.db')
    cursor = conn.cursor()
    
    # Criar tabela de hunts solo
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
    
    # Criar tabela de hunts em grupo
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
    
    # Criar tabela de mortes
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
    conn.close()

if __name__ == "__main__":
    init_database()
    print("Banco de dados inicializado com sucesso!")