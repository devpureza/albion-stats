# Configurações globais do projeto

import os
import json

def get_personagens():
    """Retorna a lista de personagens disponíveis"""
    return ["Przdecenoura", "CapetadeCenoura", "GordoDeCenoura", "FantasiaVH", "MagoRossi", "DPSdecenoura", "Rlove", "Digeon"]

def get_equipamentos(tipo):
    """
    Lê equipamentos do arquivo equipment_mapping.json
    tipo: 'armas', 'cabecas', 'armaduras', 'botas', 'capas', 'pocoes', 'comidas', 'secundaria'
    """
    arquivo = "data/equipment_mapping.json"
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Mapeia os tipos em português para as chaves do JSON
            tipo_map = {
                'cabecas': 'cabecas',
                'armaduras': 'armaduras',
                'botas': 'botas',
                'armas': 'armas',
                'secundaria': 'secundaria',
                'capas': 'capas',
                'pocoes': 'pocoes',
                'comidas': 'comidas'
            }
            
            # Pega os items da categoria correta
            items = data.get(tipo_map[tipo], [])
            # Retorna lista de dicionários com nome e id
            return sorted(items, key=lambda x: x['name'])
            
    except Exception as e:
        print(f"Erro ao ler arquivo {arquivo}: {str(e)}")
        return []

# Outras configurações globais podem ser adicionadas aqui
PAGINA_TITULO = "Albion Stats"
PAGINA_ICONE = "⚔️" 