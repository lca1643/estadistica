# app.py (versión con Box Plot y Puntos de Datos)

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Análisis de Box Plot",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 3:")
    st.header("Medidas de Dispersión")
    st.subheader("3.4 Rango Intercuartílico y Box Plots")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna = None
    color = '#A9CCE3'

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.header("2. Seleccionar Variable y Opciones")
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if not numeric_cols:
            st.error("El archivo no contiene columnas numéricas."); st.stop()
        
        columna = st.selectbox("Elige la columna para analizar:", options=numeric_cols)
        color = st.color_picker("Elige un color para la caja:", value='#A9CCE3')

# --- 3. Panel Principal ---
st.title("📦Rango Intercuartílico (IQR)")
st.write(
    "Esta herramienta visualiza la distribución de tus datos a través de sus cuartiles, "
    "identifica el rango intercuartílico y detecta valores atípicos (outliers)."
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
    # --- Cálculo de Estadísticas Clave ---
    Q1 = np.percentile(datos, 25)
    mediana = np.median(datos)
    Q3 = np.percentile(datos, 75)
    IQR = Q3 - Q1
    lim_inf = Q1 - 1.5 * IQR
    lim_sup = Q3 + 1.5 * IQR
    outliers = [x for x in datos if x < lim_inf or x > lim_sup]
    
    # --- Mostrar las métricas ---
    st.subheader("Medidas de Posición y Dispersión")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mediana (Q2)", f"{mediana:.2f}")
    col2.metric("Q1 (Percentil 25)", f"{Q1:.2f}")
    col3.metric("Q3 (Percentil 75)", f"{Q3:.2f}")
    col4.metric("Rango Intercuartílico (IQR)", f"{IQR:.2f}")
    
    with st.expander("Análisis de Valores Atípicos (Outliers)"):
        st.markdown(f"- **Límite inferior para outliers:** `{lim_inf:.2f}`")
        st.markdown(f"- **Límite superior para outliers:** `{lim_sup:.2f}`")
        if outliers:
            st.warning(f"Se encontraron **{len(outliers)}** valores atípicos: {', '.join(map(str, sorted(outliers)))}")
        else:
            st.success("No se encontraron valores atípicos en esta variable.")

    # --- Visualización ---
    st.subheader("Diagrama de Caja y Bigotes Detallado")
    
    fig, ax = plt.subplots(figsize=(12, 4))
    
    # 1. Dibujar el Boxplot. flierprops=dict(marker='') para ocultar los outliers por defecto de matplotlib
    box = ax.boxplot(datos, vert=False, patch_artist=True, widths=0.6,
                     boxprops=dict(facecolor=color, linewidth=2),
                     medianprops=dict(color='cyan', linewidth=3),
                     whiskerprops=dict(linewidth=2),
                     capprops=dict(linewidth=2),
                     flierprops=dict(marker='')) # Ocultamos los outliers automáticos

    # --- NUEVA SECCIÓN: Dibujar los puntos de datos ---
    # Usamos un 'jitter' vertical para que los puntos no se solapen perfectamente
    y_jitter = np.random.normal(1, 0.04, size=len(datos))
    
    # Separar outliers de los datos normales para colorearlos diferente
    datos_normales = [d for d in datos if d not in outliers]
    y_jitter_normales = y_jitter[:len(datos_normales)] # Asegurar misma longitud
    
    # Dibujar puntos normales en verde
    ax.scatter(datos_normales, y_jitter_normales, color='green', s=50, alpha=0.6, zorder=3, label='Datos Normales')
    # Dibujar outliers en rojo
    if outliers:
        ax.scatter(outliers, np.full(len(outliers), 1), color='blue', s=80, zorder=4, edgecolor='black', label='Outliers')

    # Anotaciones
    ax.annotate(f'Q1={Q1:.2f}', xy=(Q1, 0.7), xytext=(0, -40), textcoords='offset points', ha='center', arrowprops=dict(arrowstyle="->", color='blue'))
    ax.annotate(f'Mediana={mediana:.2f}', xy=(mediana, 0.7), xytext=(0, -30), textcoords='offset points', ha='center', arrowprops=dict(arrowstyle="->", color='blue'))
    ax.annotate(f'Q3={Q3:.2f}', xy=(Q3, 0.7), xytext=(0, -40), textcoords='offset points', ha='center', arrowprops=dict(arrowstyle="->", color='blue'))
    ax.annotate(f'IQR = {IQR:.2f}', xy=((Q1+Q3)/2, 1.4), ha='center', va='center', fontsize=12, fontweight='bold', color='darkgreen')

    # Personalización
    ax.set_title(f'Distribución de {columna}', fontsize=16, fontweight='bold')
    ax.set_xlabel('Valores', fontsize=12)
    ax.set_yticks([])
    ax.grid(axis='x', linestyle='--', alpha=0.6)
    
    # --- Botón de descarga ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button(
        label="📥 Descargar Gráfico",
        data=buf,
        file_name=f"boxplot_iqr_{columna}.png",
        mime="image/png"
    )
    
    st.pyplot(fig)
