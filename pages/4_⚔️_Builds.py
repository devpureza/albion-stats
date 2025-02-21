import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_db_connection, init_db
from config import get_personagens, get_equipamentos

st.set_page_config(page_title="Builds", page_icon="⚔️", layout="wide")

# Inicializar banco de dados
init_db()

# Funções do banco de dados
def carregar_builds():
    try:
        with get_db_connection() as conn:
            query = "SELECT * FROM builds ORDER BY tipo, nome"
            return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro ao carregar builds: {str(e)}")
        return pd.DataFrame()

def salvar_build(nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO builds (nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar build: {str(e)}")
        return False

def atualizar_build(id, nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE builds 
                SET nome=?, tipo=?, arma=?, cabeca=?, peito=?, botas=?, capa=?, potion=?, food=?, notas=?, personagem=?
                WHERE id=?
            """, (nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem, id))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar build: {str(e)}")
        return False

def deletar_build(id):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM builds WHERE id=?", (id,))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar build: {str(e)}")
        return False

# Estilo CSS personalizado
st.markdown("""
<style>
.build-card {
    background-color: #1e1e1e;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #4e4e4e;
    margin-bottom: 20px;
}
.build-card:hover {
    border-color: #00ff88;
    box-shadow: 0 5px 15px rgba(0, 255, 136, 0.2);
}
.build-title {
    color: #00ff88;
    font-size: 1.5em;
    font-weight: bold;
    margin-bottom: 15px;
}
.build-info {
    color: white;
    margin-bottom: 10px;
}
.equipment-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 10px;
    margin: 10px 0;
}
.equipment-item {
    background-color: #2a2a2a;
    padding: 8px;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Filtros")
    tipo_filtro = st.selectbox(
        "Tipo de Conteúdo",
        options=["Todos", "PvE Solo", "PvE Grupo", "PvP Solo", "PvP Grupo", "ZvZ"]
    )
    personagem_filtro = st.selectbox(
        "Personagem",
        options=["Todos"] + get_personagens()
    )

st.title("Builds ⚔️")

# Área para adicionar nova build
with st.expander("Adicionar Nova Build", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome da Build")
        tipo = st.selectbox(
            "Tipo de Conteúdo",
            ["PvE Solo", "PvE Grupo", "PvP Solo", "PvP Grupo", "ZvZ"]
        )
        personagem = st.selectbox(
            "Personagem Principal",
            get_personagens()
        )
    
    with col2:
        arma = st.selectbox(
            "Arma Principal",
            options=[""] + get_equipamentos("armas"),
            format_func=lambda x: "Selecione uma arma" if x == "" else x
        )
        cabeca = st.selectbox(
            "Cabeça",
            options=[""] + get_equipamentos("cabecas"),
            format_func=lambda x: "Selecione um capacete" if x == "" else x
        )
        peito = st.selectbox(
            "Armadura",
            options=[""] + get_equipamentos("armaduras"),
            format_func=lambda x: "Selecione uma armadura" if x == "" else x
        )
        botas = st.selectbox(
            "Botas",
            options=[""] + get_equipamentos("botas"),
            format_func=lambda x: "Selecione uma bota" if x == "" else x
        )
    
    col3, col4 = st.columns(2)
    with col3:
        capa = st.selectbox(
            "Capa",
            options=[""] + get_equipamentos("capas"),
            format_func=lambda x: "Selecione uma capa" if x == "" else x
        )
        potion = st.selectbox(
            "Poção",
            options=[""] + get_equipamentos("pocoes"),
            format_func=lambda x: "Selecione uma poção" if x == "" else x
        )
    with col4:
        food = st.selectbox(
            "Comida",
            options=[""] + get_equipamentos("comidas"),
            format_func=lambda x: "Selecione uma comida" if x == "" else x
        )
    
    notas = st.text_area("Notas/Observações")
    
    if st.button("Salvar Build"):
        if nome and arma:  # Validação básica
            if salvar_build(nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem):
                st.success("Build salva com sucesso!")
                st.balloons()
        else:
            st.error("Nome da build e arma principal são obrigatórios!")

# Exibir builds
st.subheader("Builds Salvas")

builds = carregar_builds()

# Aplicar filtros
if tipo_filtro != "Todos":
    builds = builds[builds['tipo'] == tipo_filtro]
if personagem_filtro != "Todos":
    builds = builds[builds['personagem'] == personagem_filtro]

# Adicionar lógica de edição no topo do arquivo, após as importações:
if 'editing_build' in st.session_state:
    build = st.session_state.editing_build
    st.subheader(f"Editando: {build['nome']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome da Build", value=build['nome'], key="edit_nome")
        tipo = st.selectbox("Tipo de Conteúdo", 
            ["PvE Solo", "PvE Grupo", "PvP Solo", "PvP Grupo", "ZvZ"],
            index=["PvE Solo", "PvE Grupo", "PvP Solo", "PvP Grupo", "ZvZ"].index(build['tipo']),
            key="edit_tipo")
        personagem = st.selectbox("Personagem Principal", 
            get_personagens(),
            index=get_personagens().index(build['personagem']),
            key="edit_personagem")
    
    with col2:
        arma = st.selectbox("Arma Principal", 
            options=[""] + get_equipamentos("armas"),
            index=get_equipamentos("armas").index(build['arma']) + 1,
            key="edit_arma")
        cabeca = st.selectbox("Cabeça",
            options=[""] + get_equipamentos("cabecas"),
            index=(get_equipamentos("cabecas").index(build['cabeca']) + 1) if build['cabeca'] else 0,
            key="edit_cabeca")
        peito = st.selectbox("Armadura",
            options=[""] + get_equipamentos("armaduras"),
            index=(get_equipamentos("armaduras").index(build['peito']) + 1) if build['peito'] else 0,
            key="edit_peito")
        botas = st.selectbox("Botas",
            options=[""] + get_equipamentos("botas"),
            index=(get_equipamentos("botas").index(build['botas']) + 1) if build['botas'] else 0,
            key="edit_botas")
    
    col3, col4 = st.columns(2)
    with col3:
        capa = st.selectbox("Capa",
            options=[""] + get_equipamentos("capas"),
            index=(get_equipamentos("capas").index(build['capa']) + 1) if build['capa'] else 0,
            key="edit_capa")
        potion = st.selectbox("Poção",
            options=[""] + get_equipamentos("pocoes"),
            index=(get_equipamentos("pocoes").index(build['potion']) + 1) if build['potion'] else 0,
            key="edit_potion")
    with col4:
        food = st.selectbox("Comida",
            options=[""] + get_equipamentos("comidas"),
            index=(get_equipamentos("comidas").index(build['food']) + 1) if build['food'] else 0,
            key="edit_food")
    
    notas = st.text_area("Notas/Observações", value=build['notas'], key="edit_notas")
    
    col5, col6 = st.columns(2)
    with col5:
        if st.button("Salvar Alterações"):
            if nome and arma:
                if atualizar_build(build['id'], nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem):
                    st.success("Build atualizada com sucesso!")
                    del st.session_state.editing_build
                    st.rerun()
    with col6:
        if st.button("Cancelar Edição"):
            del st.session_state.editing_build
            st.rerun()

# Exibir builds em dropdowns
for _, build in builds.iterrows():
    with st.expander(f"📋 {build['nome']} - {build['tipo']} ({build['personagem']})", expanded=False):
        col1, col2 = st.columns([0.85, 0.15])
        
        with col1:
            st.markdown(f"""
            <div class="build-card">
                <div class="equipment-section">
                    <div class="equipment-item">🗡️ Arma: {build['arma']}</div>
                    <div class="equipment-item">🎭 Cabeça: {build['cabeca']}</div>
                    <div class="equipment-item">👕 Armadura: {build['peito']}</div>
                    <div class="equipment-item">👢 Botas: {build['botas']}</div>
                    <div class="equipment-item">🎭 Capa: {build['capa']}</div>
                    <div class="equipment-item">🧪 Poção: {build['potion']}</div>
                    <div class="equipment-item">🍖 Comida: {build['food']}</div>
                </div>
                
                <div class="build-info">
                    <strong>Notas:</strong><br>
                    {build['notas'] if build['notas'] else 'Nenhuma nota adicional.'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("✏️ Editar", key=f"edit_{build['id']}"):
                st.session_state.editing_build = build
                st.rerun()
            
            if st.button("🗑️ Deletar", key=f"delete_{build['id']}"):
                if deletar_build(build['id']):
                    st.success("Build deletada com sucesso!")
                    st.rerun() 