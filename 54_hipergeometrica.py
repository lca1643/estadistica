import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import hypergeom
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Distribución Hipergeométrica",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 5:")
    st.header("Distribuciones de Probabilidad Discretas")
    st.subheader("5.4 Distribución Hipergeométrica")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Configurar Parámetros")
    st.write("Define las características de la población y de la muestra.")

    # Controles para los parámetros N, K, n
    poblacion_N = st.number_input(
        "Tamaño de la población (N):", 
        min_value=1, 
        value=200, 
        help="El número total de elementos en la población. Ej: 200 bombillas en un lote."
    )
    
    exitos_poblacion_K = st.number_input(
        "Nº de 'éxitos' en la población (K):", 
        min_value=0, 
        max_value=poblacion_N, # K no puede ser mayor que N
        value=10, 
        help="El número total de elementos con la característica de interés. Ej: 10 bombillas defectuosas."
    )

    muestra_n = st.number_input(
        "Tamaño de la muestra (n):", 
        min_value=1, 
        max_value=poblacion_N, # n no puede ser mayor que N
        value=15, 
        help="El número de elementos extraídos de la población sin reemplazo. Ej: 15 bombillas inspeccionadas."
    )

# --- 3. Panel Principal ---
st.title("🏭 Distribución Hipergeométrica")
st.write(
    "Esta distribución calcula la probabilidad de obtener un número específico de 'éxitos' en una muestra extraída **sin reemplazo** "
    "de una población finita. Es ideal para escenarios de control de calidad."
)
st.markdown("---")

# --- 4. Lógica de Cálculo y Visualización ---

st.subheader("Fórmula de la Probabilidad Hipergeométrica")
st.latex(r"P(X=k) = \frac{\binom{K}{k} \binom{N-K}{n-k}}{\binom{N}{n}}")

st.subheader("Calcular Probabilidades")

# El número máximo de éxitos en la muestra no puede superar n ni K.
max_k_slider = min(muestra_n, exitos_poblacion_K)

col1, col2 = st.columns([1, 2])

with col1:
    tipo_calculo = st.radio(
        "Selecciona el tipo de probabilidad a calcular:",
        ("Exactamente (P(X = k))", 
         "A lo más (P(X ≤ k))", 
         "Menos de (P(X < k))",
         "Al menos (P(X ≥ k))",
         "Más de (P(X > k))",
         "En un rango (k₁ ≤ X ≤ k₂)"
        ),
        key="tipo_calculo_hypergeom"
    )

    if "En un rango" in tipo_calculo:
        k_min_range = st.slider("Valor mínimo del rango (k₁):", 0, max_k_slider, value=0)
        k_max_range = st.slider("Valor máximo del rango (k₂):", k_min_range, max_k_slider, value=min(2, max_k_slider))
    else:
        k_seleccionado = st.slider("Número de éxitos en la muestra (k):", 0, max_k_slider, value=min(1, max_k_slider))

# Realizar el cálculo
# Nota: La firma de Scipy es hypergeom.pmf(k, M, n, N) donde M=Población, n=Éxitos en Población, N=Tamaño Muestra
prob_calculada = 0.0
texto_resultado = ""

# Asignación de variables para mayor claridad en las funciones de scipy
M, n_scipy, N_scipy = poblacion_N, exitos_poblacion_K, muestra_n

if "Exactamente" in tipo_calculo:
    prob_calculada = hypergeom.pmf(k=k_seleccionado, M=M, n=n_scipy, N=N_scipy)
    texto_resultado = f"La probabilidad de encontrar **exactamente {k_seleccionado}** éxito(s) es **{prob_calculada:.4f}**."

elif "A lo más" in tipo_calculo:
    prob_calculada = hypergeom.cdf(k=k_seleccionado, M=M, n=n_scipy, N=N_scipy)
    texto_resultado = f"La probabilidad de encontrar **{k_seleccionado} o menos** éxito(s) es **{prob_calculada:.4f}**."

elif "Menos de" in tipo_calculo:
    prob_calculada = hypergeom.cdf(k=k_seleccionado - 1, M=M, n=n_scipy, N=N_scipy) if k_seleccionado > 0 else 0
    texto_resultado = f"La probabilidad de encontrar **menos de {k_seleccionado}** éxito(s) es **{prob_calculada:.4f}**."

