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
if "values" not in st.session_state:
    st.session_state["values"] = default_values.copy()

# Criar inputs diretamente vinculados ao session_state["values"]
for key in default_values.keys():
    # Valor inicial vem do session_state["values"]
    st.session_state["values"][key] = st.number_input(
        label=key,
        value=st.session_state["values"][key],
        key=key
    )

# Criar DataFrame atualizado
df = pd.DataFrame({
    "Plataforma": list(default_values.keys()),
    "Valor": [st.session_state["values"][key] for key in default_values.keys()]
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
