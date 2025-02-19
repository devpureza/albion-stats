import streamlit as st

st.set_page_config(page_title="Hunts Solo", page_icon="🎯")

# Sidebar
with st.sidebar:
    st.title("Filtros")
    data_filtro = st.date_input("Data")
    tipo_dungeon = st.selectbox("Tipo de Dungeon", ["Todos", "Solo", "Corrupted", "HCE"])

st.title("Hunts Solo 🎯")

# Área para adicionar nova hunt
with st.expander("Adicionar Nova Hunt"):
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("Data da Hunt")
        st.number_input("Fame Total", min_value=0)
    with col2:
        st.selectbox("Tipo", ["Solo", "Corrupted", "HCE"])
        st.number_input("Valor Estimado (Silver)", min_value=0)
    
    st.button("Salvar Hunt")

# Tabela de hunts
st.subheader("Histórico de Hunts")
