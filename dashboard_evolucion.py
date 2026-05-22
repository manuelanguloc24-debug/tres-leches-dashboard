import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILO CORPORATIVO (DARK MODE CORPORATIVO)
st.set_page_config(page_title="Financial Operations Control", page_icon="📊", layout="wide")

# Estilos ejecutivos limpios sin elementos infantiles
st.markdown("""
    <style>
    .main {background-color: #0B0F19; color: #E2E8F0;}
    .stMetric {
        background-color: #111827; 
        padding: 22px; 
        border-radius: 6px; 
        border: 1px solid #1F2937;
    }
    div[data-testid='stMetricValue'] {color: #0EA5E9; font-family: 'Courier New', monospace; font-weight: 700; font-size: 28px;}
    div[data-testid='stMetricLabel'] {color: #9CA3AF; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;}
    h1, h2, h3 {font-family: 'Arial', sans-serif; font-weight: 700; color: #F3F4F6;}
    .stDataFrame {border: 1px solid #1F2937; border-radius: 6px;}
    </style>
""", unsafe_allow_html=True)

# 2. ENCABEZADO DE ALTA DIRECCIÓN
st.title("📊 OPERATIONAL REVENUE & CASH AUDIT")
st.caption("Business Intelligence Unit | Análisis de Rendimiento Financiero Consolidado")
st.markdown("---")

# Cargar base de datos histórica
try:
    df = pd.read_csv('mayo_real.csv')
except:
    st.error("Error de enlace: El archivo 'mayo_real.csv' no fue localizado en la raíz.")
    st.stop()

# 3. CONTROL LATERAL MINIMALISTA
st.sidebar.markdown("### 🏢 PARÁMETROS FISCALES")
mes_seleccionado = st.sidebar.selectbox("Periodo de Auditoría:", ["Todos los Meses", "abril", "mayo", "marzo"])

if mes_seleccionado != "Todos los Meses":
    df_filtrado = df[df['Mes'] == mes_seleccionado]
else:
    df_filtrado = df

# Cálculos de KPI de alto impacto
ingresos = df_filtrado[df_filtrado['Tipo'] == 'Ingreso']['Monto'].sum()
egresos = df_filtrado[df_filtrado['Tipo'] == 'Egreso']['Monto'].sum()
ganancia_neta = ingresos - egresos
margen = (ganancia_neta / ingresos) * 100 if ingresos > 0 else 0

# 4. MATRIZ DE CUADRO DE MANDO (KPIs Estilizados)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Ingresos Consolidados (Revenue)", value=f"${ingresos:,.2f}")
with col2:
    st.metric(label="Costos de Operación (OpEx)", value=f"-${egresos:,.2f}")
with col3:
    st.metric(label="Flujo de Caja Neto (Net Income)", value=f"${ganancia_neta:,.2f}")
with col4:
    st.metric(label="Margen Operativo de Caja", value=f"{margen:.1f}%")

st.markdown("<br>", unsafe_allow_html=True)

# 5. MATRIZ DE ANÁLISIS GRÁFICO PROFESIONAL
col_izq, col_der = st.columns(2)

with col_izq:
    st.markdown("### 📅 Margen de Contribución Mensual")
    st.caption("Balance macro de ingresos vs egresos por mes registrado.")
    
    resumen_mensual = df.groupby(['Mes', 'Tipo'])['Monto'].sum().unstack().fillna(0)
    
    # Gráfico sobrio con fondo acoplado al modo oscuro
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fig.patch.set_facecolor('#0B0F19')
    ax.set_facecolor('#111827')
    
    # Paleta seria: Gris acero y Azul corporativo oscuro
    resumen_mensual.plot(x=resumen_mensual.index, kind='bar', color=['#4B5563', '#0284C7'], ax=ax, width=0.35)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#374151')
    ax.spines['bottom'].set_color('#374151')
    ax.tick_params(colors='#9CA3AF', labelsize=10)
    ax.yaxis.grid(True, linestyle='--', alpha=0.05, color='#FFFFFF')
    ax.legend(['Egresos (OpEx)', 'Ingresos (Revenue)'], facecolor='#111827', edgecolor='#1F2937', labelcolor='#F3F4F6')
    
    st.pyplot(fig)

with col_der:
    st.markdown("### 🍕 Desglose Porcentual del Gasto")
    st.caption("Distribución de egresos según su categoría en el periodo analizado.")
    
    df_egresos = df_filtrado[df_filtrado['Tipo'] == 'Egreso']
    if not df_egresos.empty:
        resumen_gastos = df_egresos.groupby('Categoria')['Monto'].sum().reset_index()
        
        fig2, ax2 = plt.subplots(figsize=(6, 4.5))
        fig2.patch.set_facecolor('#0B0F19')
        ax2.set_facecolor('#111827')
        
        # Paleta ejecutiva en escala de azules y grises oscuros
        colors = ['#0EA5E9', '#0284C7', '#1E40AF', '#374151', '#4B5563']
        
        wedges, texts, autotexts = ax2.pie(
            resumen_gastos['Monto'], 
            labels=resumen_gastos['Categoria'], 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors,
            textprops=dict(color='#F3F4F6', size=10)
        )
        for autotext in autotexts:
            autotext.set_color('#0B0F19')
            autotext.set_weight('bold')
            
        st.pyplot(fig2)
    else:
        st.info("No existen registros de egresos para el corte seleccionado.")

st.markdown("---")

# 6. LIBRO MAYOR EJECUTIVO
st.markdown("### 📋 Libro Mayor y Transacciones Auditadas")
st.dataframe(df_filtrado, use_container_width=True)