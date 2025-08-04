import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# --- 1. Configuración de la Página y Estilos ---
st.set_page_config(
    page_title="Generador de Gráfico de Barras",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INYECTAR CSS PARA PERSONALIZACIÓN COMPLETA ---
st.markdown(
    """
    <style>
    /* Contenedor de la barra lateral */
    [data-testid="stSidebar"] {
        background-color: #094C72;
    }

    /* Texto general en la barra lateral */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label {
        color: white;
    }
    
    .st-bb, .st-at, .st-cs, .st-cn {
        color: black;
    }

    [data-testid="stFileUploaderFile"] {
        color: white;
    }

    /* Botón de carga de archivos */
    [data-testid="stFileUploader"] button {
        background-color: #094C72;
        color: white;
        border: 1px solid #094C72;
    }

    [data-testid="stFileUploader"] button:hover {
        background-color: #0B5A8A;
        color: white;
        border: 1px solid #0B5A8A;
    }

    /* Estilo para el recuadro de información personalizado */
    .custom-info-box {
        background-color: #094C72;
        color: white;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        display: flex;
        align-items: center;
        font-size: 16px;
        border-left: 4px solid #0B5A8A;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .custom-info-box svg {
        margin-right: 12px;
        flex-shrink: 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)
# ---------------------------------------------------

# --- RESTO DEL CÓDIGO ---
with st.sidebar:
    st.title("Fundamentos de Estadística")
    st.header("Herramientas de Visualización")
    st.subheader("Generador de Gráfico de Barras")
    st.markdown("*Autor: Luis Corona Alcantar*")
    st.markdown("_Correo: lca1643@gmail.com_")
    st.markdown("---")
    
    st.header("1. Cargar Archivo de Datos")
    
    uploaded_file = st.file_uploader(
        "Carga tu archivo (CSV o Excel)",
        type=["csv", "xlsx"],
        label_visibility="collapsed"
    )
    
    df = None
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

st.title("📊 Generador de Gráfico de Barras desde Archivo")
st.write(
    "Carga un archivo, selecciona las columnas y la aplicación creará automáticamente un gráfico de barras ordenado, "
    "mostrando los valores originales en cada barra."
)
st.markdown("---")

if df is not None:
    st.header("Vista Previa de los Datos")
    st.dataframe(df.head())

    with st.sidebar:
        st.header("2. Mapeo de Columnas")
        columnas = df.columns.tolist()
        label_col = st.selectbox("Selecciona la columna para las Etiquetas/Categorías:", columnas)
        value_col = st.selectbox("Selecciona la columna para los Valores (Numéricos):", columnas, index=1 if len(columnas) > 1 else 0)

    if pd.api.types.is_numeric_dtype(df[value_col]):
        
        processed_data = df.groupby(label_col)[value_col].sum().reset_index()
        fig, ax = plt.subplots(figsize=(11, 7))

        st.subheader(f"Resultado: Gráfico de Barras para {value_col}")
        
        processed_data = processed_data.sort_values(by=value_col, ascending=False)
        
        num_bars = len(processed_data)
        colors = plt.get_cmap('viridis')(np.linspace(0.2, 0.8, num_bars))
        
        bars = ax.bar(processed_data[label_col], processed_data[value_col], color=colors)
        
        for bar in bars:
            height = bar.get_height()
            label_text = f'{height:.1%}' if (height < 1 and height > 0) else f'{height:,.0f}'
            
            ax.text(bar.get_x() + bar.get_width() / 2, height, label_text,
                    ha='center', va='bottom', fontsize=9, fontweight='bold')

        ax.set_ylabel(value_col)
        ax.set_xlabel(label_col)
        plt.xticks(rotation=45, ha="right")
        if not processed_data.empty:
            ax.set_ylim(0, processed_data[value_col].max() * 1.15)
        
        ax.set_title(f"Distribución de {value_col}", fontsize=16, fontweight='bold')
        ax.grid(axis='y', linestyle='--', alpha=0.6)
        fig.tight_layout()

        st.pyplot(fig)
        
        buf = io.BytesIO()
        fig.savefig(buf, format="png", dpi=300, bbox_inches='tight')
        st.download_button(
            label="📥 Descargar Gráfico",
            data=buf.getvalue(),
            file_name=f"{value_col.replace(' ', '_').lower()}_chart.png",
            mime="image/png"
        )
        
    else:
        st.error(f"Error: La columna de valores ('{value_col}') no es numérica. Por favor, elige una columna con números.")

# Recuadro de información personalizado con fondo azul océano
if uploaded_file is None:
    st.markdown(
        """
        <div class="custom-info-box">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="white">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
            </svg>
            <div>Esperando a que se cargue un archivo de datos para generar el gráfico de barras.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    with st.expander("¿Qué formato debe tener mi archivo?"):
        st.markdown("""
        - Tu archivo puede ser un **CSV** o **Excel**.
        - Debe tener una **columna de encabezados** en la primera fila.
        - Asegúrate de tener al menos una columna con texto (categorías) y otra con números (valores).
        """)
