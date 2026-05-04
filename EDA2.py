import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Configuración principal de la página
st.set_page_config(page_title="Plataforma Integral de EDA", page_icon="📈", layout="wide")

# 2. Función para cargar datos con caché (mejora el rendimiento)
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# 3. Configuración del Menú Lateral (Sidebar)
st.sidebar.title("Navegación 🧭")
st.sidebar.write("Sube tus datos y elige el análisis.")

# El cargador de archivos ahora vive en la barra lateral
uploaded_file = st.sidebar.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Cargar los datos usando la función con caché
        df = load_data(uploaded_file)
        
        # Opciones del menú lateral
        opciones_eda = [
            "Vista General y Limpieza", 
            "Estadísticas Descriptivas", 
            "Análisis Univariado (Gráficos)", 
            "Análisis Bivariado (Correlación)"
        ]
        
        eleccion = st.sidebar.radio("Selecciona un proceso de EDA:", opciones_eda)
        
        st.sidebar.divider()
        st.sidebar.info(f"Dataset cargado: {uploaded_file.name}")
        
        # ---------------------------------------------------------
        # PESTAÑA 1: VISTA GENERAL
        # ---------------------------------------------------------
        if eleccion == "Vista General y Limpieza":
            st.title("🔍 Vista General del Dataset")
            
            st.subheader("1. Primeras filas de los datos")
            st.dataframe(df.head())
            
            st.subheader("2. Dimensiones del Dataset")
            col1, col2 = st.columns(2)
            col1.metric("Total de Filas", df.shape[0])
            col2.metric("Total de Columnas", df.shape[1])
            
            st.subheader("3. Detección de Valores Nulos")
            # Creamos un dataframe resumen de nulos
            nulos_df = df.isnull().sum().reset_index()
            nulos_df.columns = ['Columna', 'Cantidad de Nulos']
            nulos_df = nulos_df[nulos_df['Cantidad de Nulos'] > 0] # Solo mostrar las que tienen nulos
            
            if not nulos_df.empty:
                st.dataframe(nulos_df)
            else:
                st.success("¡Excelente! No hay valores nulos en este dataset.")

        # ---------------------------------------------------------
        # PESTAÑA 2: ESTADÍSTICAS DESCRIPTIVAS
        # ---------------------------------------------------------
        elif eleccion == "Estadísticas Descriptivas":
            st.title("📊 Estadísticas Descriptivas")
            st.write("Resumen matemático de las variables numéricas del dataset.")
            
            # describe() genera media, min, max, cuartiles, etc.
            st.dataframe(df.describe())

        # ---------------------------------------------------------
        # PESTAÑA 3: ANÁLISIS UNIVARIADO
        # ---------------------------------------------------------
        elif eleccion == "Análisis Univariado (Gráficos)":
            st.title("📉 Distribución de las Variables")
            st.write("Analiza cómo se comportan los datos de una columna individual.")
            
            # Selector de columna
            columna_seleccionada = st.selectbox("Elige una columna para graficar:", df.columns)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Si la columna es numérica, dibujamos un histograma
            if df[columna_seleccionada].dtype in ['float64', 'int64']:
                sns.histplot(df[columna_seleccionada], kde=True, color='teal', ax=ax)
                ax.set_title(f'Distribución de {columna_seleccionada}')
            # Si es texto/categórica, dibujamos un gráfico de barras (limitado a las 20 categorías más comunes)
            else:
                top_categorias = df[columna_seleccionada].value_counts().head(20)
                sns.barplot(x=top_categorias.values, y=top_categorias.index, palette='viridis', ax=ax)
                ax.set_title(f'Frecuencia de {columna_seleccionada} (Top 20)')
                ax.set_xlabel('Cantidad')
            
            st.pyplot(fig)

        # ---------------------------------------------------------
        # PESTAÑA 4: ANÁLISIS BIVARIADO (CORRELACIÓN)
        # ---------------------------------------------------------
        elif eleccion == "Análisis Bivariado (Correlación)":
            st.title("📈 Matriz de Correlación")
            
            # Filtrar solo columnas numéricas
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            
            if len(numeric_cols) > 1:
                selected_cols = st.multiselect(
                    "Selecciona las variables para la matriz:",
                    options=numeric_cols,
                    default=numeric_cols[:4] if len(numeric_cols) >= 4 else numeric_cols
                )
                
                if len(selected_cols) >= 2:
                    corr_matrix = df[selected_cols].corr()
                    
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.heatmap(
                        corr_matrix, 
                        annot=True, 
                        cmap="RdBu_r", # Paleta Rojo-Azul
                        fmt=".2f", 
                        vmin=-1, vmax=1, # Escala estandarizada de correlación
                        linewidths=0.5,
                        ax=ax
                    )
                    st.pyplot(fig)
                else:
                    st.warning("⚠️ Selecciona al menos dos columnas numéricas.")
            else:
                st.error("❌ El dataset no tiene suficientes variables numéricas para calcular correlaciones.")
                
    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")

else:
    # Pantalla de inicio si no hay archivo
    st.title("Bienvenido a tu Plataforma de EDA")
    st.info("👈 Por favor, sube un archivo CSV en el menú lateral para comenzar el análisis.")
