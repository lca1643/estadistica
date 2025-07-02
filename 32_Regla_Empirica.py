# app.py (versión para Regla Empírica)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Análisis de Dispersión",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 3:")
    st.header("Medidas de Dispersión")
    st.subheader("3.3 Regla Empírica")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna = None
    color = '#6495ED' # Color "Cornflower Blue"

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        st.header("2. Seleccionar Variable y Opciones")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if not numeric_cols:
            st.error("El archivo no contiene columnas numéricas."); st.stop()
        
        columna = st.selectbox("Elige la columna a analizar:", options=numeric_cols)
        color = st.color_picker("Elige un color para el histograma:", value='#6495ED')

# --- 3. Panel Principal ---
st.title("🔔 Visualizador de la Regla Empírica (68-95-99.7)")
st.write(
    "Esta herramienta analiza si tus datos siguen una distribución normal, mostrando "
    "la media y los porcentajes de datos dentro de 1, 2 y 3 desviaciones estándar."
)

if uploaded_file is None:
    st.warning("Por favor, sube un archivo para comenzar."); st.stop()

if df is None or columna is None or columna not in df.columns:
    st.info("Por favor, selecciona una columna en el panel de la izquierda."); st.stop()

# --- 4. Lógica de Cálculo y Visualización ---
st.markdown("---")
st.header(f"Análisis de la columna: '{columna}'")

datos = df[columna].dropna()

if datos.empty or not pd.api.types.is_numeric_dtype(datos):
    st.warning("La columna seleccionada no tiene datos numéricos válidos.")
else:
    # --- Cálculo de Estadísticas ---
    media = datos.mean()
    desviacion_estandar = datos.std() # Desviación estándar muestral
    total_datos = len(datos)
    
    # Calcular rangos
    rango_1_min, rango_1_max = media - desviacion_estandar, media + desviacion_estandar
    rango_2_min, rango_2_max = media - 2 * desviacion_estandar, media + 2 * desviacion_estandar
    rango_3_min, rango_3_max = media - 3 * desviacion_estandar, media + 3 * desviacion_estandar
    
    # Calcular porcentajes reales de datos dentro de cada rango
    porc_1_de = datos.between(rango_1_min, rango_1_max).mean() * 100
    porc_2_de = datos.between(rango_2_min, rango_2_max).mean() * 100
    porc_3_de = datos.between(rango_3_min, rango_3_max).mean() * 100
    
    # --- Mostrar las métricas ---
    st.subheader("Resultados del Análisis")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Media", value=f"{media:.2f}")
    with col2:
        st.metric(label="Desviación Estándar (DE)", value=f"{desviacion_estandar:.2f}")

    # Mostrar comparación con la regla empírica
    st.write("**Comparación con la Regla Empírica:**")
    st.markdown(f"- **Dentro de ±1 DE:** `{porc_1_de:.1f}%` de los datos (la regla predice ~68%)")
    st.markdown(f"- **Dentro de ±2 DE:** `{porc_2_de:.1f}%` de los datos (la regla predice ~95%)")
    st.markdown(f"- **Dentro de ±3 DE:** `{porc_3_de:.1f}%` de los datos (la regla predice ~99.7%)")

    # --- Visualización en Pestañas ---
    tab_grafico, tab_datos = st.tabs(["📈 Histograma", "📄 Estadísticas Detalladas"])

    with tab_grafico:
        st.subheader("Histograma con Media y Desviaciones Estándar")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        # Usamos Seaborn para añadir la curva de densidad (KDE) fácilmente
        sns.histplot(datos, bins='auto', kde=True, color=color, edgecolor='black', ax=ax)
        
        # --- Añadir las líneas verticales ---
        ax.axvline(media, color='red', linestyle='dashed', linewidth=2, label=f'Media = {media:.2f}')
        ax.axvline(rango_1_min, color='orange', linestyle='dotted', linewidth=2, label=f'±1 DE ({desviacion_estandar:.2f})')
        ax.axvline(rango_1_max, color='orange', linestyle='dotted', linewidth=2)
        ax.axvline(rango_2_min, color='green', linestyle='dotted', linewidth=2, label=f'±2 DE')
        ax.axvline(rango_2_max, color='green', linestyle='dotted', linewidth=2)
        
        ax.set_title(f'Distribución de {columna}')
        ax.set_xlabel(columna)
        ax.set_ylabel('Frecuencia')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        
        # --- Botón de descarga ---
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        st.download_button(
            label="📥 Descargar Gráfico",
            data=buf,
            file_name=f"histograma_regla_empirica_{columna}.png",
            mime="image/png"
        )
        st.pyplot(fig)

    with tab_datos:
        st.subheader("Resumen Estadístico Completo")
        stats_csv = datos.describe().to_csv().encode('utf-8')
        st.download_button("📥 Descargar Estadísticas (CSV)", data=stats_csv, file_name=f"estadisticas_{columna}.csv", mime="text/csv")
        st.dataframe(datos.describe())