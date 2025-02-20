import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os

st.set_page_config(page_title="Registro de Mortes", page_icon="💀")

# Função para carregar os dados do CSV
def carregar_dados():
    try:
        df = pd.read_csv('src/mortes.csv')
        # Converte a coluna de data para datetime e depois para o formato brasileiro
        df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
        return df
    except:
        return pd.DataFrame(columns=['personagem', 'data', 'valor_perdido', 'descricao'])

# Função para salvar dados no CSV
def salvar_morte(personagem, data, valor_perdido, descricao):
    # Converte a data para o formato brasileiro antes de salvar
    data_formatada = data.strftime('%d/%m/%Y')
    with open('src/mortes.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([personagem, data_formatada, valor_perdido, descricao])
    return True

# Sidebar
with st.sidebar:
    st.title("Filtros")
    personagem_filtro = st.selectbox(
        "Personagem",
        options=["Todos", "Przdecenoura", "Capetadecenoura", "Mouzindecenoura"]
    )
    data_inicio, data_fim = st.date_input(
        "Intervalo de Data",
        value=(datetime.now(), datetime.now()),
        key="date_range"
    )

st.title("Registro de Mortes 💀")

# Área para adicionar nova morte
with st.expander("Registrar Nova Morte", expanded=True):
    personagem = st.selectbox(
        "Personagem",
        options=["Przdecenoura", "Capetadecenoura", "Mouzindecenoura"]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data da Morte")
    with col2:
        valor_perdido = st.number_input("Valor Perdido (Sets + prata)", min_value=0, step=1000)
    
    descricao = st.text_area("Descrição/Observações")
    
    if st.button("Salvar Registro"):
        if salvar_morte(personagem, data, valor_perdido, descricao):
            st.success("Morte registrada com sucesso!")
            st.balloons()

# Exibir dados
st.subheader("Histórico de Mortes")
dados = carregar_dados()

# Aplicar filtros
if personagem_filtro != "Todos":
    dados = dados[dados['personagem'] == personagem_filtro]

# Aplicar filtro de data
dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y')
dados = dados[(dados['data'].dt.date >= data_inicio) & (dados['data'].dt.date <= data_fim)]
dados['data'] = dados['data'].dt.strftime('%d/%m/%Y')

st.dataframe(
    dados,
    use_container_width=True,  # Faz o dataframe usar toda a largura disponível
    hide_index=True,           # Esconde a coluna de índice
    column_config={
        "personagem": "Personagem",
        "data": "Data",
        "valor_perdido": st.column_config.NumberColumn(
            "Valor Perdido",
            format="R$ %.2f",  # Alterado para mostrar decimais
            help="Valor perdido em Reais"  # Alterado de Silver para Reais
        ),
        "descricao": "Descrição"
    }
)

# Após o dataframe, adicionar o gráfico
st.subheader("Análise de Perdas por Personagem")

# Preparar dados para o gráfico
chart_data = dados.groupby('personagem')['valor_perdido'].sum().reset_index()

# Criar gráfico de barras
st.bar_chart(
    chart_data,
    x='personagem',
    y='valor_perdido',
    use_container_width=True
)

# Mostrar total de perdas no período
total_perdas = dados['valor_perdido'].sum()
st.metric("Total de Perdas no Período", f"R$ {total_perdas:,.2f}") 