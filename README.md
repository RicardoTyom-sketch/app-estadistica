# App Estadística con IA 

Aplicación interactiva desarrollada en Streamlit que permite visualizar distribuciones estadísticas, realizar pruebas de hipótesis Z e interpretar resultados con inteligencia artificial mediante la API de Google Gemini.

## Módulos

- **Carga de Datos** — Sube un CSV o genera datos sintéticos
- **Visualización** — Histograma, KDE, Boxplot y análisis de distribución
- **Prueba Z** — Prueba de hipótesis con región crítica y curva
- **Asistente IA** — Interpretación de resultados con Gemini

## Requisitos

- Python 3.9+
- Streamlit
- Pandas, Numpy, Scipy
- Matplotlib, Seaborn
- Google Generative AI

## Cómo ejecutar

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

## Configuración

Crea un archivo `.env` con tu API key de Gemini:

```
GEMINI_API_KEY=tu_api_key
```