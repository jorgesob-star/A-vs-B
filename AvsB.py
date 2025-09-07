import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Comparador de Ganhos TVDE",
    page_icon="🚗",
    layout="wide"
)

# Título da aplicação
st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("Compare os lucros entre usar carro alugado e carro próprio para trabalhar como motorista TVDE.")

# ---
# Lógica de Inicialização dos Parâmetros
# ---

# Inicializa todos os parâmetros no session_state com valores padrão
if 'show_params' not in st.session_state:
    st.session_state.show_params = False
if 'rental_cost' not in st.session_state:
    st.session_state.rental_cost = 280.0
if 'rental_commission' not in st.session_state:
    st.session_state.rental_commission = 7
if 'own_insurance' not in st.session_state:
    st.session_state.own_insurance = 45.0
if 'own_maintenance' not in st.session_state:
    st.session_state.own_maintenance = 50.0
if 'own_commission' not in st.session_state:
    st.session_state.own_commission = 12
if 'weeks_comparison' not in st.session_state:
    st.session_state.weeks_comparison = 4

# ---
# Seção de Entrada de Dados e Parâmetros
# ---

col1, col2 = st.columns(2)

with col1:
    st.header("📊 Dados de Entrada")
    
    weekly_earnings = st.number_input(
        "Ganhos Semanais (€):", 
        min_value=0.0, 
        value=800.0, 
        step=50.0,
        help="Valor total ganho por semana antes de despesas"
    )
    
    fuel_cost = st.number_input(
        "Custo Semanal com Combustível (€):", 
        min_value=0.0, 
        value=200.0, 
        step=10.0,
        help="Custo semanal estimado com combustível"
    )
    
    # Adicionado: Período de comparação
    st.session_state.weeks_comparison = st.slider(
        "Período de Comparação (semanas):",
        min_value=1,
        max_value=52,
        value=st.session_state.weeks_comparison,
        help="Selecione o número de semanas para comparar"
    )

# Botão para mostrar/ocultar parâmetros
if st.button("⚙️ Mostrar/Ocultar Parâmetros Avançados"):
    st.session_state.show_params = not st.session_state.show_params

# Mostrar parâmetros apenas se show_params for True
if st.session_state.show_params:
    with col2:
        st.header("⚙️ Parâmetros Avançados")
        
        # Parâmetros para carro alugado
        st.subheader("Carro Alugado")
        st.session_state.rental_cost = st.number_input(
            "Custo do Aluguel (€/semana):", 
            min_value=0.0, 
            value=st.session_state.rental_cost, 
            step=10.0
        )
        
        st.session_state.rental_commission = st.slider(
            "Comissão com Carro Alugado (%):", 
            min_value=0, 
            max_value=30, 
            value=st.session_state.rental_commission, 
            step=1
        )
        
        # Parâmetros para carro próprio
        st.subheader("Carro Próprio")
        st.session_state.own_insurance = st.number_input(
            "Seguro (€/semana):", 
            min_value=0.0, 
            value=st.session_state.
