import streamlit as st
import pandas as pd

# --- Configuração da página ---
st.set_page_config(page_title="Comparador de Ganhos TVDE", page_icon="🚗", layout="wide")
st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("Compare os ganhos e o custo por km entre usar carro alugado ou próprio como motorista TVDE.")

# --- Inicialização dos parâmetros ---
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
    weekly_km = st.number_input("Quilómetros percorridos por semana:", min_value=0.0, value=1500.0, step=50.0)

# --- Despesas extras ---
st.header("💸 Despesas Extras")
extra_col1, extra_col2 = st.columns(2)
with extra_col1:
    st.session_state.include_extra_expenses = st.checkbox(
        "Incluir despesas extras (informativo)", value=st.session_state.include_extra_expenses
    )
with extra_col2:
    if st.session_state.include_extra_expenses:
        st.session_state.extra_expenses = st.number_input(
            "Despesas Extras Semanais (€):", min_value=0.0, value=st.session_state.extra_expenses, step=5.0
        )

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

# --- Botões de cálculo ---
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
def calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km, calculation_type):
    resultados = {}

    if calculation_type == "alugado":
        rental_comm = weekly_earnings * (st.session_state.rental_commission / 100)
        rental_net = weekly_earnings - rental_comm - st.session_state.rental_cost - fuel_cost
        custo_km_alugado = (st.session_state.rental_cost + fuel_cost + rental_comm) / weekly_km if weekly_km else 0
        resultados["alugado"] = {
            "líquido": rental_net,
            "hora": rental_net / weekly_hours if weekly_hours else 0,
            "custo_km": custo_km_alugado
        }

    elif calculation_type == "proprio":
        own_comm = weekly_earnings * (st.session_state.own_commission / 100)
        own_net = weekly_earnings - own_comm - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost
        custo_km_proprio = (st.session_state.own_insurance + st.session_state.own_maintenance + fuel_cost + own_comm) / weekly_km if weekly_km else 0
        resultados["proprio"] = {
            "líquido": own_net,
            "hora": own_net / weekly_hours if weekly_hours else 0,
            "custo_km": custo_km_proprio
        }

    elif calculation_type == "comparar":
        rental_comm = weekly_earnings * (st.session_state.rental_commission / 100)
        own_comm = weekly_earnings * (st.session_state.own_commission / 100)
        rental_net = weekly_earnings - rental_comm - st.session_state.rental_cost - fuel_cost
        own_net = weekly_earnings - own_comm - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost
        resultados["alugado"] = {
            "líquido": rental_net,
            "hora": rental_net / weekly_hours if weekly_hours else 0,
            "custo_km": (st.session_state.rental_cost + fuel_cost + rental_comm) / weekly_km if weekly_km else 0
        }
        resultados["proprio"] = {
            "líquido": own_net,
            "hora": own_net / weekly_hours if weekly_hours else 0,
            "custo_km": (st.session_state.own_insurance + st.session_state.own_maintenance + fuel_cost + own_comm) / weekly_km if weekly_km else 0
        }
        resultados["diferença"] = resultados["alugado"]["líquido"] - resultados["proprio"]["líquido"]
        resultados["diferença_hora"] = resultados["alugado"]["hora"] - resultados["proprio"]["hora"]
        resultados["diferença_km"] = resultados["alugado"]["custo_km"] - resultados["proprio"]["custo_km"]

    return resultados

# --- Executar cálculo ---
if st.session_state.calculation_type:
    resultados = calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km, st.session_state.calculation_type)
    st.header("📈 Resultados")

    if st.session_state.calculation_type == "alugado":
        alugado = resultados["alugado"]
        st.metric("Carro Alugado - Líquido (€)", f"{alugado['líquido']:.2f}")
        st.metric("Média Horária (€)", f"{alugado['hora']:.2f}")
        st.metric("Custo Real por Km (€)", f"{alugado['custo_km']:.2f}")

    elif st.session_state.calculation_type == "proprio":
        proprio = resultados["proprio"]
        st.metric("Carro Próprio - Líquido (€)", f"{proprio['líquido']:.2f}")
        st.metric("Média Horária (€)", f"{proprio['hora']:.2f}")
        st.metric("Custo Real por Km (€)", f"{proprio['custo_km']:.2f}")

    elif st.session_state.calculation_type == "comparar":
        alugado = resultados["alugado"]
        proprio = resultados["proprio"]
        st.subheader("Comparação")
        col1, col2, col3 = st.columns(3)
        col1.metric("Alugado (€)", f"{alugado['líquido']:.2f}")
        col2.metric("Próprio (€)", f"{proprio['líquido']:.2f}")
        col3.metric("Diferença (€)", f"{resultados['diferença']:.2f}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Alugado €/h", f"{alugado['hora']:.2f}")
        col2.metric("Próprio €/h", f"{proprio['hora']:.2f}")
        col3.metric("Diferença €/h", f"{resultados['diferença_hora']:.2f}")

        col1, col2, col3 = st.columns(3)
        col1.metric("Alugado €/km", f"{alugado['custo_km']:.2f}")
        col2.metric("Próprio €/km", f"{proprio['custo_km']:.2f}")
        col3.metric("Diferença €/km", f"{resultados['diferença_km']:.2f}")

    if st.session_state.include_extra_expenses:
        st.info(f"💡 Despesas extras informativas: € {st.session_state.extra_expenses:.2f} por semana (não afeta os cálculos).")
