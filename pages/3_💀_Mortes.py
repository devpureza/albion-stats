import streamlit as st

st.set_page_config(page_title="Registro de Mortes", page_icon="💀")

# Sidebar
with st.sidebar:
    st.title("Filtros")
    data_filtro = st.date_input("Data")
    tipo_morte = st.selectbox("Tipo de Morte", ["Todas", "PvP", "PvE", "Gank"])

st.title("Registro de Mortes 💀")

# Área para adicionar nova morte
with st.expander("Registrar Nova Morte"):
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Data da Morte")
        st.selectbox("Tipo", ["PvP", "PvE", "Gank"])
    with col2:
        st.number_input("Valor Perdido (Silver)", min_value=0)
        st.text_input("Localização")
    
    st.text_area("Descrição/Observações")
    st.button("Salvar Registro")

# Tabela de mortes
st.subheader("Histórico de Mortes") 