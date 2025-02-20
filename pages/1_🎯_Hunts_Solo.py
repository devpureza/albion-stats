import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_db_connection, init_db
from config import get_personagens

st.set_page_config(page_title="Hunts Solo", page_icon="🎯")

# Inicializar banco de dados
init_db()

# Função para carregar os dados do banco
def carregar_dados():
    try:
        with get_db_connection() as conn:
            query = "SELECT * FROM hunts_solo ORDER BY data DESC"
            df = pd.read_sql_query(query, conn)
            # Converter a coluna de data para datetime e depois para o formato brasileiro
            df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
            return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(columns=['id', 'data', 'personagem', 'tipo_hunt', 'lucro_itens', 'descricao'])

# Função para salvar hunt no banco
def salvar_hunt(data, personagem, tipo_hunt, lucro_itens, descricao):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO hunts_solo (data, personagem, tipo_hunt, lucro_itens, descricao)
                VALUES (?, ?, ?, ?, ?)
            """, (data.strftime('%Y-%m-%d'), personagem, tipo_hunt, lucro_itens, descricao))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        return False

# Função para deletar uma hunt do banco
def deletar_hunt(id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hunts_solo WHERE id = ?", (id,))
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

# Adicionar coluna com botão de deletar
for idx, row in dados.iterrows():
    if st.button("🗑️ Deletar", key=f"del_{row['id']}"):
        if deletar_hunt(row['id']):
            st.success("Registro deletado com sucesso!")
            st.rerun()

# Exibir dataframe
st.dataframe(
    dados.drop('id', axis=1),  # Remove a coluna ID da visualização
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
