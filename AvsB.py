import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Gestor de Valores")

# Valores padrão
default_values = {
    "Kraken": 678,
    "Gate": 1956,
    "Coinbase": 2463,
    "N26": 195,
    "Revolut": 2180,
    "Caixa": 927
}

# Inicializar session_state apenas uma vez
for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Inputs vinculados ao session_state (SEM value após a inicialização)
kraken = st.number_input("Kraken", key="Kraken")
gate = st.number_input("Gate", key="Gate")
coinbase = st.number_input("Coinbase", key="Coinbase")
n26 = st.number_input("N26", key="N26")
revolut = st.number_input("Revolut", key="Revolut")
caixa = st.number_input("Caixa", key="Caixa")

# Criar DataFrame atualizado
df = pd.DataFrame({
    "Plataforma": list(default_values.keys()),
    "Valor": [
        st.session_state["Kraken"],
        st.session_state["Gate"],
        st.session_state["Coinbase"],
        st.session_state["N26"],
        st.session_state["Revolut"],
        st.session_state["Caixa"]
    ]
})

# Mostrar soma total
st.success(f"💰 Total = {df['Valor'].sum()}")

# Gerar CSV UTF-8
csv = df.to_csv(index=False, encoding="utf-8")

# Nome do arquivo com timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"valores_{timestamp}.csv"

# Botão para salvar CSV
st.download_button(
    label="💾 Salvar Valores",
    data=csv,
    file_name=file_name,
    mime="text/csv"
)
