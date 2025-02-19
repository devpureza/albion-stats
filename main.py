import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Alô Gordão!",
    page_icon="🍔",
    layout="wide"
)

# Título e introdução
st.title("Alô Gordão! 🍔")

st.write("Bem-vindo à nossa página!")

# Conteúdo principal
st.markdown("""
       Uma página simples com uma mensagem calorosa para nosso gordão!
    
    #### O que oferecemos:
    * Doação de sets 💝
    * Mortes em avalon 🤗
    * Rhandim pistola💪
""")

# Adiciona um separador
st.divider()

# Adiciona um botão interativo
if st.button("Clique aqui para uma surpresa! 🎉"):
    st.balloons()
    st.success("Rhandim bilauzudo!")
