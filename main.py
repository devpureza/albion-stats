import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Albion Stats",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"  # Mantém o sidebar sempre aberto
)

# Customiza o título no menu
st.sidebar.header("📊 Dashboard")  # Isso vai aparecer no topo do sidebar

# Sidebar
with st.sidebar:
    st.write("Escolha uma opção abaixo:")
    
    # Você pode adicionar mais elementos ao sidebar aqui
    st.divider()
    st.write("Desenvolvido com ❤️ pelo przdeCenoura")

# Conteúdo principal
st.title("Dashboard Albion Stats ⚔️")

# Métricas principais
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total de Hunts Solo", value="0")
    
with col2:
    st.metric(label="Total de Hunts em Grupo", value="0")
    
with col3:
    st.metric(label="Total de Mortes", value="0")

# Gráfico exemplo
st.subheader("Atividades Recentes")
chart_data = {"Tipo": [], "Quantidade": []}
st.line_chart(chart_data)
