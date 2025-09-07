import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Comparador de Ganhos TVDE",
    page_icon="🚗",
    layout="wide"
)

# Estilo CSS para melhorar a aparência
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {background-color: #4CAF50; color: white; border-radius: 8px;}
    .stButton>button:hover {background-color: #45a049;}
    .stNumberInput input {border-radius: 5px;}
    .stMetric {border: 1px solid #ddd; border-radius: 8px; padding: 10px;}
    .stExpander {border: 1px solid #ddd; border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# Título da aplicação
st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("Compare os lucros entre usar carro alugado e carro próprio para trabalhar como motorista TVDE.", unsafe_allow_html=True)

# ---
# Lógica de Inicialização dos Parâmetros
# ---
if 'show_params' not in st.session_state:
    st.session_state.show_params = False
if 'rental_cost' not in st.session_state:
    st.session_state.rental_cost = 280.0
if 'rental_commission' not in st.session_state:
    st.session_state.rental_commission = 7.0
if 'own_insurance' not in st.session_state:
    st.session_state.own_insurance = 45.0
if 'own_maintenance' not in st.session_state:
    st.session_state.own_maintenance = 50.0
if 'own_commission' not in st.session_state:
    st.session_state.own_commission = 12.0
if 'other_costs' not in st.session_state:
    st.session_state.other_costs = 0.0

# ---
# Seção de Entrada de Dados
# ---
st.header("📊 Dados de Entrada")
col1, col2 = st.columns([1, 1])

with col1:
    weekly_earnings = st.number_input(
        "Ganhos Semanais (€):",
        min_value=0.0,
        value=800.0,
        step=50.0,
        help="Valor total ganho por semana antes de despesas",
        format="%.2f"
    )
    
    fuel_cost = st.number_input(
        "Custo Semanal com Combustível (€):",
        min_value=0.0,
        value=200.0,
        step=10.0,
        help="Custo semanal estimado com combustível",
        format="%.2f"
    )

with col2:
    st.session_state.other_costs = st.number_input(
        "Outros Custos Semanais (€):",
        min_value=0.0,
        value=st.session_state.other_costs,
        step=5.0,
        help="Custos adicionais, como lavagem, estacionamento ou portagens",
        format="%.2f"
    )

# Botão para mostrar/ocultar parâmetros
if st.button("⚙️ Mostrar/Ocultar Parâmetros"):
    st.session_state.show_params = not st.session_state.show_params

# Botão para redefinir parâmetros
if st.session_state.show_params:
    if st.button("🔄 Redefinir Parâmetros"):
        st.session_state.rental_cost = 280.0
        st.session_state.rental_commission = 7.0
        st.session_state.own_insurance = 45.0
        st.session_state.own_maintenance = 50.0
        st.session_state.own_commission = 12.0
        st.session_state.other_costs = 0.0
        st.session_state.show_params = False
        st.rerun()

# Mostrar parâmetros apenas se show_params for True
if st.session_state.show_params:
    st.header("⚙️ Parâmetros Avançados")
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Carro Alugado")
        st.session_state.rental_cost = st.number_input(
            "Custo do Aluguel (€/semana):",
            min_value=0.0,
            value=st.session_state.rental_cost,
            step=10.0,
            format="%.2f"
        )
        st.session_state.rental_commission = st.number_input(
            "Comissão com Carro Alugado (%):",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.rental_commission,
            step=1.0,
            format="%.1f"
        )
    
    with col4:
        st.subheader("Carro Próprio")
        st.session_state.own_insurance = st.number_input(
            "Seguro (€/semana):",
            min_value=0.0,
            value=st.session_state.own_insurance,
            step=5.0,
            format="%.2f"
        )
        st.session_state.own_maintenance = st.number_input(
            "Manutenção (€/semana):",
            min_value=0.0,
            value=st.session_state.own_maintenance,
            step=5.0,
            help="Custo semanal estimado com manutenção do veículo próprio",
            format="%.2f"
        )
        st.session_state.own_commission = st.number_input(
            "Comissão com Carro Próprio (%):",
            min_value=0.0,
            max_value=100.0,
            value=st.session_state.own_commission,
            step=1.0,
            format="%.1f"
        )

# ---
# Seção de Cálculos
# ---
def calcular_ganhos(weekly_earnings, fuel_cost, other_costs):
    """
    Calcula os lucros líquidos para carro alugado e próprio, considerando comissões e custos.
    Args:
        weekly_earnings (float): Ganhos semanais brutos.
        fuel_cost (float): Custo semanal com combustível.
        other_costs (float): Outros custos semanais (lavagem, estacionamento, etc.).
    Returns:
        tuple: Lucro líquido (alugado, próprio), diferença, valores das comissões.
    """
    # Carro alugado
    rental_commission_value = weekly_earnings * (st.session_state.rental_commission / 100)
    rental_net = weekly_earnings - rental_commission_value - st.session_state.rental_cost - fuel_cost - other_costs
    
    # Carro próprio
    own_commission_value = weekly_earnings * (st.session_state.own_commission / 100)
    own_net = weekly_earnings - own_commission_value - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost - other_costs
    
    difference = rental_net - own_net
    
    return rental_net, own_net, difference, rental_commission_value, own_commission_value

# Botão de cálculo
if st.button("Calcular", type="primary"):
    # Validação de entradas
    if weekly_earnings == 0 and fuel_cost == 0 and st.session_state.other_costs == 0:
        st.error("🚫 Por favor, insira valores válidos para ganhos ou custos.")
        st.stop()
    
    rental_net, own_net, difference, rental_commission_value, own_commission_value = calcular_ganhos(
        weekly_earnings, fuel_cost, st.session_state.other_costs
    )
    
    # ---
    # Seção de Resultados
    # ---
    st.header("📈 Resultados")
    
    # Métricas
    col5, col6, col7 = st.columns(3)
    
    with col5:
        st.metric(
            "Carro Alugado (Líquido Semanal)",
            f"€ {rental_net:.2f}",
            delta=f"{rental_net-own_net:.2f} € vs. Próprio",
            delta_color="inverse" if rental_net < own_net else "normal"
        )
    
    with col6:
        st.metric(
            "Carro Próprio (Líquido Semanal)",
            f"€ {own_net:.2f}",
            delta=f"{own_net-rental_net:.2f} € vs. Alugado",
            delta_color="inverse" if own_net < rental_net else "normal"
        )
    
    with col7:
        annual_difference = difference * 52
        st.metric(
            "Diferença Anual",
            f"€ {annual_difference:.2f}",
            delta_color="inverse" if difference < 0 else "normal"
        )
    
    # Detalhamento dos cálculos
    st.subheader("Detalhamento dos Cálculos")
    
    comparison_data = {
        "Descrição": [
            "Ganhos Semanais",
            "Comissão",
            "Custo do Aluguel",
            "Seguro",
            "Manutenção",
            "Custo com Combustível",
            "Outros Custos",
            "Total Líquido"
        ],
        "Carro Alugado (€)": [
            f"{weekly_earnings:.2f}",
            f"-{rental_commission_value:.2f} ({st.session_state.rental_commission}%)",
            f"-{st.session_state.rental_cost:.2f}",
            "0.00",
            "0.00",
            f"-{fuel_cost:.2f}",
            f"-{st.session_state.other_costs:.2f}",
            f"{rental_net:.2f}"
        ],
        "Carro Próprio (€)": [
            f"{weekly_earnings:.2f}",
            f"-{own_commission_value:.2f} ({st.session_state.own_commission}%)",
            "0.00",
            f"-{st.session_state.own_insurance:.2f}",
            f"-{st.session_state.own_maintenance:.2f}",
            f"-{fuel_cost:.2f}",
            f"-{st.session_state.other_costs:.2f}",
            f"{own_net:.2f}"
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Exportação como CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Baixar Resultados como CSV",
        data=csv,
        file_name="resultados_tvde.csv",
        mime="text/csv"
    )
    
    # Recomendação
    st.subheader("Recomendação")
    if difference > 0.01:
        st.success(f"✅ O carro alugado é mais vantajoso por € {difference:.2f} por semana, ou € {difference*52:.2f} por ano.")
    elif difference < -0.01:
        st.success(f"✅ O carro próprio é mais vantajoso por € {abs(difference):.2f} por semana, ou € {abs(difference*52):.2f} por ano.")
    else:
        st.info("ℹ️ Ambas as opções têm o mesmo resultado financeiro.")
    
    # Visualização gráfica
    st.subheader("Comparação Visual")
    chart_data = pd.DataFrame({
        "Opção": ["Carro Alugado", "Carro Próprio"],
        "Lucro Líquido (€)": [rental_net, own_net]
    })
    
    fig = px.bar(
        chart_data,
        x="Opção",
        y="Lucro Líquido (€)",
        text_auto=".2f",
        color="Opção",
        color_discrete_map={"Carro Alugado": "#4CAF50", "Carro Próprio": "#2196F3"},
        title="Lucro Líquido Semanal"
    )
    fig.update_layout(showlegend=False, title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# ---
# Informações Adicionais e Rodapé
# ---
with st.expander("💡 Dicas e Informações"):
    st.markdown("""
    - **Ganhos Semanais**: Valor total que você recebe pelos serviços de TVDE em uma semana.
    - **Custo com Combustível**: Gasto semanal estimado com abastecimento.
    - **Outros Custos**: Inclui lavagens, estacionamento, portagens ou outros custos variáveis.
    - **Comissão**: Percentual que a plataforma retém pelos serviços.
    - **Custo do Aluguel**: Valor semanal pelo aluguel do veículo (se aplicável).
    - **Seguro**: Custo semanal do seguro do veículo próprio.
    - **Manutenção**: Custo semanal estimado com manutenção do veículo próprio.
                
    ⚠️ Considere outros fatores não incluídos aqui, como:
    - Desvalorização do veículo (no caso de carro próprio)
    - Impostos e taxas
    - Custos imprevistos (ex.: multas, reparos)
    """)

st.markdown("---")
st.caption("Desenvolvido para ajudar motoristas TVDE a tomar decisões financeiras informadas. 🚗")
