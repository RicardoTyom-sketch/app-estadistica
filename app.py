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

        # ── MÓDULO VISUALIZACIÓN ──
elif modulo == "Visualización":
    st.header("Visualización de Distribuciones")

    if st.session_state.datos is None:
        st.warning("Primero carga datos en el módulo **Carga de Datos**")
    else:
        import matplotlib.pyplot as plt
        import seaborn as sns
        from scipy import stats

        df = st.session_state.datos
        variable = st.session_state.variable
        datos = df[variable].dropna()

        st.subheader(f"Variable: {variable}")

        # Estadísticos básicos
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Media", f"{datos.mean():.2f}")
        col2.metric("Mediana", f"{datos.median():.2f}")
        col3.metric("Desv. Estándar", f"{datos.std():.2f}")
        col4.metric("N", len(datos))

        st.markdown("---")

        # Gráficas
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Histograma + KDE
        sns.histplot(datos, kde=True, ax=axes[0], color="steelblue")
        axes[0].set_title("Histograma + KDE")
        axes[0].set_xlabel(variable)

        # Boxplot
        sns.boxplot(y=datos, ax=axes[1], color="lightcoral")
        axes[1].set_title("Boxplot")

        st.pyplot(fig)

        # ── ANÁLISIS AUTOMÁTICO ──
        st.markdown("---")
        st.subheader("Análisis de la distribución")

        datos_limpios = datos.dropna()
        skewness = datos_limpios.skew()
        kurtosis = datos_limpios.kurtosis()

        Q1 = datos_limpios.quantile(0.25)
        Q3 = datos_limpios.quantile(0.75)
        IQR = Q3 - Q1

        outliers = datos_limpios[
            (datos_limpios < Q1 - 1.5 * IQR) |
            (datos_limpios > Q3 + 1.5 * IQR)
        ]

        # Normalidad
        if abs(skewness) < 0.5:
            st.success("La distribución parece aproximadamente normal")
        else:
            st.warning("La distribución no parece normal")

        # Sesgo
        if skewness > 0.5:
            st.info(f"Sesgo positivo (cola derecha): {skewness:.2f}")
        elif skewness < -0.5:
            st.info(f"Sesgo negativo (cola izquierda): {skewness:.2f}")
        else:
            st.info(f"Sin sesgo significativo: {skewness:.2f}")

        # Outliers
        if len(outliers) > 0:
            st.warning(f"Se detectaron {len(outliers)} outliers")
        else:
            st.success("No se detectaron outliers")

