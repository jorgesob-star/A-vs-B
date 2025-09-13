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
def gerar_dataframe():
    return pd.DataFrame({
        "Plataforma": ["Kraken", "Gate", "Coinbase", "N26", "Revolut", "Caixa"],
        "Valor": [kraken, gate, coinbase, n26, revolut, caixa],
    })

# Mostrar soma total
df = gerar_dataframe()
total = df["Valor"].sum()
st.success(f"💰 Total = {total}")

# Botão para salvar CSV sempre com valores atuais
st.download_button(
    label="💾 Salvar Valores",
    data=lambda: gerar_dataframe().to_csv(index=False, encoding="utf-8"),
    file_name="valores.csv",
    mime="text/csv",
)
