import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os

st.set_page_config(page_title="Registro de Mortes!", page_icon="💀")

# Função para carregar os dados do CSV
def carregar_dados():
    try:
        df = pd.read_csv('data/mortes.csv')
        # Converte a coluna de data para datetime e depois para o formato brasileiro
        df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
        return df
    except:
        return pd.DataFrame(columns=['personagem', 'data', 'valor_perdido', 'descricao'])

# Função para salvar dados no CSV
def salvar_morte(personagem, data, valor_perdido, descricao):
    try:
        # Garantir que o diretório data existe
        os.makedirs('data', exist_ok=True)
        
        # Criar arquivo se não existir
        if not os.path.exists('data/mortes.csv'):
            with open('data/mortes.csv', 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['personagem', 'data', 'valor_perdido', 'descricao'])
        
        data_formatada = data.strftime('%d/%m/%Y')
        with open('data/mortes.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([personagem, data_formatada, valor_perdido, descricao])
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

# Função para deletar uma linha do CSV
def deletar_linha(index, df):
    try:
        # Remove a linha do DataFrame
        df = df.drop(index)
        # Salva o DataFrame atualizado no CSV
        df.to_csv('data/mortes.csv', index=False)
        return True
    except Exception as e:
        st.error(f"Erro ao deletar linha: {str(e)}")
        return False

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

# Exibir dados com botão de deletar
st.subheader("Histórico de Mortes")
dados = carregar_dados()

# Aplicar filtros
if personagem_filtro != "Todos":
    dados = dados[dados['personagem'] == personagem_filtro]

# Aplicar filtro de data
dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y')
dados = dados[(dados['data'].dt.date >= data_inicio) & (dados['data'].dt.date <= data_fim)]
dados['data'] = dados['data'].dt.strftime('%d/%m/%Y')

# Adicionar coluna com botão de deletar
dados_com_botao = dados.copy()
for idx in dados.index:
    if st.button("🗑️ Deletar", key=f"del_{idx}"):
        if deletar_linha(idx, dados):
            st.success("Registro deletado com sucesso!")
            st.rerun()

# Exibir dataframe
st.dataframe(
    dados,
    use_container_width=True,
    hide_index=True,
    column_config={
        "personagem": "Personagem",
        "data": "Data",
        "valor_perdido": st.column_config.NumberColumn(
            "Valor Perdido",
            format="R$ %.2f",
            help="Valor perdido em Reais"
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