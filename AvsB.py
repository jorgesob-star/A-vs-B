import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Gestor de Valores")

# Valores padrão
default_values = {
    "kraken": 678,
    "gate": 1956,
    "coinbase": 2463,
    "n26": 195,
    "revolut": 2180,
    "caixa": 927
}

# Inicializar session_state apenas uma vez
for key, val in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Inputs vinculados ao session_state (NUNCA passar value após a inicialização)
st.number_input("Kraken", key="kraken")
st.number_input("Gate", key="gate")
st.number_input("Coinbase", key="coinbase")
st.number_input("N26", key="n26")
st.number_input("Revolut", key="revolut")
st.number_input("Caixa", key="caixa")

# Criar DataFrame a partir do session_state
df = pd.DataFrame({
    "Plataforma": list(default_values.keys()),
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

# Gerar CSV a partir do session_state
csv = df.to_csv(index=False, encoding="utf-8")

# Nome do arquivo com data/hora
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"valores_{timestamp}.csv"

# Botão de download manual
st.download_button(
    label="💾 Salvar Valores",
    data=csv,
    file_name=file_name,
    mime="text/csv"
)
