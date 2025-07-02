# app.py (Visualizador de Distribución Normal con formato estándar)

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Explorador de Distribución",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles (Formato Consistente) ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 3:")
    st.header("Medidas de Dispersión")
    st.subheader("3.2 Desviación Estándar")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("Parámetros de la Distribución")
    
    # Slider para la Media
    media_seleccionada = st.slider(
        "Elige la Media (μ):",
        min_value=20.0,
        max_value=80.0,
        value=50.0,  # Valor inicial
        step=1.0
    )
    
    # Slider para la Desviación Estándar
    de_seleccionada = st.slider(
        "Elige la Desviación Estándar (σ):",
        min_value=5.0,
        max_value=20.0,
        value=10.0,  # Valor inicial
        step=0.5
    )
    
    st.info(
        "Mueve los sliders para ver cómo cambian el centro (media) y la dispersión "
        "(desviación estándar) de la distribución."
    )

# --- 3. Panel Principal ---
st.title("🔔 Explorador Interactivo de la Distribución Normal")
st.write(
    "Esta herramienta te permite generar datos que siguen una distribución normal "
    "y visualizar cómo la media y la desviación estándar afectan su forma."
)
st.markdown("---")

# --- 4. Generación de Datos y Gráfico ---

st.header("Visualización de la Distribución")

# Generar datos aleatorios basados en los sliders
np.random.seed(42)
datos_generados = np.random.normal(
    loc=media_seleccionada,
    scale=de_seleccionada,
    size=1000
)

# Crear el gráfico
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(datos_generados, bins=30, kde=True, color='dodgerblue', edgecolor='black', ax=ax)

# Añadir las líneas verticales
ax.axvline(media_seleccionada, color='red', linestyle='dashed', linewidth=2.5, label=f'Media = {media_seleccionada:.2f}')
ax.axvline(media_seleccionada + de_seleccionada, color='green', linestyle='dotted', linewidth=2, label=f'±1 DE ({de_seleccionada:.2f})')
ax.axvline(media_seleccionada - de_seleccionada, color='green', linestyle='dotted', linewidth=2)

# Personalización del Gráfico
ax.set_title("Histograma de Datos Generados", fontsize=16)
ax.set_xlabel("Valores", fontsize=12)
ax.set_ylabel("Frecuencia", fontsize=12)
ax.set_xlim(0, 100) # Mantener el eje X fijo
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Mostrar el gráfico en Streamlit
st.pyplot(fig)

# Mostrar un resumen
st.subheader("Parámetros Actuales")
col1, col2 = st.columns(2)
col1.metric("Media Seleccionada (μ)", f"{media_seleccionada:.2f}")
col2.metric("DE Seleccionada (σ)", f"{de_seleccionada:.2f}")
