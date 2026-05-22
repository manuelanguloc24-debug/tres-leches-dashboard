import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Locura 2.0 - Business Intelligence", page_icon="📈", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🚀 CONTROL DE MANDO INTERACTIVO: TRES LECHES</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4B5563;'>Auditoría Financiera Avanzada y Evolución del Negocio</p>", unsafe_allow_html=True)
st.markdown("---")

# Cargar la base de datos histórica
df = pd.read_csv('mayo_real.csv')

# FILTRO INTERACTIVO EN LA BARRA LATERAL
st.sidebar.header("🎛️ Filtros del Negocio")
mes_seleccionado = st.sidebar.selectbox("Selecciona el mes a auditar:", ["Todos los Meses", "abril", "mayo", "marzo"])

# Filtrar los datos según lo que toque el cliente con el mouse
if mes_seleccionado != "Todos los Meses":
    df_filtrado = df[df['Mes'] == mes_seleccionado]
else:
    df_filtrado = df

# --- CÁLCULOS DINÁMICOS ---
ingresos = df_filtrado[df_filtrado['Tipo'] == 'Ingreso']['Monto'].sum()
egresos = df_filtrado[df_filtrado['Tipo'] == 'Egreso']['Monto'].sum()
ganancia_neta = ingresos - egresos
margen = (ganancia_neta / ingresos) * 100 if ingresos > 0 else 0

# TARJETAS DE CONTROL FINANCIERO
st.subheader(f"📊 Métricas Clave - Período: {mes_seleccionado.upper()}")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="💰 Facturación Bruta", value=f"${ingresos:,.2f}")
with col2:
    st.metric(label="📉 Gastos Operativos", value=f"-${egresos:,.2f}")
with col3:
    st.metric(label="🏆 GANANCIA NETA LIBRE", value=f"${ganancia_neta:,.2f}")
with col4:
    st.metric(label="📈 Rentabilidad Efectiva", value=f"{margen:.1f}%")

st.markdown("---")

# --- GRÁFICOS DE EVOLUCIÓN HISTÓRICA ---
st.subheader("🔮 Comparativa y Tendencias Financieras")
col_izq, col_der = st.columns(2)

with col_izq:
    st.write("### 📅 Ingresos vs Egresos por Mes")
    # Agrupar datos por mes y tipo
    resumen_mensual = df.groupby(['Mes', 'Tipo'])['Monto'].sum().unstack().fillna(0).reset_index()
    
    fig, ax = plt.subplots(figsize=(7, 4.5))
    resumen_mensual.plot(x='Mes', kind='bar', color=['#EF4444', '#10B981'], ax=ax)
    plt.title("Balance Mensual del Negocio")
    plt.ylabel("Dólares ($)")
    plt.xticks(rotation=0)
    st.pyplot(fig)

with col_der:
    st.write("### 🍕 Distribución de Gastos en el Período Seleccionado")
    df_egresos = df_filtrado[df_filtrado['Tipo'] == 'Egreso']
    if not df_egresos.empty:
        resumen_gastos = df_egresos.groupby('Categoria')['Monto'].sum().reset_index()
        fig2, ax2 = plt.subplots(figsize=(6, 4.5))
        ax2.pie(resumen_gastos['Monto'], labels=resumen_gastos['Categoria'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('muted'))
        st.pyplot(fig2)
    else:
        st.info("No hay gastos registrados en este período.")

st.markdown("---")
st.subheader("📋 Datos Históricos Auditados")
st.dataframe(df_filtrado, use_container_width=True)