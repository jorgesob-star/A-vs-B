import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Gestor de Valores")

# Inicializar session_state com valores padrão
default_values = {
    "kraken": 678,
    "gate": 1956,
    "coinbase": 2463,
    "n26": 195,
    "revolut": 2180,
    "caixa": 927
}

for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Inputs vinculados ao session_state
st.number_input("Kraken", value=st.session_state["kraken"], key="kraken")
st.number_input("Gate", value=st.session_state["gate"], key="gate")
st.number_input("Coinbase", value=st.session_state["coinbase"], key="coinbase")
st.number_input("N26", value=st.session_state["n26"], key="n26")
st.number_input("Revolut", value=st.session_state["revolut"], key="revolut")
st.number_input("Caixa", value=st.session_state["caixa"], key="caixa")

# Criar DataFrame atualizado
df = pd.DataFrame({
    "Plataforma": ["Kraken", "Gate", "Coinbase", "N26", "Revolut", "Caixa"],
    "Valor": [
        st.session_state["kraken"],
        st.session_state["gate"],
        st.session_state["coinbase"],
        st.session_state["n26"],
        st.session_state["revolut"],
        st.session_state["caixa"]
    ]
})

# Mostrar soma total
st.success(f"💰 Total = {df['Valor'].sum()}")

# Gerar CSV como string UTF-8
csv = df.to_csv(index=False, encoding="utf-8")

# Gerar nome do arquivo com data e hora
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"valores_{timestamp}.csv"

# Botão para salvar CSV
st.download_button(
    label="💾 Salvar Valores",
    data=csv,
    file_name=file_name,
    mime="text/csv"
)
