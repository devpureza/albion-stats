import streamlit as st
import pandas as pd
from datetime import datetime
import os
from database import get_db_connection, init_db
from config import get_personagens

st.set_page_config(page_title="Registro de Mortes!", page_icon="💀", layout='wide')

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

st.title("Registro de Mortes 💀")

# Área para adicionar nova morte
with st.expander("Registrar Nova Morte", expanded=False):
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

st.markdown("""
<style>
.ranking-container {
    background-color: #1a1a1a;
    border-radius: 10px;
    padding: 15px;
    margin: 5px;
}
.ranking-item {
    display: flex;
    align-items: center;
    padding: 10px;
    margin: 5px 0;
    background-color: #2d2d2d;
    border-radius: 8px;
    transition: transform 0.2s;
}
.ranking-item:hover {
    transform: translateX(5px);
}
.medal {
    font-size: 24px;
    margin-right: 15px;
    min-width: 30px;
}
.position {
    font-size: 18px;
    margin-right: 15px;
    color: #666;
    min-width: 20px;
}
.player-name {
    flex-grow: 1;
    font-size: 16px;
    color: #ffffff;
}
.value {
    font-size: 16px;
    color: #00ff00;
    margin-left: 10px;
}
</style>
""", unsafe_allow_html=True)

# Função para obter emoji da medalha
def get_medal(position):
    if position == 0:
        return "🥇"
    elif position == 1:
        return "🥈"
    elif position == 2:
        return "🥉"
    return "🏅"

# Função para formatar valores
def formatar_valor(valor):
    if valor >= 1000000000:
        return f"{valor/1000000000:.1f}B"
    elif valor >= 1000000:
        return f"{valor/1000000:.1f}M"
    elif valor >= 1000:
        return f"{valor/1000:.1f}K"
    return f"{valor:.0f}"

# Preparar dados para os rankings
dados = carregar_dados()
ranking_mortes = dados['personagem'].value_counts().reset_index()
ranking_mortes.columns = ['Personagem', 'Quantidade de Mortes']
ranking_mortes = ranking_mortes.head(10)  # Limitar para top 10

# Adicionar mensagem de parabéns para quem mais morreu
if not ranking_mortes.empty:
    campeao_mortes = ranking_mortes.iloc[0]['Personagem']
    # st.toast(f"🏆 Parabéns {campeao_mortes}, você é o que mais morreu!", icon="🎉")
    st.markdown(f"""
        <div style='padding: 20px; 
                    background-color: #1e1e1e; 
                    border-radius: 10px; 
                    text-align: center;
                    margin: 20px 0;
                    font-size: 24px;
                    animation: pulse 2s infinite;'>
            🏆 Parabéns <span style='color: #00ff00;'>{campeao_mortes}</span>!<br>
            Você é o campeão de mortes! 💀
        </div>
        <style>
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
        </style>
    """, unsafe_allow_html=True)
    st.balloons()

ranking_valores = dados.groupby('personagem')['valor_perdido'].sum().reset_index()
ranking_valores = ranking_valores.sort_values('valor_perdido', ascending=False)
ranking_valores = ranking_valores.head(10)  # Limitar para top 10
ranking_valores.columns = ['Personagem', 'Valor Total Perdido']

# Criar duas colunas para os rankings
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ranking de Mortes")
    for i, row in ranking_mortes.iterrows():
        st.markdown(f"""
        <div class="ranking-container">
            <div class="ranking-item">
                <div class="medal">{get_medal(i)}</div>
                <div class="position">#{i+1}</div>
                <div class="player-name">{row['Personagem']}</div>
                <div class="value">{row['Quantidade de Mortes']} mortes</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("Ranking de Valores Perdidos")
    for i, row in ranking_valores.iterrows():
        valor_formatado = formatar_valor(row['Valor Total Perdido'])
        st.markdown(f"""
        <div class="ranking-container">
            <div class="ranking-item">
                <div class="medal">{get_medal(i)}</div>
                <div class="position">#{i+1}</div>
                <div class="player-name">{row['Personagem']}</div>
                <div class="value">{valor_formatado}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
st.metric("Total de Perdas no Período", formatar_valor(total_perdas)) 