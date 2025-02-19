import streamlit as st

st.set_page_config(page_title="Hunts em Grupo", page_icon="👥")

# Sidebar
with st.sidebar:
    st.title("Filtros")
    data_filtro = st.date_input("Data")
    tamanho_grupo = st.slider("Tamanho do Grupo", 2, 20, 5)

st.title("Hunts em Grupo 👥")

# Área para adicionar nova hunt
with st.expander("Adicionar Nova Hunt em Grupo"):
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Data da Hunt")
        st.number_input("Fame Total", min_value=0)
    with col2:
        st.number_input("Número de Participantes", min_value=2, max_value=20)
        st.number_input("Valor Estimado por Pessoa (Silver)", min_value=0)
    
    st.button("Salvar Hunt")

# Tabela de hunts em grupo
st.subheader("Histórico de Hunts em Grupo")
