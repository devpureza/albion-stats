import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os
from config import get_personagens

st.set_page_config(page_title="Hunts Solo", page_icon="🎯")

# Função para carregar os dados do CSV
def carregar_dados():
    try:
        # Verificar se o arquivo existe
        if not os.path.exists('src/hunts_solo.csv'):
            # Criar arquivo com cabeçalho correto
            with open('src/hunts_solo.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['data', 'personagem', 'tipo_hunt', 'lucro_itens', 'descricao'])
            return pd.DataFrame(columns=['data', 'personagem', 'tipo_hunt', 'lucro_itens', 'descricao'])
        
        df = pd.read_csv('src/hunts_solo.csv')
        # Converter lucro_itens para numérico
        df['lucro_itens'] = pd.to_numeric(df['lucro_itens'], errors='coerce')
        # Converter data para datetime
        df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y', errors='coerce')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(columns=['data', 'personagem', 'tipo_hunt', 'lucro_itens', 'descricao'])

# Função para salvar dados no CSV
def salvar_hunt(data, personagem, tipo_hunt, lucro_itens, descricao):
    data_formatada = data.strftime('%d/%m/%Y')
    with open('src/hunts_solo.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([data_formatada, personagem, tipo_hunt, lucro_itens, descricao])
    return True

# Sidebar
with st.sidebar:
    st.title("Filtros")
    personagem_filtro = st.selectbox(
        "Personagem",
        options=["Todos"] + get_personagens()
    )
    tipo_hunt = st.selectbox("Tipo de Hunt", ["Todos", "Solo", "Corrupted", "HCE"])
    data_inicio, data_fim = st.date_input(
        "Intervalo de Data",
        value=(datetime.now(), datetime.now()),
        key="date_range"
    )

st.title("Hunts Solo 🎯")

# Área para adicionar nova hunt
with st.expander("Adicionar Nova Hunt", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data da Hunt")
        personagem = st.selectbox(
            "Personagem",
            options=get_personagens()
        )
    with col2:
        tipo_hunt = st.selectbox("Tipo", ["Solo", "Corrupted", "HCE"])
        lucro_itens = st.number_input("Lucro em Itens (Valor estimado)", min_value=0, step=1000)
    
    descricao = st.text_area("Descrição")
    
    if st.button("Salvar Hunt"):
        if salvar_hunt(data, personagem, tipo_hunt, lucro_itens, descricao):
            st.success("Hunt registrada com sucesso!")
            st.balloons()

# Exibir dados
st.subheader("Histórico de Hunts")
dados = carregar_dados()

# Aplicar filtros
if personagem_filtro != "Todos":
    dados = dados[dados['personagem'] == personagem_filtro]
if tipo_hunt != "Todos":
    dados = dados[dados['tipo_hunt'] == tipo_hunt]

# Aplicar filtro de data
dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y')
dados = dados[(dados['data'].dt.date >= data_inicio) & (dados['data'].dt.date <= data_fim)]
dados['data'] = dados['data'].dt.strftime('%d/%m/%Y')

# Exibir dataframe
st.dataframe(
    dados,
    use_container_width=True,
    hide_index=True,
    column_config={
        "data": "Data",
        "personagem": "Personagem",
        "tipo_hunt": "Tipo",
        "lucro_itens": st.column_config.NumberColumn(
            "Lucro em Itens",
            format="R$ %.2f",
            help="Lucro em Reais"
        ),
        "descricao": "Descrição"
    }
)

# Análises
st.subheader("Análise de Hunts")

# Gráfico de lucro por tipo e personagem
chart_data = dados.groupby(['personagem', 'tipo_hunt'])['lucro_itens'].sum().reset_index()
# Criar um pivot table para melhor visualização
chart_pivot = chart_data.pivot(index='tipo_hunt', columns='personagem', values='lucro_itens').fillna(0)

# Exibir o gráfico usando o pivot table
st.bar_chart(chart_pivot)

# Métricas totais
col1, col2 = st.columns(2)
with col1:
    st.metric("Lucro Total", f"R$ {dados['lucro_itens'].sum():,.2f}")
with col2:
    media_lucro = dados['lucro_itens'].mean()
    st.metric("Média de Lucro por Hunt", f"R$ {media_lucro:,.2f}")
