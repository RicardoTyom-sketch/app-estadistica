import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="App Estadística", layout="wide")

st.title("Análisis Estadístico con IA")
st.markdown("---")

st.markdown("""
    <style>
        .block-container {
             padding-top: 4rem;
            padding-bottom: 1rem;
            max-width: 1100px;
        }
        h1 { 
            font-size: 1.8rem !important; 
            color: #FFFFFF !important;
            text-shadow: 0 0 10px #0066FF, 0 0 20px #0066FF;
        }
        h2 { 
            font-size: 1.4rem !important; 
            color: #FFFFFF !important;
            text-shadow: 0 0 8px #0066FF;
        }
        h3 { 
            font-size: 1.2rem !important; 
            color: #FFFFFF !important;
            text-shadow: 0 0 6px #0066FF;
        }
        .stApp {
            background-color: #0a0a0a;
            color: white;
        }
        .stSidebar {
            background-color: #111111;
            border-right: 2px solid #0066FF;
        }
        div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            text-shadow: 0 0 8px #0066FF;
        }
        .stButton > button {
            background-color: #0a0a0a;
            color: #FFFFFF;
            border: 2px solid #0066FF;
            border-radius: 8px;
        }
        .stButton > button:hover {
            background-color: #0066FF;
            color: white;
            box-shadow: 0 0 10px #0066FF;
        }
    </style>
""", unsafe_allow_html=True)

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
            st.session_state.variable = "variable"
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
            st.write(f"Curtosis: {kurtosis:.2f}")

        # Outliers
        if len(outliers) > 0:
            st.warning(f"Se detectaron {len(outliers)} outliers")
        else:
            st.success("No se detectaron outliers")

          # ── MÓDULO PRUEBA Z ──
elif modulo == "Prueba Z":
    st.header("Prueba de Hipótesis Z")

    if st.session_state.datos is None:
        st.warning("Primero carga datos en el módulo **Carga de Datos**")
    else:
        from scipy import stats
        import matplotlib.pyplot as plt
        import numpy as np
        import numpy as np

        df = st.session_state.datos
        variable = st.session_state.variable
        datos = df[variable].dropna()

        st.subheader("Definir hipótesis")

        col1, col2 = st.columns(2)
        with col1:
            mu0 = st.number_input("Media hipotética (H0: μ =)", value=50.0)
            sigma = st.number_input("Desviación estándar poblacional (σ)", value=10.0)
            alpha = st.selectbox("Nivel de significancia (α)", [0.01, 0.05, 0.10])
        with col2:
            tipo = st.radio("Tipo de prueba", [
                "Bilateral (≠)",
                "Cola izquierda (<)",
                "Cola derecha (>)"
            ])
            st.markdown(f"**H0:** μ = {mu0}")
            if tipo == "Bilateral (≠)":
                st.markdown(f"**H1:** μ ≠ {mu0}")
            elif tipo == "Cola izquierda (<)":
                st.markdown(f"**H1:** μ < {mu0}")
            else:
                st.markdown(f"**H1:** μ > {mu0}")

        if st.button("Calcular prueba Z"):
            n = len(datos)
            media_muestral = datos.mean()
            z = (media_muestral - mu0) / (sigma / np.sqrt(n))

            if tipo == "Bilateral (≠)":
                p_value = 2 * (1 - stats.norm.cdf(abs(z)))
            elif tipo == "Cola izquierda (<)":
                p_value = stats.norm.cdf(z)
            else:
                p_value = 1 - stats.norm.cdf(z)

            rechazar = p_value < alpha

            st.markdown("---")
            st.subheader("Resultados")

            col1, col2, col3 = st.columns(3)
            col1.metric("Estadístico Z", f"{z:.4f}")
            col2.metric("p-value", f"{p_value:.4f}")
            col3.metric("n", n)

            if rechazar:
                st.error(f"Se rechaza H0 con α={alpha}")
            else:
                st.success(f"No se rechaza H0 con α={alpha}")

            st.session_state.z = z
            st.session_state.p_value = p_value
            st.session_state.mu0 = mu0
            st.session_state.sigma = sigma
            st.session_state.alpha = alpha
            st.session_state.tipo = tipo
            st.session_state.media_muestral = media_muestral
            st.session_state.n = n
            st.session_state.rechazar = rechazar  

               # ── CURVA CON REGIÓN CRÍTICA ──
            fig, ax = plt.subplots(figsize=(10, 4))
            x = np.linspace(-4, 4, 1000)
            y = stats.norm.pdf(x)
            ax.plot(x, y, 'b-', linewidth=2)
            ax.fill_between(x, y, alpha=0.1, color='blue')

            if tipo == "Bilateral (≠)":
                z_crit = stats.norm.ppf(1 - alpha/2)
                ax.fill_between(x, y, where=(x <= -z_crit), color='red', alpha=0.5, label='Región de rechazo')
                ax.fill_between(x, y, where=(x >= z_crit), color='red', alpha=0.5)
            elif tipo == "Cola izquierda (<)":
                z_crit = stats.norm.ppf(alpha)
                ax.fill_between(x, y, where=(x <= z_crit), color='red', alpha=0.5, label='Región de rechazo')
            else:
                z_crit = stats.norm.ppf(1 - alpha)
                ax.fill_between(x, y, where=(x >= z_crit), color='red', alpha=0.5, label='Región de rechazo')

            ax.axvline(x=z, color='green', linestyle='--', linewidth=2, label=f'Z calculado = {z:.4f}')
            ax.set_title("Distribución Normal con Región Crítica")
            ax.set_xlabel("Z")
            ax.legend()
            st.pyplot(fig)

               # ── ASISTENTE IA ──
