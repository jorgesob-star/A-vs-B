import streamlit as st
import pandas as pd

st.title("Gestor de Valores")

# Entradas de valores
kraken = st.number_input("Kraken", value=678)
gate = st.number_input("Gate", value=1956)
coinbase = st.number_input("Coinbase", value=2463)
n26 = st.number_input("N26", value=195)
revolut = st.number_input("Revolut", value=2180)
caixa = st.number_input("Caixa", value=927)

# Criar DataFrame atualizado
valores = {
    "Plataforma": ["Kraken", "Gate", "Coinbase", "N26", "Revolut", "Caixa"],
    "Valor": [kraken, gate, coinbase, n26, revolut, caixa],
}
df = pd.DataFrame(valores)

# Mostrar soma total
total = df["Valor"].sum()
st.success(f"💰 Total = {total}")

# Botão para salvar CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "💾 Salvar Valores",
    data=csv,
    file_name="valores.csv",
    mime="text/csv",
)
