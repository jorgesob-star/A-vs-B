import streamlit as st

st.title("Soma de Valores por Plataforma")

st.subheader("Insira os valores:")

kraken = st.number_input("Kraken", value=678)
gate = st.number_input("Gate", value=1956)
coinbase = st.number_input("Coinbase", value=2463)
n26 = st.number_input("N26", value=195)
revolut = st.number_input("Revolut", value=2180)
caixa = st.number_input("Caixa", value=927)

# Dicionário atualizado
valores = {
    "Kraken": kraken,
    "Gate": gate,
    "Coinbase": coinbase,
    "N26": n26,
    "Revolut": revolut,
    "Caixa": caixa,
}

st.subheader("Valores Digitados")
st.write(valores)

# Soma total
total = sum(valores.values())
st.subheader("Soma Total")
st.success(f"💰 Total = {total}")
