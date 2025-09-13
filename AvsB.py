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
if "initialized" not in st.session_state:
    for key, val in default_values.items():
        st.session_state[key] = val
    st.session_state["initialized"] = True

# Inputs vinculados ao session_state
for key in default_values.keys():
    st.session_state[key] = st.number_input(label=key, value=st.session_state[key], key=key+"_input")

# Criar DataFrame atualizado
df = pd.DataFrame({
    "Plataforma": list(default_values.keys()),
    "Valor": [st.session_state[key] for key in default_values.keys()]
})

# Mostrar soma total
st.success(f"💰 Total = {df['Valor'].sum()}")

# Gerar CSV
csv = df.to_csv(index=False, encoding="utf-8")

# Nome do arquivo com timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"valores_{timestamp}.csv"

# Botão de download
st.download_button(
    label="💾 Salvar Valores",
    data=csv,
    file_name=file_name,
    mime="text/csv"
)
