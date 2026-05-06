# TIMI-TFM
# TIMI: Tool for Intelligent Market Inference 

**TIMI** es una herramienta avanzada de inteligencia de mercado desarrollada como Trabajo de Fin de Máster (TFM) para el programa **MAGABI26**. La aplicación utiliza modelos de Machine Learning para cuantificar el impacto de las variables demográficas en el precio del suelo de las 52 provincias españolas.

## Propósito del Proyecto
El objetivo principal de TIMI es aislar el componente social y demográfico del ruido puramente especulativo del mercado inmobiliario. Responde a la pregunta: *¿Cuánto del valor de una zona depende realmente de quién vive en ella?*

## Stack Tecnológico
*   **Lenguaje:** Python 3.9+
*   **Framework de Interfaz:** [Streamlit](https://streamlit.io/)
*   **Machine Learning:** Scikit-learn (Random Forest Regressor)
*   **Visualización Geoespacial:** Pydeck
*   **Infraestructura:** Oracle Cloud Infrastructure (OCI) para la ingesta de datos y Streamlit Cloud para el despliegue.

## Características Principales
*   **Segmentación por "Tribus":** Clasificación del mercado español en 4 clústeres estratégicos basados en ADN geodemográfico.
*   **Simulador de Escenarios:** Test de estrés que permite variar flujos migratorios, envejecimiento y demanda joven en un rango de ±50%.
*   **Inferencia en Tiempo Real:** Cálculo instantáneo del impacto en el precio (€/m²) y su variación porcentual respecto al valor real de mercado.
*   **Arquitectura MLOps:** Pipeline de datos diseñado para evitar el *data leakage* y garantizar la reproducibilidad.

## Estructura del Repositorio
*   `app.py`: Código fuente de la aplicación Streamlit.
*   `modelo_precio_suelo.pkl`: Modelo Random Forest entrenado.
*   `escalador_datos.pkl`: Escalador StandardScaler para la normalización de inputs.
*   `df_prov_mean.csv`: Base de datos de referencia con promedios provinciales (2020-2025).
*   `requirements.txt`: Dependencias necesarias para la ejecución en la nube.
*   `logo_timi.png`: Identidad visual del proyecto.

## Instalación Local
Si deseas ejecutar TIMI en tu entorno local:

*  **1. Clonar el repositorio:**
   ```bash
   git clone [https://github.com/ialonsodv/TIMI-TFM.git](https://github.com/ialonsodv/TIMI-TFM.git)
*  **2. Instalar dependencias:**
   Bash
   pip install -r requirements.txt
*  **3. Lanzar la aplicación:**
   Bash
   streamlit run app.py

**Autor**: Ignacio Alonso De Vaya
**Máster**: MAGABI26 - Instituto de Estudios Cajasol
**Fecha**: Mayo 2026
