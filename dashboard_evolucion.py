import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from datetime import datetime

# 1. CONFIGURACIÓN CORPORATIVA DE LA PLATAFORMA
st.set_page_config(page_title="Financial Operations Control", page_icon="📊", layout="wide")

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
    .stButton>button {width: 100%; background-color: #0EA5E9; color: white; border-radius: 6px; font-weight: bold; padding: 10px;}
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 📝 RECUERDA COLOCAR AQUÍ TUS ENLACES DE GOOGLE
URL_LECTURA = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSimxnt_gsoXZfo_S9ipfP_KZ7751EFyr4o4cLy__3l3dDZ8fxINQjr8H74lEysJ4MhELpXnvSD6R-C/pub?output=csv'
URL_ESCRITURA = 'https://script.google.com/macros/s/AKfycbxcEgb32zXqPECs3i9AHqBAr5vyCEP2yjDlShGX0g354C_HSdIAblgRU8WiTX2tL9EB/exec'
# =========================================================

# CREACIÓN DE PESTAÑAS (TABS) INTERACTIVAS
tab1, tab2 = st.tabs(["📈 CONTROL DE MANDO VISUAL", "📝 REGISTRAR COMPRA / GASTO"])

with tab1:
    st.title("📊 OPERATIONAL REVENUE & CASH AUDIT")
    st.caption("Business Intelligence Unit | Análisis de Volumen y Rendimiento en Tiempo Real")
    st.markdown("---")

    try:
        # Leer la hoja limpia
        df = pd.read_csv(URL_LECTURA)
        
        # Normalizar columnas por seguridad
        df.columns = df.columns.str.strip().str.lower()
        
        if not df.empty and 'fecha' in df.columns and 'monto' in df.columns:
            df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
            
            # Mapeo de meses inteligente
            meses_es = {1: 'enero', 2: 'febrero', 3: 'marzo', 4: 'abril', 5: 'mayo', 6: 'junio',
                        7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
            df['mes'] = df['fecha'].dt.month.map(meses_es).fillna('desconocido')
            df['monto'] = pd.to_numeric(df['monto'], errors='coerce').fillna(0.0)
            
            # Asegurar que la columna cantidad sea numérica
            if 'cantidad' in df.columns:
                df['cantidad'] = pd.to_numeric(df['cantidad'], errors='coerce').fillna(0)
            else:
                df['cantidad'] = 0
            
            # Filtro por mes
            lista_meses = [m for m in df['mes'].unique() if m != 'desconocido']
            mes_seleccionado = st.sidebar.selectbox("Periodo de Auditoría:", ["Todos los Meses"] + lista_meses)
            
            df_filtrado = df[df['mes'] == mes_seleccionado] if mes_seleccionado != "Todos los Meses" else df[df['mes'] != 'desconocido']
            
            # KPIs Financieros
            ingresos = df_filtrado[df_filtrado['tipo'] == 'Ingreso']['monto'].sum()
            egresos = df_filtrado[df_filtrado['tipo'] == 'Egreso']['monto'].sum()
            ganancia_neta = ingresos - egresos
            margen = (ganancia_neta / ingresos) * 100 if ingresos > 0 else 0
            
            # Suma del volumen total de postres vendidos (solo filas de Ingreso)
            total_pasteles = int(df_filtrado[df_filtrado['tipo'] == 'Ingreso']['cantidad'].sum())
            
            # Despliegue de métricas en 5 columnas ejecutivas
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Ingresos (Revenue)", f"${ingresos:,.2f}")
            col2.metric("Costos (OpEx)", f"-${egresos:,.2f}")
            col3.metric("Net Income", f"${ganancia_neta:,.2f}")
            col4.metric("Margen de Caja", f"{margen:.1f}%")
            col5.metric("Postres Vendidos", f"{total_pasteles} uds")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Gráficos e Historial
            col_izq, col_der = st.columns(2)
            with col_izq:
                st.markdown("### 📅 Margen de Contribución Mensual")
                resumen_mensual = df[df['mes'] != 'desconocido'].groupby(['mes', 'tipo'])['monto'].sum().unstack().fillna(0)
                if 'Egreso' not in resumen_mensual.columns: resumen_mensual['Egreso'] = 0.0
                if 'Ingreso' not in resumen_mensual.columns: resumen_mensual['Ingreso'] = 0.0
                
                fig, ax = plt.subplots(figsize=(7, 4.5))
                fig.patch.set_facecolor('#0B0F19')
                ax.set_facecolor('#111827')
                resumen_mensual.plot(kind='bar', color=['#4B5563', '#0284C7'], ax=ax, width=0.35)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.tick_params(colors='#9CA3AF', labelsize=10)
                plt.xticks(rotation=0)
                st.pyplot(fig)
                
            with col_der:
                st.markdown("### 🍕 Desglose del Gasto")
                df_egresos = df_filtrado[(df_filtrado['tipo'] == 'Egreso') & (df_filtrado['monto'] > 0)]
                if not df_egresos.empty:
                    resumen_gastos = df_egresos.groupby('categoria')['monto'].sum()
                    fig2, ax2 = plt.subplots(figsize=(6, 4.5))
                    fig2.patch.set_facecolor('#0B0F19')
                    ax2.pie(resumen_gastos, labels=resumen_gastos.index, autopct='%1.1f%%', startangle=140, textprops=dict(color='#F3F4F6'))
                    st.pyplot(fig2)
                else:
                    st.info("Sin gastos operativos en este periodo.")
                    
            st.markdown("---")
            st.markdown("### 📋 Libro Mayor en Tiempo Real")
            st.dataframe(df_filtrado.sort_values(by='fecha', ascending=False), use_container_width=True)
        else:
            st.info("La base de datos de Google Sheets está vacía. Agrega tu primer registro en la pestaña contigua.")
    except Exception as e:
        st.error(f"Esperando conexión con Google Sheets... {e}")

with tab2:
    st.title("📝 CONSOLA DE REGISTRO DIRECTO")
    st.write("Introduce una nueva transacción. Los cambios impactarán directamente en la Google Sheet en la nube.")
    st.markdown("---")
    
    with st.form("formulario_dashboard", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            ins_fecha = st.date_input("Fecha del Movimiento", datetime.now())
            ins_tipo = st.selectbox("Tipo de Operación", ["Ingreso", "Egreso"])
            ins_monto = st.number_input("Monto en Dólares ($)", min_value=0.0, format="%.2f")
        with col_form2:
            ins_cat = st.selectbox("Categoría Fiscal", ["Pago", "Gastos", "Deudas", "Servicios", "Mano de Obra"])
            ins_cant = st.number_input("Cantidad de Unidades (Volumen)", min_value=1, step=1, value=1)
            ins_det = st.text_input("Detalle descriptivo (ej: Venta 30 moldes, Pago de luz)")
            
        st.markdown("<br>", unsafe_allow_html=True)
        btn_registrar = st.form_submit_button("🚀 GUARDAR EN GOOGLE SHEETS")
        
        if btn_registrar:
            if ins_det == "" or ins_monto == 0:
                st.warning("El detalle y el monto no pueden guardarse vacíos.")
            else:
                # Si es un gasto (egreso), las unidades vendidas se marcan en 0 por defecto
                valor_cantidad = ins_cant if ins_tipo == "Ingreso" else 0
                
                # Paquete ordenado hacia Google Sheets
                datos_envio = {
                    "fecha": ins_fecha.strftime("%Y-%m-%d"),
                    "tipo": ins_tipo,
                    "categoria": ins_cat,
                    "detalle": ins_det,
                    "cantidad": valor_cantidad,
                    "monto": ins_monto
                }
                try:
                    peticion = requests.post(URL_ESCRITURA, data=json.dumps(datos_envio))
                    if peticion.status_code == 200:
                        st.success(f"✅ ¡Éxito! Registrado: {ins_det} por ${ins_monto:.2f}.")
                        st.balloons()
                    else:
                        st.error("La base de datos rechazó la escritura. Verifica los permisos de Apps Script.")
                except:
                    st.error("Error de enlace. Verifica tu conexión a internet.")