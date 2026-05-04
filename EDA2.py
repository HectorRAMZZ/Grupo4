import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Exploración de Datos Avanzada", layout="wide")

st.title("Aplicativo de Exploración de Datos - Nivel Pro")

uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("Archivo cargado correctamente")

        st.subheader("Vista previa")
        st.dataframe(df.head())

        # Información general
        st.subheader("Información del dataset")
        st.write(df.describe())

        # Limpieza de datos
        st.subheader("Limpieza de datos")
        if st.checkbox("Eliminar valores nulos"):
            df = df.dropna()
            st.success("Valores nulos eliminados")

        # Selección de columnas numéricas
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_columns) >= 2:
            st.subheader("Correlación interactiva")
            selected_columns = st.multiselect(
                "Selecciona columnas",
                numeric_columns,
                default=numeric_columns[:2]
            )

            if len(selected_columns) >= 2:
                corr = df[selected_columns].corr()
                fig = px.imshow(corr, text_auto=True, aspect="auto")
                st.plotly_chart(fig)

                # Descargar matriz
                csv_corr = corr.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar matriz de correlación",
                    data=csv_corr,
                    file_name="correlacion.csv",
                    mime="text/csv"
                )

        # Visualización adicional
        st.subheader("Gráficos adicionales")
        col1, col2 = st.columns(2)

        with col1:
            x_axis = st.selectbox("Eje X", df.columns)
        with col2:
            y_axis = st.selectbox("Eje Y", df.columns)

        if x_axis and y_axis:
            fig2 = px.scatter(df, x=x_axis, y=y_axis)
            st.plotly_chart(fig2)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Sube un archivo CSV para comenzar")

st.sidebar.title("Funciones incluidas")
st.sidebar.write("""
- Vista previa de datos
- Estadísticas descriptivas
- Eliminación de nulos
- Correlación interactiva
- Descarga de resultados
- Gráficos dinámicos
""")
