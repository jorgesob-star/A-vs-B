import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Comparador TVDE", page_icon="🚗", layout="centered")

st.title("🚗 Comparador de Ganhos TVDE")
st.markdown("Veja rapidamente qual opção é mais vantajosa, mesmo no celular.")

# --- Entrada de Dados ---
weekly_earnings = st.number_input("Ganhos Semanais (€):", min_value=0.0, value=800.0, step=50.0)
fuel_cost = st.number_input("Custo Combustível (€):", min_value=0.0, value=200.0, step=10.0)
other_costs = st.number_input("Outros Custos (€):", min_value=0.0, value=0.0, step=5.0)

st.markdown("### ⚙️ Parâmetros Avançados")
rental_cost = st.number_input("Custo Aluguel (€/semana):", value=280.0)
rental_commission = st.number_input("Comissão Alugado (%):", value=7.0)
own_insurance = st.number_input("Seguro Próprio (€):", value=45.0)
own_maintenance = st.number_input("Manutenção Próprio (€):", value=50.0)
own_commission = st.number_input("Comissão Próprio (%):", value=12.0)

# --- Cálculos ---
def calcular_ganhos(weekly, fuel, other, rental_cost, rental_comm, own_ins, own_maint, own_comm):
    rental_comm_val = weekly * rental_comm / 100
    rental_net = weekly - rental_comm_val - rental_cost - fuel - other

    own_comm_val = weekly * own_comm / 100
    own_net = weekly - own_comm_val - own_ins - own_maint - fuel - other

    diff = rental_net - own_net
    return rental_net, own_net, diff, rental_comm_val, own_comm_val

rental_net, own_net, diff, rental_comm_val, own_comm_val = calcular_ganhos(
    weekly_earnings, fuel_cost, other_costs, rental_cost, rental_commission, own_insurance, own_maintenance, own_commission
)

# --- Resultados ---
st.subheader("📈 Lucro Líquido")
st.metric("Alugado (€)", f"{rental_net:.2f}", delta=f"{rental_net-own_net:.2f}")
st.metric("Próprio (€)", f"{own_net:.2f}", delta=f"{own_net-rental_net:.2f}")
st.metric("Diferença Anual (€)", f"{diff*52:.2f}")

# Tabela detalhada compacta
df = pd.DataFrame({
    "Descrição": ["Ganhos","Comissão","Aluguel","Seguro","Manutenção","Combustível","Outros","Líquido"],
    "Alugado (€)": [f"{weekly_earnings:.2f}", f"-{rental_comm_val:.2f}", f"-{rental_cost:.2f}", "0.00","0.00", f"-{fuel_cost:.2f}", f"-{other_costs:.2f}", f"{rental_net:.2f}"],
    "Próprio (€)": [f"{weekly_earnings:.2f}", f"-{own_comm_val:.2f}", "0.00", f"-{own_insurance:.2f}", f"-{own_maintenance:.2f}", f"-{fuel_cost:.2f}", f"-{other_costs:.2f}", f"{own_net:.2f}"]
})
st.dataframe(df, use_container_width=True, hide_index=True)

# Download CSV
st.download_button("📥 Baixar CSV", df.to_csv(index=False), file_name="resultados_tvde.csv", mime="text/csv")

# Recomendação compacta
st.subheader("✅ Recomendação")
if diff > 0.01:
    st.success(f"Alugado mais vantajoso: € {diff:.2f}/semana")
elif diff < -0.01:
    st.success(f"Próprio mais vantajoso: € {abs(diff):.2f}/semana")
else:
    st.info("Resultado financeiro similar.")

# Gráfico simples e compacto
st.subheader("📊 Comparação Visual")
chart_data = pd.DataFrame({"Lucro (€)":[rental_net, own_net]}, index=["Alugado","Próprio"])
st.bar_chart(chart_data)

# Dicas rápidas
st.markdown("""
**💡 Dicas rápidas**
- Ganhos: total recebido.
- Combustível: gasto semanal.
- Outros: lavagem, estacionamento, portagens.
- Comissão: percentual plataforma.
- Seguro/Manutenção: custos do próprio.
⚠️ Fatores não incluídos: desvalorização, impostos, custos imprevistos.
""")
