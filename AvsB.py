import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="Comparador de Ganhos TVDE",
    page_icon="🚗",
    layout="wide"
)

# Estilo simples
st.markdown("""
<style>
.stButton>button {background-color: #4CAF50; color: white; border-radius: 8px;}
.stButton>button:hover {background-color: #45a049;}
.stNumberInput input {border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("Compare os lucros entre carro alugado e próprio para motoristas TVDE.")

# Parâmetros padrão
params = {
    "rental_cost": 280.0,
    "rental_commission": 7.0,
    "own_insurance": 45.0,
    "own_maintenance": 50.0,
    "own_commission": 12.0,
    "other_costs": 0.0
}

# --- Dados de Entrada ---
st.header("📊 Dados de Entrada")
weekly_earnings = st.number_input("Ganhos Semanais (€):", min_value=0.0, value=800.0, step=50.0)
fuel_cost = st.number_input("Custo Semanal com Combustível (€):", min_value=0.0, value=200.0, step=10.0)
other_costs = st.number_input("Outros Custos Semanais (€):", min_value=0.0, value=params["other_costs"], step=5.0)

# --- Parâmetros Avançados ---
with st.expander("⚙️ Parâmetros Avançados"):
    col1, col2 = st.columns(2)
    with col1:
        rental_cost = st.number_input("Custo do Aluguel (€/semana):", value=params["rental_cost"])
        rental_commission = st.number_input("Comissão Carro Alugado (%):", value=params["rental_commission"])
    with col2:
        own_insurance = st.number_input("Seguro Carro Próprio (€):", value=params["own_insurance"])
        own_maintenance = st.number_input("Manutenção Carro Próprio (€):", value=params["own_maintenance"])
        own_commission = st.number_input("Comissão Carro Próprio (%):", value=params["own_commission"])

# --- Função de cálculo ---
def calcular_ganhos(weekly_earnings, fuel_cost, other_costs, rental_cost, rental_comm, own_ins, own_maint, own_comm):
    rental_comm_value = weekly_earnings * (rental_comm / 100)
    rental_net = weekly_earnings - rental_comm_value - rental_cost - fuel_cost - other_costs
    
    own_comm_value = weekly_earnings * (own_comm / 100)
    own_net = weekly_earnings - own_comm_value - own_ins - own_maint - fuel_cost - other_costs
    
    return rental_net, own_net, rental_net - own_net, rental_comm_value, own_comm_value

# --- Botão de cálculo ---
if st.button("Calcular"):
    if weekly_earnings < 0 or fuel_cost < 0 or other_costs < 0:
        st.error("🚫 Valores não podem ser negativos.")
        st.stop()
    
    rental_net, own_net, diff, rental_comm_val, own_comm_val = calcular_ganhos(
        weekly_earnings, fuel_cost, other_costs, rental_cost, rental_commission, own_insurance, own_maintenance, own_commission
    )
    
    # --- Resultados ---
    st.header("📈 Resultados")
    col1, col2, col3 = st.columns(3)
    col1.metric("Carro Alugado (€)", f"{rental_net:.2f}", delta=f"{rental_net-own_net:.2f} vs Próprio")
    col2.metric("Carro Próprio (€)", f"{own_net:.2f}", delta=f"{own_net-rental_net:.2f} vs Alugado")
    col3.metric("Diferença Anual (€)", f"{diff*52:.2f}")
    
    # Tabela detalhada
    df = pd.DataFrame({
        "Descrição": ["Ganhos Semanais","Comissão","Custo Aluguel","Seguro","Manutenção","Combustível","Outros Custos","Líquido"],
        "Carro Alugado (€)": [f"{weekly_earnings:.2f}", f"-{rental_comm_val:.2f} ({rental_commission}%)", f"-{rental_cost:.2f}", "0.00","0.00", f"-{fuel_cost:.2f}", f"-{other_costs:.2f}", f"{rental_net:.2f}"],
        "Carro Próprio (€)": [f"{weekly_earnings:.2f}", f"-{own_comm_val:.2f} ({own_commission}%)", "0.00", f"-{own_insurance:.2f}", f"-{own_maintenance:.2f}", f"-{fuel_cost:.2f}", f"-{other_costs:.2f}", f"{own_net:.2f}"]
    })
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Download CSV
    st.download_button("📥 Baixar CSV", df.to_csv(index=False), file_name="resultados_tvde.csv", mime="text/csv")
    
    # Recomendação
    st.subheader("Recomendação")
    if diff > 0.01:
        st.success(f"✅ Carro alugado mais vantajoso: € {diff:.2f}/semana")
    elif diff < -0.01:
        st.success(f"✅ Carro próprio mais vantajoso: € {abs(diff):.2f}/semana")
    else:
        st.info("ℹ️ Resultado financeiro similar para ambas opções.")
    
    # Gráfico simples
    chart_data = pd.DataFrame({"Lucro Líquido (€)":[rental_net, own_net]}, index=["Alugado","Próprio"])
    st.bar_chart(chart_data)

# Dicas
with st.expander("💡 Dicas e Informações"):
    st.markdown("""
    - Ganhos Semanais: total recebido.
    - Combustível: gasto semanal.
    - Outros Custos: lavagem, estacionamento, portagens.
    - Comissão: percentual da plataforma.
    - Seguro e Manutenção: custo do carro próprio.
    ⚠️ Outros fatores não incluídos: desvalorização, impostos, custos imprevistos.
    """)

st.markdown("---")
st.caption("Desenvolvido para ajudar motoristas TVDE a tomar decisões financeiras informadas. 🚗")
