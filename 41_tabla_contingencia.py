import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
from scipy.stats import chi2_contingency

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Prueba de Chi-Cuadrado",
    page_icon="χ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 4:")
    st.header("Análisis de Datos Categóricos")
    st.subheader("4.1 Tablas de Contingencia")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Datos")
    uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv", label_visibility="collapsed")
    
    df = None
    columna_filas = None
    columna_columnas = None
    alpha = 0.05

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.header("2. Seleccionar Variables")
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(categorical_cols) < 2:
            st.error("El archivo CSV debe contener al menos dos columnas de tipo texto/categórico."); st.stop()
        
        columna_filas = st.selectbox("Elige la variable para las FILAS:", options=categorical_cols, index=0)
        
        opciones_columnas = [col for col in categorical_cols if col != columna_filas]
        columna_columnas = st.selectbox("Elige la variable para las COLUMNAS:", options=opciones_columnas, index=1 if len(opciones_columnas) > 1 else 0)

        st.header("3. Opciones de la Prueba")
        alpha = st.slider("Nivel de Significancia (α):", min_value=0.01, max_value=0.20, value=0.05, step=0.01)

# --- 3. Panel Principal ---
st.title("Tablas de Contingencia")
st.write(
    "Esta aplicación analiza la relación entre dos variables categóricas de un archivo que tú proporciones. "
    "Construye una tabla de contingencia y realiza la prueba Chi-Cuadrado para determinar si existe una asociación estadísticamente significativa entre ellas."
)

if uploaded_file is None:
    st.warning("Por favor, sube un archivo CSV para comenzar."); st.stop()

if df is None or columna_filas is None or columna_columnas is None:
    st.info("Asegúrate de haber seleccionado dos variables categóricas en el panel de la izquierda."); st.stop()

# --- 4. Lógica de Cálculo y Visualización ---
st.markdown("---")
st.header(f"Análisis de Asociación: '{columna_filas}' vs. '{columna_columnas}'")

try:
    contingency_table = pd.crosstab(df[columna_filas], df[columna_columnas])
    
    st.subheader("Tabla de Contingencia (Frecuencias Observadas)")
    st.dataframe(contingency_table)

    # --- NUEVA SECCIÓN: Tablas Porcentuales ---
    with st.expander("Ver Tablas de Contingencia con Porcentajes"):
        st.write("Estas tablas ayudan a interpretar las relaciones independientemente del tamaño de las muestras.")
        
        # Porcentaje por Fila
        st.markdown("**Porcentajes por Fila** (cada fila suma 100%)")
        contingency_pct_row = pd.crosstab(df[columna_filas], df[columna_columnas], normalize='index')
        st.dataframe(contingency_pct_row.style.format("{:.2%}"))

        # Porcentaje por Columna
        st.markdown("**Porcentajes por Columna** (cada columna suma 100%)")
        contingency_pct_col = pd.crosstab(df[columna_filas], df[columna_columnas], normalize='columns')
        st.dataframe(contingency_pct_col.style.format("{:.2%}"))
        
        # Porcentaje sobre el Total
        st.markdown("**Porcentajes sobre el Total General** (la tabla entera suma 100%)")
        contingency_pct_total = pd.crosstab(df[columna_filas], df[columna_columnas], normalize='all')
        st.dataframe(contingency_pct_total.style.format("{:.2%}"))
    
    # --- Aplicar la Prueba Chi-Cuadrado ---
    chi2, p_value, dof, expected_freq = chi2_contingency(contingency_table)

    st.subheader("Resultados de la Prueba Chi-Cuadrado")
    col1, col2, col3 = st.columns(3)
    col1.metric("Estadístico Chi-Cuadrado (χ²)", f"{chi2:.4f}")
    col2.metric("Valor p (p-value)", f"{p_value:.4f}")
    col3.metric("Grados de Libertad (dof)", f"{dof}")

    with st.expander("Ver tabla de Frecuencias Esperadas"):
        st.write("Estas son las frecuencias que se esperarían si no hubiera asociación entre las variables (bajo la hipótesis nula).")
        st.dataframe(pd.DataFrame(expected_freq, index=contingency_table.index, columns=contingency_table.columns).style.format("{:.2f}"))

    st.subheader("Interpretación y Conclusión")
    
    st.markdown("##### Hipótesis de la Prueba:")
    st.markdown(f"- **Hipótesis Nula (H₀):** No existe asociación entre '{columna_filas}' y '{columna_columnas}'. Las variables son independientes.")
    st.markdown(f"- **Hipótesis Alternativa (H₁):** Existe una asociación entre '{columna_filas}' y '{columna_columnas}'. Las variables son dependientes.")
    st.markdown("---")

    st.markdown(f"##### Decisión Estadística (con α = {alpha}):")
    if p_value < alpha:
        st.success(f"**Conclusión: Se rechaza la hipótesis nula (H₀).**")
        st.markdown(f"El valor p obtenido **({p_value:.4f})** es menor que el nivel de significancia **({alpha})**. Esto indica que existe evidencia estadística suficiente para afirmar que hay una **asociación significativa** entre **'{columna_filas}'** y **'{columna_columnas}'**.")
    else:
        st.warning(f"**Conclusión: No se puede rechazar la hipótesis nula (H₀).**")
        st.markdown(f"El valor p obtenido **({p_value:.4f})** es mayor o igual que el nivel de significancia **({alpha})**. Esto indica que no hay evidencia estadística suficiente para afirmar que exista una asociación entre **'{columna_filas}'** y **'{columna_columnas}'**.")
    
    st.subheader("Visualización: Mapa de Calor (Heatmap)")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues', linewidths=.5, ax=ax)
    
    ax.set_title(f"Mapa de Calor de Frecuencias: {columna_filas} vs. {columna_columnas}", fontsize=16, fontweight='bold')
    ax.set_xlabel(columna_columnas, fontsize=12)
    ax.set_ylabel(columna_filas, fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    st.download_button(
        label="📥 Descargar Gráfico",
        data=buf,
        file_name=f"heatmap_chi2_{columna_filas}_vs_{columna_columnas}.png",
        mime="image/png"
    )

except Exception as e:
    st.error(f"Ocurrió un error al procesar los datos: {e}")
    st.warning("Verifica que el archivo CSV esté bien formado y que las columnas seleccionadas sean categóricas.")
