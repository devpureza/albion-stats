# Configurações globais do projeto

import os

def get_personagens():
    """Retorna a lista de personagens disponíveis"""
    return ["Przdecenoura", "CapetadeCenoura", "GordoDeCenoura", "FantasiaVH", "MagoRossi", "DPSdecenoura", "Rlove"]

def get_equipamentos(tipo):
    """
    Lê equipamentos de um arquivo txt
    tipo: 'armas', 'cabecas', 'armaduras', 'botas', 'capas', 'pocoes', 'comidas'
    """
    arquivo = f"data/equipamentos/{tipo}.txt"
    try:
        if not os.path.exists(arquivo):
            # Criar arquivo se não existir
            os.makedirs(os.path.dirname(arquivo), exist_ok=True)
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write('')
            return []
        
        with open(arquivo, 'r', encoding='utf-8') as f:
            # Remove linhas vazias e espaços em branco
            items = [line.strip() for line in f.readlines() if line.strip()]
            return sorted(items)
    except Exception as e:
        print(f"Erro ao ler arquivo {arquivo}: {str(e)}")
        return []

# Outras configurações globais podem ser adicionadas aqui
PAGINA_TITULO = "Albion Stats"
PAGINA_ICONE = "⚔️" 