elif "Al menos" in tipo_calculo:
    prob_calculada = hypergeom.sf(k=k_seleccionado - 1, M=M, n=n_scipy, N=N_scipy)
    texto_resultado = f"La probabilidad de encontrar **{k_seleccionado} o más** éxito(s) es **{prob_calculada:.4f}**."

elif "Más de" in tipo_calculo:
    prob_calculada = hypergeom.sf(k=k_seleccionado, M=M, n=n_scipy, N=N_scipy)
    texto_resultado = f"La probabilidad de encontrar **más de {k_seleccionado}** éxito(s) es **{prob_calculada:.4f}**."

elif "En un rango" in tipo_calculo:
    prob_superior = hypergeom.cdf(k=k_max_range, M=M, n=n_scipy, N=N_scipy)
    prob_inferior = hypergeom.cdf(k=k_min_range - 1, M=M, n=n_scipy, N=N_scipy)
    prob_calculada = prob_superior - prob_inferior
    texto_resultado = f"La probabilidad de encontrar **entre {k_min_range} y {k_max_range}** éxito(s) es **{prob_calculada:.4f}**."

with col2:
    st.success(texto_resultado)
    st.write(f"Esto representa aproximadamente un **{prob_calculada*100:.2f}%** de probabilidad.")

# --- Visualización ---
st.subheader(f"Gráfico de la Distribución Hipergeométrica")

try:
    k_values = np.arange(0, max_k_slider + 1)
    probabilities = hypergeom.pmf(k_values, M=M, n=n_scipy, N=N_scipy)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Máscara para resaltar las barras
    resaltar_mask = np.zeros_like(k_values, dtype=bool)
    if "En un rango" in tipo_calculo:
        resaltar_mask = (k_values >= k_min_range) & (k_values <= k_max_range)
    elif "Exactamente" in tipo_calculo:
        resaltar_mask = (k_values == k_seleccionado)
    # ... (y así para los demás casos)
    elif "A lo más" in tipo_calculo: resaltar_mask = (k_values <= k_seleccionado)
    elif "Menos de" in tipo_calculo: resaltar_mask = (k_values < k_seleccionado)
    elif "Al menos" in tipo_calculo: resaltar_mask = (k_values >= k_seleccionado)
    elif "Más de" in tipo_calculo: resaltar_mask = (k_values > k_seleccionado)

    ax.bar(k_values, probabilities, color='c', alpha=0.7, label='Probabilidad P(X=k)')
    ax.bar(k_values[resaltar_mask], probabilities[resaltar_mask], color='darkcyan', label=f'Probabilidad Calculada ({prob_calculada:.4f})')
    
    ax.set_xlabel('Número de Éxitos en la Muestra (k)', fontsize=12)
    ax.set_ylabel('Probabilidad', fontsize=12)
    ax.set_title(f'Distribución Hipergeométrica', fontsize=16, fontweight='bold')
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')
    ax.set_xticks(k_values)
    ax.set_xlim(-0.5, max_k_slider + 0.5)

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    st.download_button(label="📥 Descargar Gráfico", data=buf.getvalue(), file_name="hypergeometric_dist.png", mime="image/png")

    with st.expander("Ver Interpretación de los Parámetros (Ej: Bombillas)"):
        st.markdown(f"**Población Total (N = {poblacion_N}):** El lote completo consta de {poblacion_N} bombillas.")
        st.markdown(f"**Éxitos en la Población (K = {exitos_poblacion_K}):** Dentro de ese lote, se sabe que hay {exitos_poblacion_K} bombillas defectuosas (nuestros 'éxitos').")
        st.markdown(f"**Muestra (n = {muestra_n}):** Se selecciona una muestra aleatoria de {muestra_n} bombillas para inspección, sin devolverlas al lote.")
        st.markdown(f"**Variable (k):** El gráfico y los cálculos muestran la probabilidad de encontrar un número 'k' de bombillas defectuosas en la muestra de {muestra_n}.")

except Exception as e:
    st.error(f"Ocurrió un error al generar el gráfico: {e}")
