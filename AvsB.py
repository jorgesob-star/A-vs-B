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
# Isso garante que os valores estejam sempre disponíveis, mesmo quando ocultos
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

# ---
# Seção de Cálculos
# ---

# Função para realizar os cálculos (boa prática para organização)
def calcular_ganhos(weekly_earnings, fuel_cost):
    # Calcular para carro alugado
    rental_commission_value = weekly_earnings * (st.session_state.rental_commission / 100)
    rental_net = weekly_earnings - rental_commission_value - st.session_state.rental_cost - fuel_cost
    
    # Calcular para carro próprio
    own_commission_value = weekly_earnings * (st.session_state.own_commission / 100)
    own_net = weekly_earnings - own_commission_value - st.session_state.own_insurance - st.session_state.own_maintenance - fuel_cost
    
    difference = rental_net - own_net
    
    return rental_net, own_net, difference, rental_commission_value, own_commission_value

# Botão de cálculo
if st.button("Calcular", type="primary"):
    rental_net, own_net, difference, rental_commission_value, own_commission_value = calcular_ganhos(weekly_earnings, fuel_cost)
    
    # ---
    # Seção de Resultados
    # ---

    st.header("📈 Resultados")
    
    # Métricas
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
    
    # Detalhamento dos cálculos
    st.subheader("Detalhamento dos Cálculos")
    
    comparison_data = {
        "Descrição": [
            "Ganhos Semanais",
            f"Comissão ({st.session_state.rental_commission}%)",
            "Custo do Aluguel",
            "Manutenção",
            "Custo com Combustível",
            "Total Líquido"
        ],
        "Carro Alugado (€)": [
            weekly_earnings,
            -rental_commission_value,
            -st.session_state.rental_cost,
            0,
            -fuel_cost,
            rental_net
        ],
        "Carro Próprio (€)": [
            weekly_earnings,
            -own_commission_value,
            -st.session_state.own_insurance,
            -st.session_state.own_maintenance,
            -fuel_cost,
            own_net
        ]
    }
    
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
    
    chart_data = pd.DataFrame({
        "Opção": ["Carro Alugado", "Carro Próprio"],
        "Lucro Líquido (€)": [rental_net, own_net]
    })
    
    st.bar_chart(chart_data, x="Opção", y="Lucro Líquido (€)")

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
    """)

st.markdown("---")
st.caption("Desenvolvido para ajudar motoristas TVDE a tomar decisões financeiras informadas.")

