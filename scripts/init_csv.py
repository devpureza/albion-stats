import os
import csv

# Garantir que o diretório data existe
os.makedirs('data', exist_ok=True)

# Criar hunts_solo.csv
with open('data/hunts_solo.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['data', 'personagem', 'tipo_hunt', 'lucro_itens', 'descricao'])

# Criar hunts_grupo.csv
with open('data/hunts_grupo.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['data', 'personagens', 'valor_total', 'observacoes'])

# Criar mortes.csv
with open('data/mortes.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['personagem', 'data', 'valor_perdido', 'descricao']) 