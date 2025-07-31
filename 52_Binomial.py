import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import io # Necesario para el buffer de descarga

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Distribución Binomial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 5:")
    st.header("Distribuciones de Probabilidad Discretas")
    st.subheader("5.2 Distribución Binomial")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Configurar Parámetros")
    
    # Controles deslizantes para los parámetros n y p
    n_ensayos = st.slider(
        "Número de ensayos (n):", 
        min_value=1, 
        max_value=100, 
        value=10, 
        help="El número total de veces que se repite el experimento."
    )
    
    prob_exito = st.slider(
        "Probabilidad de éxito (p):", 
        min_value=0.0, 
        max_value=1.0, 
        value=0.5, 
        step=0.01,
        help="La probabilidad de que ocurra un 'éxito' en un solo ensayo."
    )

# --- 3. Panel Principal ---
st.title("📊 Distribución Binomial")
st.write(
    "Esta aplicación visualiza la distribución de probabilidad binomial y te permite calcular la probabilidad "
    "para un número específico de éxitos (k)."
)
st.markdown("---")

# --- 4. Lógica de Cálculo y Visualización ---

# Fórmula de la distribución binomial
st.subheader("Fórmula de la Probabilidad Binomial")
st.latex(r"P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}")

# --- Sección de Cálculo Interactivo ---
st.subheader("Calcular Probabilidad para un Valor Específico")

# El valor máximo para k es n
k_seleccionado = st.slider(
    "Selecciona un número de éxitos (k) para calcular su probabilidad:", 
    min_value=0, 
    max_value=n_ensayos, 
    value=min(3, n_ensayos),  # Evita errores si n es muy pequeño
    help="El número de éxitos cuya probabilidad quieres calcular."
)

# Calcular la probabilidad para el k seleccionado
prob_k_seleccionado = binom.pmf(k_seleccionado, n_ensayos, prob_exito)

st.success(f"La probabilidad de obtener exactamente **{k_seleccionado}** éxito(s) en **{n_ensayos}** ensayos es **{prob_k_seleccionado:.4f}**")

# --- Visualización ---
st.subheader(f"Gráfico de la Distribución Binomial: n={n_ensayos}, p={prob_exito}")

try:
    # Preparar datos para el gráfico
    k_values = range(n_ensayos + 1)
    probabilities = [binom.pmf(k, n_ensayos, prob_exito) for k in k_values]

    fig, ax = plt.subplots(figsize=(12, 7)) # Aumentamos un poco el tamaño para más claridad

    # Gráfico de barras principal
    bars = ax.bar(k_values, probabilities, color='teal', edgecolor='black', alpha=0.6, label='Probabilidad P(X=k)')
    
    # Destacar la barra para el k seleccionado
    ax.bar(k_seleccionado, prob_k_seleccionado, color='#1C545E', edgecolor='black', 
           label=f'P(X={k_seleccionado}) = {prob_k_seleccionado:.4f}')

    # --- AÑADIR ETIQUETAS DE PROBABILIDAD ENCIMA DE LAS BARRAS ---
    for bar in bars:
        yval = bar.get_height()
        # El formato del texto puede cambiar dinámicamente para no ser tan grande
        text_format = f'{yval:.3f}' if yval > 0.001 else f'{yval:.4f}'
        ax.text(bar.get_x() + bar.get_width()/2.0, yval, text_format, 
                va='bottom', ha='center', fontsize=8) # va='bottom' lo pone justo encima
    # -----------------------------------------------------------------

    ax.set_xlabel('Número de Éxitos (k)', fontsize=12)
    ax.set_ylabel('Probabilidad', fontsize=12)
    ax.set_title(f'Distribución Binomial (n={n_ensayos}, p={prob_exito})', fontsize=16, fontweight='bold')
    
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')
    ax.set_xticks(k_values) 
    # Ajuste dinámico del eje Y para dejar espacio a las etiquetas
    if probabilities:
        ax.set_ylim(0, max(probabilities) * 1.25) 
    else:
        ax.set_ylim(0, 0.1)

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # --- BOTÓN DE DESCARGA ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight') # bbox_inches asegura que todo se guarde
    
    st.download_button(
        label="📥 Descargar Gráfico",
        data=buf.getvalue(),
        file_name=f"binomial_n{n_ensayos}_p{prob_exito:.2f}.png",
        mime="image/png"
    )
    # -------------------------

    # --- Interpretación ---
    with st.expander("Ver Interpretación de los Parámetros"):
        st.markdown(f"**Número de ensayos (n = {n_ensayos}):** Representa el número total de veces que se realiza un experimento independiente. Por ejemplo, lanzar una moneda {n_ensayos} veces.")
        st.markdown(f"**Probabilidad de éxito (p = {prob_exito}):** Es la probabilidad de que ocurra un resultado 'exitoso' en un único ensayo. Por ejemplo, la probabilidad de que salga 'cara' en un lanzamiento es {prob_exito}.")
        st.markdown(f"**Número de éxitos (k):** Es la variable que representa el número de éxitos que nos interesa contar. El gráfico muestra la probabilidad para cada posible valor de k, desde 0 hasta {n_ensayos}.")
        st.markdown(f"El gráfico de arriba muestra cómo se distribuyen las probabilidades. Los valores de **k** con las barras más altas son los resultados más probables.")

except Exception as e:
    st.error(f"Ocurrió un error al generar el gráfico: {e}")
