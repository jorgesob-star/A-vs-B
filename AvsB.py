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
if 'extra_expenses' not in st.session_state:
    st.session_state.extra_expenses = 0.0
if 'include_extra_expenses' not in st.session_state:
    st.session_state.include_extra_expenses = False

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
    
    weekly_hours = st.number_input(
        "Horas Trabalhadas por Semana:", 
        min_value=0.0, 
        value=40.0, 
        step=1.0,
        help="Total de horas trabalhadas na semana"
    )
    
    fuel_cost = st.number_input(
        "Custo Semanal com Combustível (€):", 
        min_value=0.0, 
        value=200.0, 
        step=10.0,
        help="Custo semanal estimado com combustível"
    )

# Botão para mostrar/ocultar parâmetros
if st.button("⚙️ Parâmetros"):
    st.session_state.show_params = not st.session_state.show_params

# Mostrar parâmetros apenas se show_params for True
if st.session_state.show_params:
    with col2:
        st.header("⚙️ Parâmetros")
        
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
        
        st.session_state.own_commission = st.slider(
            "Comissão com Carro Próprio (%):", 
            min_value=0, 
            max_value=30, 
            value=st.session_state.own_commission, 
            step=1
        )
        
        # Despesas extras (aplicáveis a ambos os cenários)
        st.subheader("Despesas Extras")
        st.session_state.include_extra_expenses = st.checkbox(
            "Incluir despesas extras no cálculo",
            value=st.session_state.include_extra_expenses,
            help="Marque para incluir despesas extras no cálculo do lucro final"
        )
        
        if st.session_state.include_extra_expenses:
            st.session_state.extra_expenses = st.number_input(
                "Despesas Extras Semanais (€):", 
                min_value=0.0, 
                value=st.session_state.extra_expenses, 
                step=5.0,
                help="Despesas adicionais como estacionamento, portagens, lavagens, etc."
            )

# ---
# Seção de Cálculos
# ---

# Função para realizar os cálculos
def calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost):
    # Calcular para carro alugado (sem despesas extras)
    rental_commission_value = weekly_earnings * (st.session_state.rental_commission / 100)
    rental_net_before_extras = weekly_earnings - rental_commission_value - st.session_state.rental_cost - fuel_cost
    rental_hourly = rental_net_before_extras / weekly_hours if weekly_hours > 0 else 0
    
    # Aplicar despesas extras se selecionado
    if st.session_state.include_extra_expenses:
        rental_net_final = rental_net_before_extras - st.session_state.extra_expenses
    else:
        rental_net_final = rental_net_before_extras
    
    # Calcular para carro próprio (sem despesas extras)
    own_commission_value = weekly_earnings * (st.session_state.own_commission / 100)
    own_net_before_extras = weekly_earnings - own_commission_value - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost
    own_hourly = own_net_before_extras / weekly_hours if weekly_hours > 0 else 0
    
    # Aplicar despesas extras se selecionado
    if st.session_state.include_extra_expenses:
        own_net_final = own_net_before_extras - st.session_state.extra_expenses
    else:
        own_net_final = own_net_before_extras
    
    difference = rental_net_final - own_net_final
    difference_hourly = rental_hourly - own_hourly
    
    return (rental_net_final, own_net_final, difference, rental_commission_value, 
            own_commission_value, rental_hourly, own_hourly, difference_hourly,
            rental_net_before_extras, own_net_before_extras)

