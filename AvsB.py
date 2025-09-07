import streamlit as st  
import pandas as pd  

# Configuração da página  
st.set_page_config(  
    page_title="Comparador de Ganhos TVDE",  
    page_icon="🚗",  
    layout="wide"  
)  

# Título da aplicação  
st.title("🚗 Comparador de Ganhos TVDE")  
st.markdown("Compare os lucros entre usar carro alugado e carro próprio para trabalhar como motorista TVDE.")  

# --- Inicialização dos Parâmetros ---  
if 'show_params' not in st.session_state:  
    st.session_state.show_params = False  
if 'rental_cost' not in st.session_state:  
    st.session_state.rental_cost = 270.0  
if 'rental_commission' not in st.session_state:  
    st.session_state.rental_commission = 6.0  
if 'own_insurance' not in st.session_state:  
    st.session_state.own_insurance = 45.0  
if 'own_maintenance' not in st.session_state:  
    st.session_state.own_maintenance = 50.0  
if 'own_commission' not in st.session_state:  
    st.session_state.own_commission = 12.0  
if 'extra_expenses' not in st.session_state:  
    st.session_state.extra_expenses = 0.0  
if 'include_extra_expenses' not in st.session_state:  
    st.session_state.include_extra_expenses = False  
if 'calculation_type' not in st.session_state:  
    st.session_state.calculation_type = None  

# --- Entrada de Dados ---  
col1, col2 = st.columns(2)  

with col1:  
    st.header("📊 Dados de Entrada")  
    weekly_earnings = st.number_input("Ganhos Semanais (€):", min_value=0.0, value=999.0, step=50.0)  
    weekly_hours = st.number_input("Horas Trabalhadas por Semana:", min_value=0.0, value=56.0, step=1.0)  
    fuel_cost = st.number_input("Custo Semanal com Combustível (€):", min_value=0.0, value=170.0, step=10.0)  

with col2:  
    st.header("📏 Quilometragem")  
    weekly_km = st.number_input("Quilómetros percorridos por semana:", min_value=0.0, value=1200.0, step=50.0)  

# Despesas Extras  
st.header("💸 Despesas Extras")  
extra_col1, extra_col2 = st.columns(2)  
with extra_col1:  
    st.session_state.include_extra_expenses = st.checkbox("Incluir despesas extras (informativo)", value=st.session_state.include_extra_expenses)  
with extra_col2:  
    if st.session_state.include_extra_expenses:  
        st.session_state.extra_expenses = st.number_input("Despesas Extras Semanais (€):", min_value=0.0, value=st.session_state.extra_expenses, step=5.0)  

# Parâmetros Avançados  
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

# Botões de Cálculo  
st.header("🧮 Calcular")  
calc_col1, calc_col2, calc_col3 = st.columns(3)  
with calc_col1:  
    if st.button("Calcular Carro Alugado"):  
        st.session_state.calculation_type = "alugado"  
with calc_col2:  
    if st.button("Calcular Carro Próprio"):  
        st.session_state.calculation_type = "próprio"  
with calc_col3:  
    if st.button("Comparar Ambos"):  
        st.session_state.calculation_type = "comparar"  

# --- Função de Cálculo ---  
def calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km, calculation_type):  
    resultados = {}  
    if calculation_type in ["alugado", "comparar"]:  
        rental_commission_value = weekly_earnings * (st.session_state.rental_commission / 100)  
        rental_net = weekly_earnings - rental_commission_value - st.session_state.rental_cost - fuel_cost  
        resultados["alugado"] = {  
            "líquido": rental_net,  
            "hora": rental_net / weekly_hours if weekly_hours > 0 else 0,  
            "fuel_km": fuel_cost / weekly_km if weekly_km > 0 else 0,  
            "total_km": (st.session_state.rental_cost + fuel_cost) / weekly_km if weekly_km > 0 else 0,  
            "profit_km": rental_net / weekly_km if weekly_km > 0 else 0  
        }  
    if calculation_type in ["próprio", "comparar"]:  
        own_commission_value = weekly_earnings * (st.session_state.own_commission / 100)  
        own_net = weekly_earnings - own_commission_value - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost  
        resultados["próprio"] = {  
            "líquido": own_net,  
            "hora": own_net / weekly_hours if weekly_hours > 0 else 0,  
            "fuel_km": fuel_cost / weekly_km if weekly_km > 0 else 0,  
            "total_km": (st.session_state.own_insurance + st.session_state.own_maintenance + fuel_cost) / weekly_km if weekly_km > 0 else 0,  
            "profit_km": own_net / weekly_km if weekly_km > 0 else 0  
        }  
    if calculation_type == "comparar" and "alugado" in resultados and "próprio" in resultados:  
        resultados["diferença"] = resultados["alugado"]["líquido"] - resultados["próprio"]["líquido"]  
        resultados["diferença_hora"] = resultados["alugado"]["hora"] - resultados["próprio"]["hora"]  
        resultados["diferença_km"] = resultados["alugado"]["profit_km"] - resultados["próprio"]["profit_km"]  
    return resultados  

# --- Executar e Mostrar Resultados ---  
if st.session_state.calculation_type:  
    resultados = calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km, st.session_state.calculation_type)  
    st.header("📈 Resultados")  

    if st.session_state.calculation_type == "comparar":  
        alugado = resultados["alugado"]  
        proprio = resultados["próprio"]  

        st.subheader("Comparação Visual")  
        tab1, tab2, tab3 = st.tabs(["Lucro Semanal", "Média Horária", "Lucro por Km"])  

        with tab1:  
            st.bar_chart(pd.DataFrame({"Opção": ["Carro Alugado", "Carro Próprio"], "Lucro Líquido Semanal (€)": [alugado['líquido'], proprio['líquido']]}), x="Opção", y="Lucro Líquido Semanal (€)")  

        with tab2:  
            st.bar_chart(pd.DataFrame({"Opção": ["Carro Alugado", "Carro Próprio"], "Média Horária (€)": [alugado['hora'], proprio['hora']]}), x="Opção", y="Média Horária (€)")  

        with tab3:  
            st.bar_chart(pd.DataFrame({"Opção": ["Carro Alugado", "Carro Próprio"], "Lucro por Km (€)": [alugado['profit_km'], proprio['profit_km']]}), x="Opção", y="Lucro por Km (€)")  

    if st.session_state.include_extra_expenses:  
        st.info(f"💡 Despesas extras informativas: € {st.session_state.extra_expenses:.2f} por semana (não afeta os cálculos).")
