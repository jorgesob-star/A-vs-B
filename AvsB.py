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
  
# ---  
# Lógica de Inicialização dos Parâmetros  
# ---  
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
  
# ---  
# Seção de Entrada de Dados e Parâmetros  
# ---  
col1, col2 = st.columns(2)  
  
with col1:  
    st.header("📊 Dados de Entrada")  
      
    weekly_earnings = st.number_input(  
        "Ganhos Semanais (€):",   
        min_value=0.0,   
        value=999.0,   
        step=50.0,  
        help="Valor total ganho por semana antes de despesas"  
    )  
      
    weekly_hours = st.number_input(  
        "Horas Trabalhadas por Semana:",   
        min_value=0.0,   
        value=56.0,   
        step=1.0,  
        help="Total de horas trabalhadas na semana"  
    )  
      
    fuel_cost = st.number_input(  
        "Custo Semanal com Combustível (€):",   
        min_value=0.0,   
        value=170.0,   
        step=10.0,  
        help="Custo semanal estimado com combustível"  
    )  
  
with col2:  
    st.header("📏 Quilometragem")  
    weekly_km = st.number_input(  
        "Quilómetros percorridos por semana:",  
        min_value=0.0,  
        value=1200.0,  
        step=50.0,  
        help="Número estimado de km percorridos semanalmente"  
    )  
  
# Despesas extras (fora dos parâmetros, sempre visíveis)  
st.header("💸 Despesas Extras")  
  
extra_col1, extra_col2 = st.columns(2)  
  
with extra_col1:  
    st.session_state.include_extra_expenses = st.checkbox(  
        "Incluir despesas extras no cálculo",  
        value=st.session_state.include_extra_expenses,  
        help="Marque para incluir despesas extras no cálculo do lucro final"  
    )  
  
with extra_col2:  
    if st.session_state.include_extra_expenses:  
        st.session_state.extra_expenses = st.number_input(  
            "Despesas Extras Semanais (€):",   
            min_value=0.0,   
            value=st.session_state.extra_expenses,   
            step=5.0,  
            help="Despesas adicionais como estacionamento, portagens, lavagens, etc."  
        )  
  
# Botão para mostrar/ocultar parâmetros  
if st.button("⚙️ Parâmetros Avançados"):  
    st.session_state.show_params = not st.session_state.show_params  
  
# Mostrar parâmetros apenas se show_params for True  
if st.session_state.show_params:  
    st.header("⚙️ Parâmetros Avançados")  
      
    adv_col1, adv_col2 = st.columns(2)  
      
    with adv_col1:  
        st.subheader("Carro Alugado")  
        st.session_state.rental_cost = st.number_input(  
            "Custo do Aluguel (€/semana):",   
            min_value=0.0,   
            value=st.session_state.rental_cost,   
            step=10.0  
        )  
        st.session_state.rental_commission = st.number_input(  
            "Comissão com Carro Alugado (%):",   
            min_value=0.0,   
            max_value=30.0,   
            value=st.session_state.rental_commission,   
            step=0.5,  
            help="Percentual que a plataforma retém pelos serviços com carro alugado"  
        )  
      
    with adv_col2:  
        st.subheader("Carro Próprio")  
        st.session_state.own_insurance = st.number_input(  
            "Seguro (€/semana):",   
            min_value=0.0,   
            value=st.session_state.own_insurance,   
            step=5.0  
        )  
        st.session_state.own_maintenance = st.number_input(  
            "Manutenção (€/semana):",   
            min_value=0.0,   
            value=st.session_state.own_maintenance,   
            step=5.0,  
            help="Custo semanal estimado com manutenção do veículo próprio"  
        )  
        st.session_state.own_commission = st.number_input(  
            "Comissão com Carro Próprio (%):",   
            min_value=0.0,   
            max_value=30.0,   
            value=st.session_state.own_commission,   
            step=0.5,  
            help="Percentual que a plataforma retém pelos serviços com carro próprio"  
        )  
  
