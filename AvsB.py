import streamlit as st
import matplotlib.pyplot as plt

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Descontos", layout="centered")
st.title("💸 Comparador de Descontos")

# --- Valores padrão ---
DEFAULTS = {
    'aluguer': 280.0,
    'perc_aluguer': 7.0,
    'seguro': 45.0,
    'perc_seguro': 12.0,
    'manutencao': 20.0
}

# Inicializa valores no estado da sessão
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Entradas do usuário ---
st.header("Entradas do Usuário")
apuro = st.number_input("💰 Apuro total (€)", min_value=0.0, value=800.0, step=10.0)
desc_combustivel = st.number_input("⛽ Desconto de Combustível (€)", min_value=0.0, value=200.0, step=1.0)

apuro_liquido = apuro - desc_combustivel

st.markdown("---")

# --- Opções da empresa com expander ---
st.header("Opções da Empresa")
with st.expander("Modificar Opções Padrão"):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Opção 1")
        st.number_input("🏠 Aluguer (€)", min_value=0.0, value=st.session_state.aluguer, step=1.0, key='aluguer')
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_aluguer, step=0.5, key='perc_aluguer')
    with col2:
        st.subheader("Opção 2")
        st.number_input("🛡️ Seguro (€)", min_value=0.0, value=st.session_state.seguro, step=1.0, key='seguro')
        st.number_input("👔 Percentual (%)", min_value=0.0, value=st.session_state.perc_seguro, step=0.5, key='perc_seguro')
        st.number_input("🛠️ Manutenção (€)", min_value=0.0, value=st.session_state.manutencao, step=1.0, key='manutencao')

st.markdown("---")

# --- Função de cálculo ---
def calcular_sobra(apuro_liquido, percentual, fixo, manutencao=0):
    return apuro_liquido - (apuro * percentual / 100) - fixo - manutencao

# --- Botão de cálculo ---
if st.button("Calcular 🔹"):
    sobra_opcao1 = calcular_sobra(apuro_liquido, st.session_state.perc_aluguer, st.session_state.aluguer)
    sobra_opcao2 = calcular_sobra(apuro_liquido, st.session_state.perc_seguro, st.session_state.seguro, st.session_state.manutencao)

    # --- Resultados ---
    st.subheader("📊 Resultados")
    col3, col4 = st.columns(2)
    col3.metric("Sobra na Opção 1", f"{sobra_opcao1:,.2f} €")
    col4.metric("Sobra na Opção 2", f"{sobra_opcao2:,.2f} €")
    
    if sobra_opcao1 > sobra_opcao2:
        st.success(f"🎉 A **Opção 1** é a melhor escolha, com diferença de {(sobra_opcao1 - sobra_opcao2):,.2f} €.")
    elif sobra_opcao2 > sobra_opcao1:
        st.success(f"🎉 A **Opção 2** é a melhor escolha, com diferença de {(sobra_opcao2 - sobra_opcao1):,.2f} €.")
    else:
        st.info("As duas opções resultam no mesmo valor.")
    
    st.markdown("---")
    
    # --- Detalhes dos cálculos ---
    st.markdown("### Detalhes dos Cálculos")
    
    st.markdown(f"""
**Opção 1:**  
Apuro Líquido: {apuro_liquido:,.2f} €  
Dedução Percentual ({st.session_state.perc_aluguer}%): {(apuro * st.session_state.perc_aluguer / 100):,.2f} €  
Dedução Aluguer: {st.session_state.aluguer:,.2f} €  
**Valor Final:** {sobra_opcao1:,.2f} €
""")
    
    st.markdown(f"""
**Opção 2:**  
Apuro Líquido: {apuro_liquido:,.2f} €  
Dedução Percentual ({st.session_state.perc_seguro}%): {(apuro * st.session_state.perc_seguro / 100):,.2f} €  
Dedução Seguro: {st.session_state.seguro:,.2f} €  
Dedução Manutenção: {st.session_state.manutencao:,.2f} €  
**Valor Final:** {sobra_opcao2:,.2f} €
""")

    # --- Gráfico comparativo ---
    st.markdown("### 📊 Comparação Visual")
    fig, ax = plt.subplots(figsize=(6, 4))
    opcoes = ['Opção 1', 'Opção 2']
    valores = [sobra_opcao1, sobra_opcao2]
    cores = ['#4CAF50', '#2196F3']
    ax.bar(opcoes, valores, color=cores)
    ax.set_ylabel('€ Restantes')
    ax.set_title('Comparação entre Opções')
    for i, v in enumerate(valores):
        ax.text(i, v + 5, f"{v:,.2f} €", ha='center', fontweight='bold')
    st.pyplot(fig)
