import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import io

# --- 1. Configuración de la Página ---
st.set_page_config(
    page_title="Distribución de Poisson",
    page_icon="🔔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Barra Lateral con Controles ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("CAPÍTULO 5:")
    st.header("Distribuciones de Probabilidad Discretas")
    st.subheader("5.3 Distribución de Poisson")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Configurar Parámetros")
    
    lambda_avg = st.slider(
        "Tasa promedio de ocurrencias (λ):", 
        min_value=0.1, 
        max_value=30.0, 
        value=6.0,
        step=0.1,
        help="El número promedio de veces que ocurre un evento en un intervalo."
    )

# --- 3. Panel Principal ---
st.title("🔔 Distribución de Poisson")
st.write(
    "La distribución de Poisson modela la probabilidad del número de veces que ocurre un evento en un intervalo fijo de tiempo o espacio, "
    "dado que conocemos la tasa promedio (λ) con la que sucede."
)
st.markdown("---")

# --- 4. Lógica de Cálculo y Visualización ---

st.subheader("Fórmula de la Probabilidad de Poisson")
st.latex(r"P(X=k) = \frac{e^{-\lambda} \lambda^k}{k!}")

st.subheader("Calcular Probabilidades")

max_k_slider = max(20, int(lambda_avg * 2) + 5) 
col1, col2 = st.columns([1, 2])

with col1:
    tipo_calculo = st.radio(
        "Selecciona el tipo de probabilidad a calcular:",
        ("Exactamente (P(X = k))", 
         "A lo más (P(X ≤ k))", 
         "Menos de (P(X < k))",
         "Al menos (P(X ≥ k))",
         "Más de (P(X > k))",
         "En un rango (k₁ ≤ X ≤ k₂)" # NUEVA OPCIÓN
        ),
        key="tipo_calculo_poisson"
    )

    # Lógica para mostrar uno o dos sliders
    if "En un rango" in tipo_calculo:
        k_min_range = st.slider(
            "Valor mínimo del rango (k₁):", 
            min_value=0, 
            max_value=max_k_slider, 
            value=4,
            help="Límite inferior del rango (inclusivo)."
        )
        k_max_range = st.slider(
            "Valor máximo del rango (k₂):", 
            min_value=k_min_range, # Asegura que k_max no sea menor que k_min
            max_value=max_k_slider, 
            value=8,
            help="Límite superior del rango (inclusivo)."
        )
    else:
        k_seleccionado = st.slider(
            "Número de ocurrencias (k):", 
            min_value=0, 
            max_value=max_k_slider, 
            value=4,
            help="El número de eventos cuya probabilidad quieres calcular."
        )

# Realizar el cálculo basado en la selección
prob_calculada = 0.0
texto_resultado = ""

if "Exactamente" in tipo_calculo:
    prob_calculada = poisson.pmf(k=k_seleccionado, mu=lambda_avg)
    texto_resultado = f"La probabilidad de que ocurran **exactamente {k_seleccionado}** eventos es **{prob_calculada:.4f}**."

elif "A lo más" in tipo_calculo:
    prob_calculada = poisson.cdf(k=k_seleccionado, mu=lambda_avg)
    texto_resultado = f"La probabilidad de que ocurran **{k_seleccionado} o menos** eventos es **{prob_calculada:.4f}**."

elif "Menos de" in tipo_calculo:
    prob_calculada = poisson.cdf(k=k_seleccionado - 1, mu=lambda_avg) if k_seleccionado > 0 else 0
    texto_resultado = f"La probabilidad de que ocurran **menos de {k_seleccionado}** eventos es **{prob_calculada:.4f}**."

elif "Al menos" in tipo_calculo:
    prob_calculada = 1 - poisson.cdf(k=k_seleccionado - 1, mu=lambda_avg) if k_seleccionado > 0 else 1.0
    texto_resultado = f"La probabilidad de que ocurran **{k_seleccionado} o más** eventos es **{prob_calculada:.4f}**."

elif "Más de" in tipo_calculo:
    prob_calculada = 1 - poisson.cdf(k=k_seleccionado, mu=lambda_avg)
    texto_resultado = f"La probabilidad de que ocurran **más de {k_seleccionado}** eventos es **{prob_calculada:.4f}**."

elif "En un rango" in tipo_calculo: # LÓGICA PARA EL NUEVO CÁLCULO
    if k_min_range == 0:
        prob_calculada = poisson.cdf(k=k_max_range, mu=lambda_avg)
    else:
        prob_calculada = poisson.cdf(k=k_max_range, mu=lambda_avg) - poisson.cdf(k=k_min_range - 1, mu=lambda_avg)
    texto_resultado = f"La probabilidad de que ocurran **entre {k_min_range} y {k_max_range}** eventos (inclusive) es **{prob_calculada:.4f}**."


with col2:
    st.success(texto_resultado)
    st.write(f"Esto representa aproximadamente un **{prob_calculada*100:.2f}%** de probabilidad.")


# --- Visualización ---
st.subheader(f"Gráfico de la Distribución de Poisson: λ = {lambda_avg}")

try:
    max_k_grafico = max(20, int(lambda_avg * 2.5))
    k_values = np.arange(0, max_k_grafico + 1)
    probabilities = poisson.pmf(k=k_values, mu=lambda_avg)

    fig, ax = plt.subplots(figsize=(12, 7))

    # Identificar las barras a resaltar
    resaltar_mask = np.zeros_like(k_values, dtype=bool)
    if "Exactamente" in tipo_calculo:
        resaltar_mask = (k_values == k_seleccionado)
    elif "A lo más" in tipo_calculo:
        resaltar_mask = (k_values <= k_seleccionado)
    elif "Menos de" in tipo_calculo:
        resaltar_mask = (k_values < k_seleccionado)
    elif "Al menos" in tipo_calculo:
        resaltar_mask = (k_values >= k_seleccionado)
    elif "Más de" in tipo_calculo:
        resaltar_mask = (k_values > k_seleccionado)
    elif "En un rango" in tipo_calculo: # MÁSCARA PARA LA NUEVA VISUALIZACIÓN
        resaltar_mask = (k_values >= k_min_range) & (k_values <= k_max_range)
    
    # Gráfico de barras
    ax.bar(k_values, probabilities, color='skyblue', alpha=0.7, label='Probabilidad P(X=k)')
    ax.bar(k_values[resaltar_mask], probabilities[resaltar_mask], color='navy', label=f'Probabilidad Calculada ({prob_calculada:.4f})')

    ax.set_xlabel('Número de Ocurrencias (k)', fontsize=12)
    ax.set_ylabel('Probabilidad', fontsize=12)
    ax.set_title(f'Distribución de Poisson (λ={lambda_avg})', fontsize=16, fontweight='bold')
    
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6, axis='y')
    ax.set_xticks(k_values)
    plt.xticks(rotation=90)
    ax.set_xlim(-0.5, max_k_grafico + 0.5)

    st.pyplot(fig)

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
    
    st.download_button(
        label="📥 Descargar Gráfico",
        data=buf.getvalue(),
        file_name=f"poisson_lambda{lambda_avg:.2f}.png",
        mime="image/png"
    )

    with st.expander("Ver Interpretación de los Parámetros"):
        st.markdown(f"**Tasa Promedio (λ = {lambda_avg}):** Representa el número promedio de eventos que se espera que ocurran en un intervalo.")
        st.markdown(f"**Número de Ocurrencias (k):** Es la variable que representa el número de eventos que nos interesa contar.")
        st.markdown(f"El gráfico de arriba ilustra que los resultados más probables son los que se agrupan alrededor de la tasa promedio λ. A medida que 'k' se aleja de {lambda_avg}, la probabilidad de observar ese número de eventos disminuye.")

except Exception as e:
    st.error(f"Ocurrió un error al generar el gráfico: {e}")
