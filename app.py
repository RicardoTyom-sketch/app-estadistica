import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="App Estadística", layout="wide")

st.title("Análisis Estadístico con IA")
st.markdown("---")

# Menú lateral
modulo = st.sidebar.selectbox("Selecciona un módulo", [
    "Inicio",
    "Carga de Datos",
    "Visualización",
    "Prueba Z",
    "Asistente IA"
])

# Variables globales en sesión
if "datos" not in st.session_state:
    st.session_state.datos = None
if "variable" not in st.session_state:
    st.session_state.variable = None

# ── MÓDULO INICIO ──
if modulo == "Inicio":
    st.header("Bienvenido")
    st.write("Esta app permite visualizar distribuciones, realizar pruebas de hipótesis e interpretar resultados con IA.")
    st.info("Comienza cargando tus datos en el módulo **Carga de Datos**")

# ── MÓDULO CARGA DE DATOS ──
elif modulo == "Carga de Datos":
    st.header("Carga de Datos")

    opcion = st.radio("¿Cómo deseas cargar los datos?", 
                      ["Subir CSV", "Generar datos sintéticos"])

    if opcion == "Subir CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            st.session_state.datos = df
            st.success("Archivo cargado correctamente")
            st.dataframe(df.head())

    else:
        st.subheader("Generador de datos sintéticos")
        n = st.slider("Número de datos (n)", 30, 500, 100)
        media = st.number_input("Media", value=50.0)
        desv = st.number_input("Desviación estándar", value=10.0)

        if st.button("Generar datos"):
            datos = np.random.normal(loc=media, scale=desv, size=n)
            df = pd.DataFrame({"variable": datos})
            st.session_state.datos = df
            st.success(f"Se generaron {n} datos con media={media} y σ={desv}")
            st.dataframe(df.head())

    # Selección de variable
    if st.session_state.datos is not None:
        df = st.session_state.datos
        columnas = df.select_dtypes(include=[np.number]).columns.tolist()
        variable = st.selectbox("Selecciona la variable a analizar", columnas)
        st.session_state.variable = variable
        st.info(f"Variable seleccionada: **{variable}**")