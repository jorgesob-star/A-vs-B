import streamlit as st
import pandas as pd

st.title("Gestor de Valores")

# Inicializar session_state apenas uma vez
for key, default in {
    "kraken": 678,
    "gate": 1956,
    "coinbase": 2463,
    "n26": 195,
    "revolut": 2180,
    "caixa": 927
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# Entradas de valores vinculadas ao session_state
kraken = st.number_input("Kraken", value=st.session_state["kraken"], key="kraken")
gate = st.number_input("Gate", value=st.session_state["gate"], key="gate")
coinbase = st.number_input("Coinbase", value=st.session_state["coinbase"], key="coinbase")
n26 = st.number_input("N26", value=st.session_state["n26"], key="n26")
revolut = st.number_input("Revolut", value=st.session_state["revolut"], key="revolut")
caixa = st.number_input("Caixa", value=st.session_state["caixa"], key="caixa")

# Criar DataFrame atualizado
valores = {
    "Plataforma": ["Kraken", "Gate", "Coinbase", "N26", "Revolut", "Caixa"],
    "Valor": [kraken, gate, coinbase, n26, revolut, caixa],
}
df = pd.DataFrame(valores)

# Mostrar soma total
total = df["Valor"].sum()
st.success(f"💰 Total = {total}")

# Gerar CSV pronto para download
csv = df.to_csv(index=False, encoding="utf-8")

# Botão de download manual
st.download_button(
    label="💾 Salvar Valores",
    data=csv,
    file_name="valores.csv",
    mime="text/csv",
)