elif modulo == "Asistente IA":
    st.header(" Asistente IA - Gemini")

    if st.session_state.datos is None:
        st.warning("Primero carga datos y ejecuta la prueba Z")
    elif "z" not in st.session_state:
        st.warning("Primero ejecuta la prueba Z")
    else:
        import google.generativeai as genai
        import os
        from dotenv import load_dotenv

        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)

        st.subheader("Resumen estadístico")
        st.write(f"**Media muestral:** {st.session_state.media_muestral:.2f}")
        st.write(f"**Media hipotética (H0):** {st.session_state.mu0}")
        st.write(f"**n:** {st.session_state.n}")
        st.write(f"**σ:** {st.session_state.sigma}")
        st.write(f"**α:** {st.session_state.alpha}")
        st.write(f"**Tipo de prueba:** {st.session_state.tipo}")
        st.write(f"**Z calculado:** {st.session_state.z:.4f}")
        st.write(f"**p-value:** {st.session_state.p_value:.4f}")
        st.write(f"**Decisión:** {'Se rechaza H0' if st.session_state.rechazar else 'No se rechaza H0'}")

        st.markdown("---")

        if st.button("Consultar a Gemini"):
            prompt = f"""Se realizó una prueba Z con los siguientes parámetros:
media muestral = {st.session_state.media_muestral:.2f}
media hipotética = {st.session_state.mu0}
n = {st.session_state.n}
sigma = {st.session_state.sigma}
alpha = {st.session_state.alpha}
tipo de prueba = {st.session_state.tipo}
El estadístico Z fue = {st.session_state.z:.4f}
p-value = {st.session_state.p_value:.4f}
¿Se rechaza H0? Explica la decisión y si los supuestos de la prueba son razonables."""

            with st.spinner("Consultando a Gemini..."):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(prompt)
                    st.subheader("Respuesta de Gemini")
                    st.write(response.text)

                    st.markdown("---")
                    st.subheader("¿Coincide con tu decisión?")
                    decision_app = "Se rechaza H0" if st.session_state.rechazar else "No se rechaza H0"
                    st.info(f"Tu app decidió: **{decision_app}**")
                    st.write("Compara con la respuesta de Gemini arriba.")

                except Exception as e:
                    st.error(f"Error al conectar con Gemini: {e}")

            

     