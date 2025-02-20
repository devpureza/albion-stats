import streamlit as st
import pandas as pd
from datetime import datetime
from database import get_db_connection, init_db
from config import get_personagens

st.set_page_config(page_title="Hunts em Grupo", page_icon="👥")

# Inicializar banco de dados
init_db()

# Função para carregar os dados do banco
def carregar_dados():
    try:
        with get_db_connection() as conn:
            query = "SELECT * FROM hunts_grupo ORDER BY data DESC"
            df = pd.read_sql_query(query, conn)
            # Converter a coluna de data para datetime e depois para o formato brasileiro
            df['data'] = pd.to_datetime(df['data']).dt.strftime('%d/%m/%Y')
            return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame(columns=['id', 'data', 'personagens', 'valor_total', 'observacoes'])

# Função para salvar hunt no banco
def salvar_hunt(data, personagens, valor_total, observacoes):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            personagens_str = ", ".join(personagens)
            cursor.execute("""
                INSERT INTO hunts_grupo (data, personagens, valor_total, observacoes)
                VALUES (?, ?, ?, ?)
            """, (data.strftime('%Y-%m-%d'), personagens_str, valor_total, observacoes))
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
            cursor.execute("DELETE FROM hunts_grupo WHERE id = ?", (id,))
            conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar registro: {str(e)}")
        return False

# Sidebar
with st.sidebar:
    st.title("Filtros")
    tamanho_grupo = st.slider("Tamanho do Grupo", 2, 20, (2, 20))
    data_inicio, data_fim = st.date_input(
        "Intervalo de Data",
        value=(datetime.now().date() - pd.Timedelta(days=30), datetime.now().date()),
        key="date_range"
    )

st.title("Hunts em Grupo 👥")

# Área para adicionar nova hunt
with st.expander("Adicionar Nova Hunt em Grupo", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data da Hunt")
        # Seleção múltipla de personagens
        personagens = st.multiselect(
            "Selecione os Personagens",
            options=get_personagens(),
            default=[get_personagens()[0]]  # Seleciona o primeiro personagem por padrão
        )
    with col2:
        valor_total = st.number_input("Valor Total da Hunt", min_value=0, step=1000)
    
    observacoes = st.text_area("Observações")
    
    if st.button("Salvar Hunt"):
        if len(personagens) > 0:  # Verificar se pelo menos um personagem foi selecionado
            if salvar_hunt(data, personagens, valor_total, observacoes):
                st.success("Hunt em grupo registrada com sucesso!")
                st.balloons()
        else:
            st.error("Selecione pelo menos um personagem!")

# Exibir dados
st.subheader("Histórico de Hunts em Grupo")
dados = carregar_dados()

# Aplicar filtros
# Filtro por número de participantes
dados['num_participantes'] = dados['personagens'].str.count(',') + 1
dados = dados[
    (dados['num_participantes'] >= tamanho_grupo[0]) & 
    (dados['num_participantes'] <= tamanho_grupo[1])
]

# Aplicar filtro de data
dados['data'] = pd.to_datetime(dados['data'], format='%d/%m/%Y')
dados = dados[(dados['data'].dt.date >= data_inicio) & (dados['data'].dt.date <= data_fim)]
dados['data'] = dados['data'].dt.strftime('%d/%m/%Y')

# Calcular valor por pessoa
dados['valor_por_pessoa'] = dados['valor_total'] / dados['num_participantes']

# Adicionar coluna com botão de deletar
for idx, row in dados.iterrows():
    if st.button("🗑️ Deletar", key=f"del_{row['id']}"):
        if deletar_hunt(row['id']):
            st.success("Registro deletado com sucesso!")
            st.rerun()

# Exibir dataframe
st.dataframe(
    dados.drop(['id', 'num_participantes'], axis=1),  # Remove colunas técnicas
    use_container_width=True,
    hide_index=True,
    column_config={
        "data": "Data",
        "personagens": "Personagens",
        "valor_total": st.column_config.NumberColumn(
            "Valor Total",
            format="R$ %.2f",
            help="Valor total da hunt em Reais"
        ),
        "valor_por_pessoa": st.column_config.NumberColumn(
            "Valor por Pessoa",
            format="R$ %.2f",
            help="Valor por pessoa em Reais"
        ),
        "observacoes": "Observações"
    }
)

# Análises
st.subheader("Análise de Hunts em Grupo")

# Métricas totais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Média de Participantes", f"{dados['num_participantes'].mean():.1f}")
with col2:
    st.metric("Valor Total Acumulado", f"R$ {dados['valor_total'].sum():,.2f}")
with col3:
    st.metric("Média por Pessoa", f"R$ {dados['valor_por_pessoa'].mean():,.2f}")