# Botão de cálculo
if st.button("Calcular", type="primary"):
    (rental_net, own_net, difference, rental_commission_value, 
     own_commission_value, rental_hourly, own_hourly, difference_hourly,
     rental_before_extras, own_before_extras) = calcular_ganhos(weekly_earnings, weekly_hours, fuel_cost)
    
    # ---
    # Seção de Resultados
    # ---

    st.header("📈 Resultados")
    
    # Métricas semanais
    st.subheader("Resultados Semanais")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Carro Alugado (Líquido Semanal)", 
            f"€ {rental_net:.2f}",
            delta_color="inverse" if rental_net < 0 else "normal"
        )
    
    with col2:
        st.metric(
            "Carro Próprio (Líquido Semanal)", 
            f"€ {own_net:.2f}",
            delta_color="inverse" if own_net < 0 else "normal"
        )
    
    with col3:
        st.metric(
            "Diferença Semanal", 
            f"€ {difference:.2f}",
            delta_color="inverse" if difference < 0 else "normal"
        )
    
    # Métricas horárias (calculadas SEM despesas extras)
    st.subheader("Média Horária (sem despesas extras)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Carro Alugado (€/hora)", 
            f"€ {rental_hourly:.2f}",
            delta_color="inverse" if rental_hourly < 0 else "normal"
        )
    
    with col2:
        st.metric(
            "Carro Próprio (€/hora)", 
            f"€ {own_hourly:.2f}",
            delta_color="inverse" if own_hourly < 0 else "normal"
        )
    
    with col3:
        st.metric(
            "Diferença Horária", 
            f"€ {difference_hourly:.2f}",
            delta_color="inverse" if difference_hourly < 0 else "normal"
        )
    
    # Detalhamento dos cálculos
    st.subheader("Detalhamento dos Cálculos")
    
    # Preparar dados para a tabela
    comparison_data = {
        "Descrição": [
            "Ganhos Semanais",
            f"Comissão ({st.session_state.rental_commission}%)",
            "Custo do Aluguel",
            "Seguro",
            "Manutenção",
            "Custo com Combustível",
            "Subtotal (antes de despesas extras)",
        ],
        "Carro Alugado (€)": [
            weekly_earnings,
            -rental_commission_value,
            -st.session_state.rental_cost,
            "N/A",
            "N/A",
            -fuel_cost,
            rental_before_extras,
        ],
        "Carro Próprio (€)": [
            weekly_earnings,
            -own_commission_value,
            "N/A",
            -st.session_state.own_insurance,
            -st.session_state.own_maintenance,
            -fuel_cost,
            own_before_extras,
        ]
    }
    
    # Adicionar linha de despesas extras se aplicável
    if st.session_state.include_extra_expenses:
        comparison_data["Descrição"].append("Despesas Extras")
        comparison_data["Carro Alugado (€)"].append(-st.session_state.extra_expenses)
        comparison_data["Carro Próprio (€)"].append(-st.session_state.extra_expenses)
        
        comparison_data["Descrição"].append("Total Líquido Final")
        comparison_data["Carro Alugado (€)"].append(rental_net)
        comparison_data["Carro Próprio (€)"].append(own_net)
    else:
        comparison_data["Descrição"].append("Total Líquido Final")
        comparison_data["Carro Alugado (€)"].append(rental_net)
        comparison_data["Carro Próprio (€)"].append(own_net)
    
    # Adicionar horas e média horária
    comparison_data["Descrição"].extend(["Horas Trabalhadas", "Média Horária (€/hora)"])
    comparison_data["Carro Alugado (€)"].extend([weekly_hours, rental_hourly])
    comparison_data["Carro Próprio (€)"].extend([weekly_hours, own_hourly])
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Recomendação
    st.subheader("Recomendação")
    if difference > 0.01:
        st.success(f"✅ O carro alugado é mais vantajoso por € {difference:.2f} por semana.")
    elif difference < -0.01:
        st.success(f"✅ O carro próprio é mais vantajoso por € {abs(difference):.2f} por semana.")
    else:
        st.info("ℹ️ Ambas as opções têm o mesmo resultado financeiro.")
    
    # Visualização gráfica
    st.subheader("Comparação Visual")
    
    tab1, tab2, tab3 = st.tabs(["Lucro Semanal", "Média Horária", "Comparativo Completo"])
    
    with tab1:
        chart_data_weekly = pd.DataFrame({
            "Opção": ["Carro Alugado", "Carro Próprio"],
            "Lucro Líquido Semanal (€)": [rental_net, own_net]
        })
        st.bar_chart(chart_data_weekly, x="Opção", y="Lucro Líquido Semanal (€)")
    
    with tab2:
        chart_data_hourly = pd.DataFrame({
            "Opção": ["Carro Alugado", "Carro Próprio"],
            "Média Horária (€)": [rental_hourly, own_hourly]
        })
        st.bar_chart(chart_data_hourly, x="Opção", y="Média Horária (€)")
        
    with tab3:
        # Gráfico comparativo completo
        comparativo_data = pd.DataFrame({
            "Categoria": [
                "Ganhos Semanais", 
                "Comissão", 
                "Custo Aluguel/Seguro", 
                "Manutenção", 
                "Combustível"
            ],
            "Carro Alugado (€)": [
                weekly_earnings,
                -rental_commission_value,
                -st.session_state.rental_cost,
                0,
                -fuel_cost
            ],
            "Carro Próprio (€)": [
                weekly_earnings,
                -own_commission_value,
                -st.session_state.own_insurance,
                -st.session_state.own_maintenance,
                -fuel_cost
            ]
        })
        
        # Adicionar despesas extras se aplicável
        if st.session_state.include_extra_expenses:
            extras_row = pd.DataFrame({
                "Categoria": ["Despesas Extras"],
                "Carro Alugado (€)": [-st.session_state.extra_expenses],
                "Carro Próprio (€)": [-st.session_state.extra_expenses]
            })
            comparativo_data = pd.concat([comparativo_data, extras_row], ignore_index=True)
        
        st.bar_chart(comparativo_data.set_index("Categoria"))

# ---
# Informações Adicionais e Rodapé
# ---

with st.expander("💡 Dicas e Informações"):
    st.markdown("""
    - **Ganhos Semanais**: Valor total que você recebe pelos serviços de TVDE em uma semana.
    - **Horas Trabalhadas**: Total de horas trabalhadas na semana (incluindo tempo de espera).
    - **Custo com Combustível**: Gasto semanal estimado com abastecimento.
    - **Comissão**: Percentual que a plataforma retém pelos serviços.
    - **Custo do Aluguel**: Valor semanal pelo aluguel do veículo (se aplicável).
    - **Seguro**: Custo semanal do seguro do veículo próprio.
    - **Manutenção**: Custo semanal estimado com manutenção do veículo próprio.
    - **Despesas Extras**: Custos adicionais como estacionamento, portagens, lavagens, etc.
                
    ⚠️ Notas importantes:
    - As médias horárias são calculadas SEM incluir as despesas extras
    - As despesas extras são aplicadas apenas no lucro final
    - Considere outros custos não incluídos aqui, como desvalorização do veículo e impostos
    """)

st.markdown("---")
st.caption("Desenvolvido para ajudar motoristas TVDE a tomar decisões financeiras informadas.")
