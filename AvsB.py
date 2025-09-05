import streamlit as st

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# Entradas ajustáveis
apuro = st.number_input("💰 Apuro (€)", min_value=0.0, value=800.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto Combustível (€)", min_value=0.0, value=200.0, step=1.0)

st.markdown("---")
st.subheader("Opções da Empresa")

# Opção 1
aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=280.0, step=1.0)
perc_aluguer = st.number_input("👔 Empresa sobre Apuro (%)", min_value=0.0, value=7.0, step=0.5)

# Opção 2
seguro = st.number_input("🛡️ Seguro (€)", min_value=0.0, value=45.0, step=1.0)
perc_seguro = st.number_input("👔 Empresa sobre Apuro (%)", min_value=0.0, value=12.0, step=0.5)

st.markdown("---")

if st.button("Calcular 🔹"):
    st.subheader("📊 Resultados:")

    # Subtrair combustível do apuro
    apuro_liquido = apuro - desc_combustivel

    # Cálculo do que sobra em cada opção
    sobra_opcao1 = apuro_liquido - (apuro * perc_aluguer / 100) - aluguer
    sobra_opcao2 = apuro_liquido - (apuro * perc_seguro / 100) - seguro

    # Mostrar resultados
    st.markdown(f"💰 **Opção 1:** {perc_aluguer}% do apuro + {aluguer} € aluguer → **Sobra: {sobra_opcao1:.2f} €**")
    st.markdown(f"💰 **Opçãoimport streamlit as st

# Configuração da página
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# Entradas ajustáveis
apuro = st.number_input("💰 Apuro (€)", min_value=0.0, value=800.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto Combustível (€)", min_value=0.0, value=200.0, step=1.0)

st.markdown("---")
st.subheader("Opções da Empresa")

# Opção 1
aluguer = st.number_input("🏠 Aluguer (€)", min_value=0.0, value=280.0, step=1.0)
perc_aluguer = st.number_input("👔 Empresa sobre Aluguer (%)", min_value=0.0, value=7.0, step=0.5)

# Opção 2
seguro = st.number_input("🛡️ Seguro (€)", min_value=0.0, value=45.0, step=1.0)
perc_seguro = st.number_input("👔 Empresa sobre Seguro (%)", min_value=0.0, value=12.0, step=0.5)

st.markdown("---")

if st.button("Calcular 🔹"):
    st.subheader("📊 Resultados:")

    # Cálculo do custo total de cada opção
    total_opcao1 = aluguer + (aluguer * perc_aluguer / 100) + desc_combustivel
    total_opcao2 = seguro + (seguro * perc_seguro / 100) + desc_combustivel

    # Quanto sobra do apuro
    sobra_opcao1 = apuro - total_opcao1
    sobra_opcao2 = apuro - total_opcao2

    # Mostrar resultados
    st.markdown(f"💰 **Opção 1:** {aluguer} € + {perc_aluguer}% + {desc_combustivel} € combustível → **Sobra: {sobra_opcao1:.2f} €**")
    st.markdown(f"💰 **Opção 2:** {seguro} € + {perc_seguro}% + {desc_combustivel} € combustível → **Sobra: {sobra_opcao2:.2f} €**")

    # Indicar qual compensa mais
    if sobra_opcao1 > sobra_opcao2:
        st.success("✅ Opção 1 é mais vantajosa!")
    elif sobra_opcao2 > sobra_opcao1:
        st.success("✅ Opção 2 é mais vantajosa!")
    else:
        st.info("⚖️ Ambas as opções resultam no mesmo valor restante.")