# ---  
# Botões de Cálculo  
# ---  
st.header("🧮 Calcular")  
  
calc_col1, calc_col2, calc_col3 = st.columns(3)  
  
with calc_col1:  
    if st.button("Calcular Carro Alugado", type="primary", use_container_width=True):  
        st.session_state.calculation_type = "alugado"  
  
with calc_col2:  
    if st.button("Calcular Carro Próprio", type="primary", use_container_width=True):  
        st.session_state.calculation_type = "próprio"  
  
with calc_col3:  
    if st.button("Comparar Ambos", type="primary", use_container_width=True):  
        st.session_state.calculation_type = "comparar"  
  
# ---  
# Função de Cálculo  
# ---  
def calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km, calculation_type):  
    resultados = {}  
  
    # Carro Alugado  
    if calculation_type in ["alugado", "comparar"]:  
        rental_commission_value = weekly_earnings * (st.session_state.rental_commission / 100)  
        rental_net_before_extras = weekly_earnings - rental_commission_value - st.session_state.rental_cost - fuel_cost  
        rental_hourly = rental_net_before_extras / weekly_hours if weekly_hours > 0 else 0  
        if st.session_state.include_extra_expenses:  
            rental_net_final = rental_net_before_extras - st.session_state.extra_expenses  
        else:  
            rental_net_final = rental_net_before_extras  
  
        # Custos por km  
        fuel_per_km = fuel_cost / weekly_km if weekly_km > 0 else 0  
        total_costs = st.session_state.rental_cost + fuel_cost  
        if st.session_state.include_extra_expenses:  
            total_costs += st.session_state.extra_expenses  
        total_per_km = total_costs / weekly_km if weekly_km > 0 else 0  
        profit_per_km = rental_net_final / weekly_km if weekly_km > 0 else 0  
  
        resultados["alugado"] = {  
            "líquido": rental_net_final,  
            "antes_extras": rental_net_before_extras,  
            "hora": rental_hourly,  
            "comissao": rental_commission_value,  
            "fuel_km": fuel_per_km,  
            "total_km": total_per_km,  
            "profit_km": profit_per_km,  
        }  
  
    # Carro Próprio  
    if calculation_type in ["próprio", "comparar"]:  
        own_commission_value = weekly_earnings * (st.session_state.own_commission / 100)  
        own_net_before_extras = weekly_earnings - own_commission_value - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost  
        own_hourly = own_net_before_extras / weekly_hours if weekly_hours > 0 else 0  
        if st.session_state.include_extra_expenses:  
            own_net_final = own_net_before_extras - st.session_state.extra_expenses  
        else:  
            own_net_final = own_net_before_extras  
  
        # Custos por km  
        fuel_per_km = fuel_cost / weekly_km if weekly_km > 0 else 0  
        total_costs = st.session_state.own_insurance + st.session_state.own_maintenance + fuel_cost  
        if st.session_state.include_extra_expenses:  
            total_costs += st.session_state.extra_expenses  
        total_per_km = total_costs / weekly_km if weekly_km > 0 else 0  
        profit_per_km = own_net_final / weekly_km if weekly_km > 0 else 0  
  
        resultados["próprio"] = {  
            "líquido": own_net_final,  
            "antes_extras": own_net_before_extras,  
            "hora": own_hourly,  
            "comissao": own_commission_value,  
            "fuel_km": fuel_per_km,  
            "total_km": total_per_km,  
            "profit_km": profit_per_km,  
        }  
  
    # Diferenças na comparação  
    if calculation_type == "comparar" and "alugado" in resultados and "próprio" in resultados:  
        resultados["diferença"] = resultados["alugado"]["líquido"] - resultados["próprio"]["líquido"]  
        resultados["diferença_hora"] = resultados["alugado"]["hora"] - resultados["próprio"]["hora"]  
        resultados["diferença_km"] = resultados["alugado"]["profit_km"] - resultados["próprio"]["profit_km"]  
  
    return resultados  
  
