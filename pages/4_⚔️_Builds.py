import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_db_connection, init_db, upgrade_db
from config import get_personagens, get_equipamentos

st.set_page_config(page_title="Builds", page_icon="⚔️", layout="wide")

# Inicializar e atualizar banco de dados
init_db()
upgrade_db()

# Adicionar constante para a URL base
ALBION_RENDER_URL = "https://render.albiononline.com/v1/item/"

# Função para converter nome do item para ID do Albion
def get_item_id(item_name):
    if not item_name:  # Se o item estiver vazio
        return None
        
    # Procurar o item em todas as categorias
    categorias = ['armas', 'cabecas', 'armaduras', 'botas', 'capas', 'pocoes', 'comidas', 'secundaria']
    
    for categoria in categorias:
        items = get_equipamentos(categoria)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get('name') == item_name:
                    return item.get('id')
    
    return None

# Funções do banco de dados
def carregar_builds():
    try:
        with get_db_connection() as conn:
            query = "SELECT * FROM builds ORDER BY tipo, nome"
            return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Erro ao carregar builds: {str(e)}")
        return pd.DataFrame()

def salvar_build(nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem, secundaria):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO builds (nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem, secundaria)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem, secundaria))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar build: {str(e)}")
        return False

def atualizar_build(id, nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem, secundaria):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE builds 
                SET nome=?, tipo=?, arma=?, cabeca=?, peito=?, botas=?, capa=?, potion=?, food=?, notas=?, personagem=?, secundaria=?
                WHERE id=?
            """, (nome, tipo, arma, cabeca, peito, botas, capa, potion, food, notas, personagem, secundaria, id))
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

# Adicionar/modificar o CSS
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
    margin-top: 20px;
    padding: 15px;
    background-color: #2a2a2a;
    border-radius: 5px;
    color: #ffffff;
    white-space: pre-wrap;
    word-wrap: break-word;
}
.build-info strong {
    color: #00ff88;
    font-size: 1.1em;
}
.build-info br {
    display: block;
    margin: 5px 0;
}
.equipment-section {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 15px;
    margin: 10px 0;
    max-width: 400px;
    margin: 0 auto;
}
.equipment-item {
    background-color: #2a2a2a;
    padding: 10px;
    border-radius: 5px;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    aspect-ratio: 1;
    position: relative;
}
.equipment-img {
    width: 96px;
    height: 96px;
    margin: 0 auto;
}
.equipment-name {
    font-size: 0.8em;
    color: #ffffff;
    text-align: center;
    word-wrap: break-word;
}
.tooltip-trigger {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    cursor: help;
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
        armas = get_equipamentos("armas")
        arma = st.selectbox(
            "Arma Principal",
            options=[{"name": "", "id": ""}] + armas,
            format_func=lambda x: "Selecione uma arma" if not x or x.get("name") == "" else x.get("name"),
            key="arma"
        )
        secundarias = get_equipamentos("secundaria")
        secundaria = st.selectbox(
            "Mão Secundária",
            options=[{"name": "", "id": ""}] + secundarias,
            format_func=lambda x: "Selecione item secundário" if not x or x.get("name") == "" else x.get("name"),
            key="secundaria"
        )
        cabecas = get_equipamentos("cabecas")
        cabeca = st.selectbox(
            "Cabeça",
            options=[{"name": "", "id": ""}] + cabecas,
            format_func=lambda x: "Selecione um capacete" if not x or x.get("name") == "" else x.get("name"),
            key="cabeca"
        )
        armaduras = get_equipamentos("armaduras")
        peito = st.selectbox(
            "Armadura",
            options=[{"name": "", "id": ""}] + armaduras,
            format_func=lambda x: "Selecione uma armadura" if not x or x.get("name") == "" else x.get("name"),
            key="peito"
        )
        botas_list = get_equipamentos("botas")
        botas = st.selectbox(
            "Botas",
            options=[{"name": "", "id": ""}] + botas_list,
            format_func=lambda x: "Selecione uma bota" if not x or x.get("name") == "" else x.get("name"),
            key="botas"
        )
    
    col3, col4 = st.columns(2)
    with col3:
        capas = get_equipamentos("capas")
        capa = st.selectbox(
            "Capa",
            options=[{"name": "", "id": ""}] + capas,
            format_func=lambda x: "Selecione uma capa" if x["name"] == "" else x["name"],
            key="capa"
        )
        pocoes = get_equipamentos("pocoes")
        potion = st.selectbox(
            "Poção",
            options=[{"name": "", "id": ""}] + pocoes,
            format_func=lambda x: "Selecione uma poção" if x["name"] == "" else x["name"],
            key="potion"
        )
    with col4:
        comidas = get_equipamentos("comidas")
        food = st.selectbox(
            "Comida",
            options=[{"name": "", "id": ""}] + comidas,
            format_func=lambda x: "Selecione uma comida" if x["name"] == "" else x["name"],
            key="food"
        )
    
    notas = st.text_area("Notas/Observações")
    
    if st.button("Salvar Build"):
        if nome and arma["name"]:  # Validação básica
            if salvar_build(
                nome, 
                tipo, 
                arma["name"], 
                cabeca["name"], 
                peito["name"], 
                botas["name"], 
                capa["name"], 
                potion["name"], 
                food["name"], 
                notas, 
                personagem, 
                secundaria["name"]
            ):
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

# Mover a função para antes da seção de edição
def encontrar_indice_item(items, nome_item):
    if not nome_item:
        return 0
    for i, item in enumerate(items):
        if item.get('name') == nome_item:
            return i + 1  # +1 porque temos um item vazio no início
    return 0

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
        armas = get_equipamentos("armas")
        arma = st.selectbox("Arma Principal", 
            options=[{"name": "", "id": ""}] + armas,
            index=encontrar_indice_item(armas, build['arma']),
            format_func=lambda x: x.get("name"),
            key="edit_arma")
        secundarias = get_equipamentos("secundaria")
        secundaria = st.selectbox("Mão Secundária",
            options=[{"name": "", "id": ""}] + secundarias,
            index=encontrar_indice_item(secundarias, build['secundaria']),
            format_func=lambda x: x.get("name"),
            key="edit_secundaria")
        cabecas = get_equipamentos("cabecas")
        cabeca = st.selectbox("Cabeça",
            options=[{"name": "", "id": ""}] + cabecas,
            index=encontrar_indice_item(cabecas, build['cabeca']),
            format_func=lambda x: x.get("name"),
            key="edit_cabeca")
        armaduras = get_equipamentos("armaduras")
        peito = st.selectbox("Armadura",
            options=[{"name": "", "id": ""}] + armaduras,
            index=encontrar_indice_item(armaduras, build['peito']),
            format_func=lambda x: x.get("name"),
            key="edit_peito")
        botas_list = get_equipamentos("botas")
        botas = st.selectbox("Botas",
            options=[{"name": "", "id": ""}] + botas_list,
            index=encontrar_indice_item(botas_list, build['botas']),
            format_func=lambda x: x.get("name"),
            key="edit_botas")
    
    col3, col4 = st.columns(2)
    with col3:
        capas = get_equipamentos("capas")
        capa = st.selectbox("Capa",
            options=[{"name": "", "id": ""}] + capas,
            index=encontrar_indice_item(capas, build['capa']),
            format_func=lambda x: x.get("name"),
            key="edit_capa")
        pocoes = get_equipamentos("pocoes")
        potion = st.selectbox("Poção",
            options=[{"name": "", "id": ""}] + pocoes,
            index=encontrar_indice_item(pocoes, build['potion']),
            format_func=lambda x: x.get("name"),
            key="edit_potion")
    with col4:
        comidas = get_equipamentos("comidas")
        food = st.selectbox("Comida",
            options=[{"name": "", "id": ""}] + comidas,
            index=encontrar_indice_item(comidas, build['food']),
            format_func=lambda x: x.get("name"),
            key="edit_food")
    
    notas = st.text_area("Notas/Observações", value=build['notas'], key="edit_notas")
    
    col5, col6 = st.columns(2)
    with col5:
        if st.button("Salvar Alterações"):
            if nome and arma.get("name"):
                if atualizar_build(
                    build['id'], 
                    nome, 
                    tipo, 
                    arma.get("name", ""),
                    cabeca.get("name", ""),
                    peito.get("name", ""),
                    botas.get("name", ""),
                    capa.get("name", ""),
                    potion.get("name", ""),
                    food.get("name", ""),
                    notas,
                    personagem,
                    secundaria.get("name", "")
                ):
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
        col1, col2, col3 = st.columns([0.6, 0.25, 0.15])
        
        with col1:
            st.markdown(f"""
            <div class="build-card">
                <div class="equipment-section">
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + 'T8_BAG@4' + '.png'}">
                        <div class="tooltip-trigger" title="Mochila"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['cabeca']) or '') + '.png'}" alt="{build['cabeca'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['cabeca'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['capa']) or '') + '.png'}" alt="{build['capa'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['capa'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['arma']) or '') + '.png'}" alt="{build['arma'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['arma'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['peito']) or '') + '.png'}" alt="{build['peito'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['peito'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['secundaria'] or build['arma']) or '') + '.png'}" alt="{build['secundaria'] or build['arma'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['secundaria'] or build['arma'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['potion']) or '') + '.png'}" alt="{build['potion'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['potion'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['botas']) or '') + '.png'}" alt="{build['botas'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['botas'] or 'Nenhuma'}"></div>
                    </div>
                    <div class="equipment-item">
                        <img class="equipment-img" src="{ALBION_RENDER_URL + (get_item_id(build['food']) or '') + '.png'}" alt="{build['food'] or 'Nenhuma'}">
                        <div class="tooltip-trigger" title="{build['food'] or 'Nenhuma'}"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if build['notas']:  # Só mostra o tooltip se houver notas
                st.markdown("ℹ️ Passe o mouse aqui para ver as notas" + " " * 100, help=build['notas'])
        
        with col2:
            # Lista de equipamentos
            st.markdown("**Equipamentos:**")
            if build['arma']: st.markdown(f"🗡️ {build['arma']}")
            if build['secundaria']: 
                st.markdown(f"🛡️ {build['secundaria']}")
            elif build['arma']:
                st.markdown(f"🛡️ {build['arma']} (Duas mãos)")
            if build['cabeca']: st.markdown(f"⛑️ {build['cabeca']}")
            if build['peito']: st.markdown(f"👕 {build['peito']}")
            if build['botas']: st.markdown(f"👢 {build['botas']}")
            if build['capa']: st.markdown(f"🧥 {build['capa']}")
            if build['potion']: st.markdown(f"🧪 {build['potion']}")
            if build['food']: st.markdown(f"🍖 {build['food']}")

        with col3:
            if st.button("✏️ Editar", key=f"edit_{build['id']}"):
                st.session_state.editing_build = build
                st.rerun()
            
            if st.button("🗑️ Deletar", key=f"delete_{build['id']}"):
                if deletar_build(build['id']):
                    st.success("Build deletada com sucesso!")
                    st.rerun() 