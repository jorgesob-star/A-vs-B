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

# Inputs vinculados ao session_state (SEM passar value)
for key in default_values.keys():
    st.number_input(key, key=key)

# Criar DataFrame a partir dos valores atuais do session_state
df = pd.DataFrame({
    "Plataforma": list(default_values.keys()),
    "Valor": [st.session_state[k] for k in default_values.keys()]
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
