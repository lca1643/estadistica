import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from scipy.stats import linregress

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Análisis de Regresión Lineal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 4:")
    st.header("Regresión y Correlación")
    st.subheader("4.2 Regresión Lineal Simple")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna_x = None
    columna_y = None

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.header("2. Seleccionar Variables")
        
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        
        if len(numeric_cols) < 2:
            st.error("El archivo CSV debe contener al menos dos columnas numéricas."); st.stop()
        
        columna_x = st.selectbox("Elige la Variable Independiente (Eje X):", options=numeric_cols, index=0)
        
        opciones_y = [col for col in numeric_cols if col != columna_x]
        columna_y = st.selectbox("Elige la Variable Dependiente (Eje Y):", options=opciones_y, index=0)

# --- 3. Panel Principal ---
st.title("📈 Regresión Lineal Simple")
st.write(
    "Esta aplicación realiza un análisis de regresión lineal simple entre dos variables numéricas. "
    "Calcula la línea que mejor se ajusta a los datos, evalúa la calidad del ajuste con R² y permite hacer predicciones."
)

if uploaded_file is None:
    st.warning("Por favor, sube un archivo CSV para comenzar."); st.stop()

if df is None or columna_x is None or columna_y is None:
    st.info("Asegúrate de haber seleccionado dos variables numéricas en el panel de la izquierda."); st.stop()

# --- 4. Lógica de Cálculo y Visualización ---
st.markdown("---")
st.header(f"Análisis de Regresión: '{columna_y}' (Y) vs. '{columna_x}' (X)")

try:
    datos_limpios = df[[columna_x, columna_y]].dropna()
    x_data = datos_limpios[columna_x]
    y_data = datos_limpios[columna_y]

    if x_data.empty or y_data.empty:
        st.error("No hay suficientes datos válidos en las columnas seleccionadas después de eliminar valores faltantes."); st.stop()

    slope, intercept, r_value, p_value, std_err = linregress(x_data, y_data)
    r_squared = r_value**2

    st.subheader("Resultados del Modelo de Regresión")
    col1, col2, col3 = st.columns(3)
    col1.metric("Pendiente (b₁)", f"{slope:.4f}")
    col2.metric("Intercepto (b₀)", f"{intercept:.4f}")
    col3.metric("Coeficiente de Determinación (R²)", f"{r_squared:.4f}")

    st.markdown("##### Ecuación de la Recta de Regresión:")
    st.latex(f"Y = {intercept:.4f} + ({slope:.4f}) \\times X")
    
    st.subheader("Realizar una Predicción")
    min_val, max_val = float(x_data.min()), float(x_data.max())
    
    valor_prediccion_x = st.slider(f"Selecciona un valor para '{columna_x}' para predecir '{columna_y}':", 
                                   min_value=min_val, max_value=max_val, value=(min_val + max_val) / 2)
    
    prediccion_y = intercept + slope * valor_prediccion_x
    st.success(f"Para un valor de **{columna_x} = {valor_prediccion_x:.2f}**, el valor predicho de **{columna_y}** es **{prediccion_y:.2f}**")

    st.subheader("Gráfico de Dispersión y Línea de Regresión")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x=x_data, y=y_data, s=80, label='Datos Observados', ax=ax)
    ax.plot(x_data, intercept + slope * x_data, color='red', linewidth=2, label=f'Línea de Regresión (R² = {r_squared:.3f})')
    ax.scatter(valor_prediccion_x, prediccion_y, color='green', marker='o', s=150, zorder=5, 
               label=f'Predicción para X={valor_prediccion_x:.2f}')
    
    ax.set_title(f"Relación entre {columna_x} y {columna_y}", fontsize=16, fontweight='bold')
    ax.set_xlabel(columna_x, fontsize=12)
    ax.set_ylabel(columna_y, fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig)

    # --- NUEVA SECCIÓN: Botón de descarga ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button(
        label="📥 Descargar Gráfico",
        data=buf,
        file_name=f"regresion_{columna_y}_vs_{columna_x}.png",
        mime="image/png"
    )
    
    with st.expander("Ver Interpretación Detallada de los Resultados"):
        st.markdown(f"**Pendiente ({slope:.4f}):** Por cada unidad que aumenta **{columna_x}**, se estima que **{columna_y}** {'aumenta' if slope > 0 else 'disminuye'} en un promedio de **{abs(slope):.4f}** unidades.")
        st.markdown(f"**Intercepto ({intercept:.4f}):** Cuando **{columna_x}** es igual a 0, el valor estimado de **{columna_y}** es **{intercept:.4f}**. (Esta interpretación es útil solo si X=0 tiene sentido en el contexto de tus datos).")
        st.markdown(f"**Coeficiente de Determinación R² ({r_squared:.4f}):** El **{r_squared*100:.2f}%** de la variabilidad en **{columna_y}** puede ser explicada por la variación en **{columna_x}** a través de este modelo lineal. Un valor más cercano a 1 indica un mejor ajuste del modelo a los datos.")
        st.markdown(f"**Valor p ({p_value:.4f}):** Este valor indica la significancia estadística de la relación. Un p-valor bajo (típicamente < 0.05) sugiere que la relación observada no se debe al azar.")

except Exception as e:
    st.error(f"Ocurrió un error al procesar los datos: {e}")
    st.warning("Verifica que el archivo CSV esté bien formado y que las columnas seleccionadas sean numéricas y no tengan errores.")
