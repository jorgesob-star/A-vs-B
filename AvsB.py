import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Comparador de Ganhos TVDE", page_icon="🚗", layout="wide")

st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("Compare os lucros entre usar carro alugado e carro próprio para trabalhar como motorista TVDE.")

# --- Inicialização ---
params = ['show_params', 'rental_cost', 'rental_commission', 'own_insurance', 'own_maintenance', 'own_commission',
          'extra_expenses', 'include_extra_expenses', 'calculation_type']
defaults = [False, 270.0, 6.0, 45.0, 50.0, 12.0, 0.0, False, None]
for p, d in zip(params, defaults):
    if p not in st.session_state:
        st.session_state[p] = d

# --- Entradas ---
col1, col2 = st.columns(2)
with col1:
    st.header("📊 Dados de Entrada")
    weekly_earnings = st.number_input("Ganhos Semanais (€):", min_value=0.0, value=999.0, step=50.0)
    weekly_hours = st.number_input("Horas Trabalhadas por Semana:", min_value=0.0, value=56.0, step=1.0)
    fuel_cost = st.number_input("Custo Semanal com Combustível (€):", min_value=0.0, value=170.0, step=10.0)
with col2:
    st.header("📏 Quilometragem")
    weekly_km = st.number_input("Quilómetros percorridos por semana:", min_value=0.0, value=1200.0, step=50.0)

st.header("💸 Despesas Extras")
extra_col1, extra_col2 = st.columns(2)
with extra_col1:
    st.session_state.include_extra_expenses = st.checkbox("Incluir despesas extras (informativo)", value=st.session_state.include_extra_expenses)
with extra_col2:
    if st.session_state.include_extra_expenses:
        st.session_state.extra_expenses = st.number_input("Despesas Extras Semanais (€):", min_value=0.0, value=st.session_state.extra_expenses, step=5.0)

# --- Parâmetros avançados ---
if st.button("⚙️ Parâmetros Avançados"):
    st.session_state.show_params = not st.session_state.show_params

if st.session_state.show_params:
    st.header("⚙️ Parâmetros Avançados")
    adv_col1, adv_col2 = st.columns(2)
    with adv_col1:
        st.subheader("Carro Alugado")
        st.session_state.rental_cost = st.number_input("Custo do Aluguel (€/semana):", min_value=0.0, value=st.session_state.rental_cost, step=10.0)
        st.session_state.rental_commission = st.number_input("Comissão com Carro Alugado (%):", min_value=0.0, max_value=30.0, value=st.session_state.rental_commission, step=0.5)
    with adv_col2:
        st.subheader("Carro Próprio")
        st.session_state.own_insurance = st.number_input("Seguro (€/semana):", min_value=0.0, value=st.session_state.own_insurance, step=5.0)
        st.session_state.own_maintenance = st.number_input("Manutenção (€/semana):", min_value=0.0, value=st.session_state.own_maintenance, step=5.0)
        st.session_state.own_commission = st.number_input("Comissão com Carro Próprio (%):", min_value=0.0, max_value=30.0, value=st.session_state.own_commission, step=0.5)

# --- Botões ---
st.header("🧮 Calcular")
calc_col1, calc_col2, calc_col3 = st.columns(3)
with calc_col1:
    if st.button("Calcular Carro Alugado"):
        st.session_state.calculation_type = "alugado"
with calc_col2:
    if st.button("Calcular Carro Próprio"):
        st.session_state.calculation_type = "proprio"
with calc_col3:
    if st.button("Comparar Ambos"):
        st.session_state.calculation_type = "comparar"

# --- Função de cálculo ---
def calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km):
    alugado_comm = weekly_earnings * (st.session_state.rental_commission / 100)
    alugado_net = weekly_earnings - alugado_comm - st.session_state.rental_cost - fuel_cost
    proprio_comm = weekly_earnings * (st.session_state.own_commission / 100)
    proprio_net = weekly_earnings - proprio_comm - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost

    resultados = {
        "alugado": {
            "líquido": alugado_net,
            "hora": alugado_net / weekly_hours if weekly_hours else 0,
            "profit_km": alugado_net / weekly_km if weekly_km else 0,
            "fuel_km": fuel_cost / weekly_km if weekly_km else 0,
            "total_km": (st.session_state.rental_cost + fuel_cost) / weekly_km if weekly_km else 0
        },
        "proprio": {
            "líquido": proprio_net,
            "hora": proprio_net / weekly_hours if weekly_hours else 0,
            "profit_km": proprio_net / weekly_km if weekly_km else 0,
            "fuel_km": fuel_cost / weekly_km if weekly_km else 0,
            "total_km": (st.session_state.own_insurance + st.session_state.own_maintenance + fuel_cost) / weekly_km if weekly_km else 0
        }
    }
    resultados["diferença"] = resultados["alugado"]["líquido"] - resultados["proprio"]["líquido"]
    resultados["diferença_hora"] = resultados["alugado"]["hora"] - resultados["proprio"]["hora"]
    resultados["diferença_km"] = resultados["alugado"]["profit_km"] - resultados["proprio"]["profit_km"]
    return resultados

# --- Executar cálculo ---
if st.session_state.calculation_type:
    resultados = calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km)
    alugado = resultados["alugado"]
    proprio = resultados["proprio"]

    st.header("📈 Resultados")
    st.subheader("Métricas Semanais")
    col1, col2, col3 = st.columns(3)
    col1.metric("Carro Alugado (€)", f"{alugado['líquido']:.2f}")
    col2.metric("Carro Próprio (€)", f"{proprio['líquido']:.2f}")
    col3.metric("Diferença (€)", f"{resultados['diferença']:.2f}")

    st.subheader("Média Horária (€)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Alugado", f"{alugado['hora']:.2f}")
    col2.metric("Próprio", f"{proprio['hora']:.2f}")
    col3.metric("Diferença", f"{resultados['diferença_hora']:.2f}")

    st.subheader("Lucro por Km (€)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Alugado", f"{alugado['profit_km']:.2f}")
    col2.metric("Próprio", f"{proprio['profit_km']:.2f}")
    col3.metric("Diferença", f"{resultados['diferença_km']:.2f}")

    st.subheader("Gráficos")
    tab1, tab2, tab3 = st.tabs(["Lucro Semanal", "Média Horária", "Lucro por Km"])
    with tab1:
        st.bar_chart(pd.DataFrame({"Opção": ["Alugado", "Próprio"], "Lucro (€)": [alugado['líquido'], proprio['líquido']]}), x="Opção", y="Lucro (€)")
    with tab2:
        st.bar_chart(pd.DataFrame({"Opção": ["Alugado", "Próprio"], "Média Horária (€)": [alugado['hora'], proprio['hora']]}), x="Opção", y="Média Horária (€)")
    with tab3:
        st.bar_chart(pd.DataFrame({"Opção": ["Alugado", "Próprio"], "Lucro por Km (€)": [alugado['profit_km'], proprio['profit_km']]}), x="Opção", y="Lucro por Km (€)")

    if st.session_state.include_extra_expenses:
        st.info(f"💡 Despesas extras informativas: € {st.session_state.extra_expenses:.2f} por semana (não afeta os cálculos).")
