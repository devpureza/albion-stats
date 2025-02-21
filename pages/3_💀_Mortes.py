import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import get_db_connection, init_db
from config import get_personagens

st.set_page_config(page_title="Registro de Mortes!", page_icon="💀")

# Inicializar banco de dados
init_db()

# Função para carregar os dados do banco
def carregar_dados():
    try:
        with get_db_connection() as conn:
            query = "SELECT * FROM mortes ORDER BY data DESC"
            df = pd.read_sql_query(query, conn)
            # Converter a coluna de data para datetime e depois para o formato brasileiro
            df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
            return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(columns=['id', 'data', 'personagem', 'valor_perdido', 'descricao'])

# Função para salvar morte no banco
def salvar_morte(personagem, data, valor_perdido, descricao):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mortes (data, personagem, valor_perdido, descricao)
                VALUES (?, ?, ?, ?)
            """, (data.strftime('%Y-%m-%d'), personagem, valor_perdido, descricao))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

# Função para deletar uma morte do banco
def deletar_morte(id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mortes WHERE id = ?", (id,))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar registro: {str(e)}")
        return False

# Sidebar
with st.sidebar:
    st.title("Filtros")
    personagem_filtro = st.selectbox(
        "Personagem",
        options=["Todos"] + get_personagens()
    )
    data_inicio, data_fim = st.date_input(
        "Intervalo de Data",
        value=(datetime.now().date() - pd.Timedelta(days=30), datetime.now().date()),
        key="date_range"
    )

st.title("Registro de Mortes 💀")

# Área para adicionar nova morte
with st.expander("Registrar Nova Morte", expanded=True):
    personagem = st.selectbox(
        "Personagem",
        options=get_personagens()
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

# Exibir dataframe
st.dataframe(
    dados.drop('id', axis=1),  # Remove a coluna ID da visualização
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

# Análise de Perdas por Personagem
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