# ---  
# Resultados  
# ---  
if st.session_state.calculation_type:  
    resultados = calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost, weekly_km, st.session_state.calculation_type)  
    st.header("📈 Resultados")  
  
    # Carro Alugado  
    if st.session_state.calculation_type == "alugado" and "alugado" in resultados:  
        alugado = resultados["alugado"]  
        st.subheader("Carro Alugado")  
        col1, col2 = st.columns(2)  
        with col1:  
            st.metric("Total Líquido Semanal", f"€ {alugado['líquido']:.2f}")  
            if st.session_state.include_extra_expenses:  
                st.metric("Antes das Despesas Extras", f"€ {alugado['antes_extras']:.2f}")  
        with col2:  
            st.metric("Média Horária", f"€ {alugado['hora']:.2f}")  
  
        st.subheader("🚦 Indicadores por Km")  
        col1, col2, col3 = st.columns(3)  
        with col1:  
            st.metric("Combustível/km", f"€ {alugado['fuel_km']:.3f}")  
        with col2:  
            st.metric("Custo total/km", f"€ {alugado['total_km']:.3f}")  
        with col3:  
            st.metric("Lucro líquido/km", f"€ {alugado['profit_km']:.3f}")  
  
    # Carro Próprio  
    elif st.session_state.calculation_type == "próprio" and "próprio" in resultados:  
        proprio = resultados["próprio"]  
        st.subheader("Carro Próprio")  
        col1, col2 = st.columns(2)  
        with col1:  
            st.metric("Total Líquido Semanal", f"€ {proprio['líquido']:.2f}")  
            if st.session_state.include_extra_expenses:  
                st.metric("Antes das Despesas Extras", f"€ {proprio['antes_extras']:.2f}")  
        with col2:  
            st.metric("Média Horária", f"€ {proprio['hora']:.2f}")  
  
        st.subheader("🚦 Indicadores por Km")  
        col1, col2, col3 = st.columns(3)  
        with col1:  
            st.metric("Combustível/km", f"€ {proprio['fuel_km']:.3f}")  
        with col2:  
            st.metric("Custo total/km", f"€ {proprio['total_km']:.3f}")  
        with col3:  
            st.metric("Lucro líquido/km", f"€ {proprio['profit_km']:.3f}")  
  
    # Comparação  
    elif st.session_state.calculation_type == "comparar" and "alugado" in resultados and "próprio" in resultados:  
        alugado = resultados["alugado"]  
        proprio = resultados["próprio"]  
        st.subheader("Comparação Semanal")  
        col1, col2, col3 = st.columns(3)  
        with col1:  
            st.metric("Alugado (líquido)", f"€ {alugado['líquido']:.2f}")  
        with col2:  
            st.metric("Próprio (líquido)", f"€ {proprio['líquido']:.2f}")  
        with col3:  
            st.metric("Diferença", f"€ {resultados['diferença']:.2f}")  
  
        st.subheader("🚦 Comparação por Km")  
        col1, col2, col3 = st.columns(3)  
        with col1:  
            st.metric("Alugado lucro/km", f"€ {alugado['profit_km']:.3f}")  
        with col2:  
            st.metric("Próprio lucro/km", f"€ {proprio['profit_km']:.3f}")  
        with col3:  
            st.metric("Diferença/km", f"€ {resultados['diferença_km']:.3f}")  
  
# ---  
# Rodapé  
# ---  
with st.expander("💡 Dicas e Informações"):  
    st.markdown("""  
    - **Ganhos Semanais**: valor total recebido pelos serviços.  
    - **Horas Trabalhadas**: total de horas semanais (inclui espera).  
    - **Quilometragem**: total de km percorridos na semana.  
    - **Custos por km**: úteis para comparar eficiência e planeamento.  
    """)
