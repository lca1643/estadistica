import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="CDF Binomial",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 5:")
    st.header("Distribuciones de Probabilidad Discretas")
    # Título específico para esta sección
    st.subheader("5.2.1 Función de Distribución Acumulada (CDF) Binomial")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Configurar Parámetros")
    
    # Controles deslizantes para los parámetros n y p (igual que antes)
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
st.title("📈 Función de Distribución Acumulada (CDF) Binomial")
st.write(
    "Esta aplicación visualiza la **Función de Distribución Acumulada (CDF)** de una distribución binomial. "
    "La CDF nos dice la probabilidad de obtener **k o menos** éxitos."
)
st.markdown("---")

# --- 4. Lógica de Cálculo y Visualización ---

# Fórmula de la CDF binomial
st.subheader("Fórmula de la Función de Distribución Acumulada")
st.latex(r"P(X \leq k) = \sum_{i=0}^{k} \binom{n}{i} p^i (1-p)^{n-i}")

# --- Sección de Cálculo Interactivo ---
st.subheader("Calcular Probabilidad Acumulada para un Valor Específico")

# El valor máximo para k es n
k_seleccionado = st.slider(
    "Selecciona un número de éxitos (k) para calcular su probabilidad acumulada:", 
    min_value=0, 
    max_value=n_ensayos, 
    value=min(3, n_ensayos),
    help="La probabilidad acumulada de obtener un número de éxitos menor o igual a k."
)

# Calcular la probabilidad ACUMULADA para el k seleccionado
prob_acumulada_k = binom.cdf(k_seleccionado, n_ensayos, prob_exito)

st.info(f"La probabilidad de obtener **{k_seleccionado} o menos** éxito(s) en **{n_ensayos}** ensayos es **{prob_acumulada_k:.4f}**")

# --- Visualización ---
st.subheader(f"Gráfico de la CDF: n={n_ensayos}, p={prob_exito}")

try:
    # Preparar datos para el gráfico
    # Necesitamos k hasta n+1 para dibujar el último escalón
    k_values = np.arange(0, n_ensayos + 2)
    cdf_values = np.array([binom.cdf(k, n_ensayos, prob_exito) for k in k_values])

    fig, ax = plt.subplots(figsize=(12, 7))

    # DIBUJAR LA CDF COMO FUNCIÓN ESCALONADA (Líneas horizontales)
    ax.hlines(y=cdf_values[:-1], xmin=k_values[:-1], xmax=k_values[1:],
              colors='blue', linestyles='solid', linewidth=2, label='CDF Binomial P(X ≤ k)')

    # DIBUJAR PUNTOS SÓLIDOS en los saltos para mayor claridad
    ax.scatter(k_values[:-1], cdf_values[:-1], color='blue', zorder=5)

    # DESTACAR LA PROBABILIDAD ACUMULADA para el k seleccionado
    if k_seleccionado <= n_ensayos:
        ax.hlines(y=prob_acumulada_k, xmin=-0.5, xmax=k_seleccionado, colors='purple', linestyles='--',
                  label=f'$P(X \leq {k_seleccionado}) = {prob_acumulada_k:.4f}$')
        ax.plot([k_seleccionado, k_seleccionado], [0, prob_acumulada_k], 'purple', linestyle='--') # Línea vertical

    # Estilo y etiquetas del gráfico
    ax.set_xlabel('Número de Éxitos (k)', fontsize=12)
    ax.set_ylabel('Probabilidad Acumulada P(X ≤ k)', fontsize=12)
    ax.set_title(f'Función de Distribución Acumulada (CDF)', fontsize=16, fontweight='bold')
    
    ax.legend(loc='lower right')
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')
    ax.set_xticks(range(n_ensayos + 1)) 
    ax.set_xlim(-0.5, n_ensayos + 0.5) 
    ax.set_ylim(0, 1.05) 

    # Mostrar el gráfico en Streamlit
    st.pyplot(fig)

    # --- BOTÓN DE DESCARGA ---
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    
    st.download_button(
        label="📥 Descargar Gráfico de la CDF",
        data=buf.getvalue(),
        file_name=f"CDF_binomial_n{n_ensayos}_p{prob_exito:.2f}.png",
        mime="image/png"
    )

    # --- Interpretación ---
    with st.expander("Ver Interpretación de la CDF"):
        st.markdown(f"**¿Qué significa este gráfico?**")
        st.markdown(
            "La Función de Distribución Acumulada (CDF) muestra la probabilidad de que la variable aleatoria X (número de éxitos) "
            "tome un valor **menor o igual** a un número específico 'k'."
        )
        st.markdown(
            "- El **eje X** representa el número de éxitos (k).\n"
            "- El **eje Y** representa la probabilidad acumulada `P(X ≤ k)`."
        )
        st.markdown(
            f"Por ejemplo, para `k = {k_seleccionado}`, el valor en el eje Y (`{prob_acumulada_k:.4f}`) es la suma de las probabilidades de obtener 0 éxitos, 1 éxito, ..., hasta {k_seleccionado} éxitos."
        )
        st.markdown(
            "Observe cómo la función crece en 'escalones' hasta llegar a 1. La altura de cada escalón es igual a la probabilidad de ese valor de 'k' específico (como se veía en el gráfico de barras anterior)."
        )

except Exception as e:
    st.error(f"Ocurrió un error al generar el gráfico: {e}")