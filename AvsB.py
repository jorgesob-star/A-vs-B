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
    
    # Período de comparação
    st.session_state.weeks_comparison = st.number_input(
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
        
        st.session_state.rental_commission = st.number_input(
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
        
        st.session_state.own_commission = st.number_input(
            "Comissão com Carro Próprio (%):", 
            min_value=0, 
            max_value=30, 
            value=st.session_state.own_commission, 
            step=1
        )

# ---
# Seção de Cálculos
# ---

# Função para realizar os cálculos
def calcular_ganhos(weekly_earnings, fuel_cost, weeks=1):
    # Calcular para carro alugado
    rental_commission_value = weekly_earnings * (st.session_state.rental_commission / 100)
    rental_net_weekly = weekly_earnings - rental_commission_value - st.session_state.rental_cost - fuel_cost
    rental_net_total = rental_net_weekly * weeks
    
    # Calcular para carro próprio
    own_commission_value = weekly_earnings * (st.session_state.own_commission / 100)
    own_net_weekly = weekly_earnings - own_commission_value - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost
    own_net_total = own_net_weekly * weeks
    
    difference_weekly = rental_net_weekly - own_net_weekly
    difference_total = rental_net_total - own_net_total
    
    return (rental_net_weekly, rental_net_total, own_net_weekly, own_net_total, 
            difference_weekly, difference_total, rental_commission_value, own_commission_value)

# Botão de cálculo
if st.button("Calcular", type="primary"):
    (rental_net_weekly, rental_net_total, own_net_weekly, own_net_total, 
     difference_weekly, difference_total, rental_commission_value, own_commission_value) = calcular_ganhos(
        weekly_earnings, fuel_cost, st.session_state.weeks_comparison)
    
    # ---
    # Seção de Resultados
    # ---

    st.header("📈 Resultados")
    
    # Métricas semanais
    st.subheader(f"Resultados Semanais")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Carro Alugado (Líquido Semanal)", 
            f"€ {rental_net_weekly:.2f}",
            delta_color="inverse" if rental_net_weekly < 0 else "normal"
        )
    
    with col2:
        st.metric(
            "Carro Próprio (Líquido Semanal)", 
            f"€ {own_net_weekly:.2f}",
            delta_color="inverse" if own_net_weekly < 0 else "normal"
        )
    
    with col3:
        st.metric(
            "Diferença Semanal", 
            f"€ {difference_weekly:.2f}",
            delta_color="inverse" if difference_weekly < 0 else "normal"
        )
    
    # Métricas totais
    st.subheader(f"Resultados no Período de {st.session_state.weeks_comparison} semanas")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Carro Alugado (Total)", 
            f"€ {rental_net_total:.2f}",
            delta_color="inverse" if rental_net_total < 0 else "normal"
        )
    
    with col2:
        st.metric(
            "Carro Próprio (Total)", 
            f"€ {own_net_total:.2f}",
            delta_color="inverse" if own_net_total < 0 else "normal"
        )
    
    with col3:
        st.metric(
            "Diferença Total", 
            f"€ {difference_total:.2f}",
            delta_color="inverse" if difference_total < 0 else "normal"
        )
    
    # Detalhamento dos cálculos
    st.subheader("Detalhamento dos Cálculos (Semanal)")
    
    comparison_data = {
        "Descrição": [
            "Ganhos Semanais",
            f"Comissão ({st.session_state.rental_commission}%)",
            "Custo do Aluguel",
            "Seguro",
            "Manutenção",
            "Custo com Combustível",
            "Total Líquido"
        ],
        "Carro Alugado (€)": [
            weekly_earnings,
            -rental_commission_value,
            -st.session_state.rental_cost,
            0,
            0,
            -fuel_cost,
            rental_net_weekly
        ],
        "Carro Próprio (€)": [
            weekly_earnings,
            -own_commission_value,
            0,
            -st.session_state.own_insurance,
            -st.session_state.own_maintenance,
            -fuel_cost,
            own_net_weekly
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Recomendação
    st.subheader("Recomendação")
    if difference_weekly > 0.01:
        st.success(f"✅ O carro alugado é mais vantajoso por € {difference_weekly:.2f} por semana.")
        st.info(f"💰 Em {st.session_state.weeks_comparison} semanas, você economizaria € {difference_total:.2f} com carro alugado.")
    elif difference_weekly < -0.01:
        st.success(f"✅ O carro próprio é mais vantajoso por € {abs(difference_weekly):.2f} por semana.")
        st.info(f"💰 Em {st.session_state.weeks_comparison} semanas, você economizaria € {abs(difference_total):.2f} com carro próprio.")
    else:
        st.info("ℹ️ Ambas as opções têm o mesmo resultado financeiro.")
    
    # Visualização gráfica
    st.subheader("Comparação Visual")
    
    # Gráfico de comparação semanal
    weekly_data = pd.DataFrame({
        "Opção": ["Carro Alugado", "Carro Próprio"],
        "Lucro Líquido (€)": [rental_net_weekly, own_net_weekly]
    })
    
    fig_weekly = px.bar(weekly_data, x="Opção", y="Lucro Líquido (€)", 
                        title="Comparação Semanal de Lucro Líquido",
                        color="Opção")
    st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Gráfico de comparação total
    total_data = pd.DataFrame({
        "Opção": ["Carro Alugado", "Carro Próprio"],
        "Lucro Líquido (€)": [rental_net_total, own_net_total]
    })
    
    fig_total = px.bar(total_data, x="Opção", y="Lucro Líquido (€)", 
                       title=f"Comparação Total de Lucro Líquido ({st.session_state.weeks_comparison} semanas)",
                       color="Opção")
    st.plotly_chart(fig_total, use_container_width=True)

# ---
# Informações Adicionais e Rodapé
# ---

with st.expander("💡 Dicas e Informações"):
    st.markdown("""
    - **Ganhos Semanais**: Valor total que você recebe pelos serviços de TVDE em uma semana.
    - **Custo com Combustível**: Gasto semanal estimado com abastecimento.
    - **Comissão**: Percentual que a plataforma retém pelos serviços.
    - **Custo do Aluguel**: Valor semanal pelo aluguel do veículo (se aplicável).
    - **Seguro**: Custo semanal do seguro do veículo próprio.
    - **Manutenção**: Custo semanal estimado com manutenção do veículo próprio.
                
    ⚠️ Lembre-se de considerar outros custos não incluídos aqui, como:
    - Lavagens e limpeza
    - Estacionamento e portagens
    - Desvalorização do veículo (no caso de carro próprio)
    - Impostos e taxas
    - Custos de aquisição do veículo próprio (precisa ser diluído ao longo do tempo)
    """)

st.markdown("---")
st.caption("Desenvolvido para ajudar motoristas TVDE a tomar decisões financeiras informadas.")
