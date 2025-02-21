import streamlit as st
from config import PAGINA_TITULO, PAGINA_ICONE
from database import get_db_connection
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title=PAGINA_TITULO,
    page_icon=PAGINA_ICONE,
    layout="wide",
    initial_sidebar_state="expanded"  # Mantém o sidebar sempre aberto
)
# Sidebar
with st.sidebar:
    st.write("Desenvolvido com ❤️ pelo przdeCenoura")

# Estilo CSS personalizado
st.markdown("""
<style>
.metric-card {
    background-color: #1e1e1e;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #4e4e4e;
    text-align: center;
    transition: transform 0.2s;
}
.metric-card:hover {
    transform: translateY(-5px);
    border-color: #00ff88;
    box-shadow: 0 5px 15px rgba(0, 255, 136, 0.2);
}
.metric-label {
    color: #00ff88;
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 10px;
}
.metric-value {
    color: white;
    font-size: 2em;
    font-weight: bold;
}
.main-title {
    text-align: center;
    color: #00ff88;
    padding: 20px;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# Título principal estilizado
st.markdown("<h1 class='main-title'>Dashboard Albion Stats ⚔️</h1>", unsafe_allow_html=True)

# Funções para buscar estatísticas
def get_total_hunts_solo():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM hunts_solo")
            return cursor.fetchone()[0]
    except Exception:
        return 0

def get_total_hunts_grupo():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM hunts_grupo")
            return cursor.fetchone()[0]
    except Exception:
        return 0

def get_total_mortes():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM mortes")
            return cursor.fetchone()[0]
    except Exception:
        return 0

# Métricas principais com cards estilizados
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total de Hunts Solo</div>
        <div class="metric-value">{get_total_hunts_solo()}</div>
    </div>
    """, unsafe_allow_html=True)
    
with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total de Hunts em Grupo</div>
        <div class="metric-value">{get_total_hunts_grupo()}</div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total de Mortes</div>
        <div class="metric-value">{get_total_mortes()}</div>
    </div>
    """, unsafe_allow_html=True)

# Gráfico de atividades recentes
st.markdown("<h2 style='color: #00ff88; margin-top: 40px;'>Atividades Recentes</h2>", unsafe_allow_html=True)

# Buscar dados para o gráfico
try:
    with get_db_connection() as conn:
        # Últimos 30 dias de atividades
        df_solo = pd.read_sql("""
            SELECT date(data) as data, COUNT(*) as quantidade, 'Solo' as tipo
            FROM hunts_solo
            WHERE data >= date('now', '-30 days')
            GROUP BY date(data)
        """, conn)
        
        df_grupo = pd.read_sql("""
            SELECT date(data) as data, COUNT(*) as quantidade, 'Grupo' as tipo
            FROM hunts_grupo
            WHERE data >= date('now', '-30 days')
            GROUP BY date(data)
        """, conn)
        
        df_mortes = pd.read_sql("""
            SELECT date(data) as data, COUNT(*) as quantidade, 'Morte' as tipo
            FROM mortes
            WHERE data >= date('now', '-30 days')
            GROUP BY date(data)
        """, conn)
        
        # Combinar todos os dados
        df_chart = pd.concat([df_solo, df_grupo, df_mortes])
        df_chart['data'] = pd.to_datetime(df_chart['data'])
        
        # Criar gráfico
        chart_data = pd.pivot_table(
            df_chart,
            values='quantidade',
            index='data',
            columns='tipo',
            fill_value=0
        )
        
        st.line_chart(chart_data)
except Exception as e:
    st.error(f"Erro ao carregar o gráfico: {str(e)}")
