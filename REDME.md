# Análisis de Arbitraje en Criptomonedas

## Descripción
Este proyecto analiza las oportunidades de arbitraje entre diferentes exchanges de criptomonedas (Binance, Coinbase, Kucoin y OKX) para Bitcoin (BTC), Ethereum (ETH) y Ripple (XRP). El análisis se basa en datos históricos de precios con intervalos de 1 minuto recopilados entre 2017 y 2019.

## Objetivos
- Identificar y cuantificar oportunidades de arbitraje entre exchanges
- Determinar qué criptomoneda y par de exchanges ofrecen las mejores oportunidades
- Analizar los patrones de spread entre diferentes plataformas
- Desarrollar un dashboard interactivo para visualizar los resultados

## Características del proyecto
- Análisis de más de 4 millones de registros de precios
- Comparativa entre BTC, ETH y XRP
- Dashboard interactivo desarrollado con Streamlit
- Simulador de estrategias de arbitraje

## Hallazgos clave
- Ethereum presenta el mayor porcentaje de oportunidades (28.63%)
- Bitcoin muestra los spreads más extremos (hasta 48.51%)
- El par Coinbase-Kucoin resultó óptimo para ETH y XRP, mientras que Kucoin-OKX fue el mejor para BTC

## Estructura del repositorio
- **data/processed/**: Contiene los datos procesados y resumidos
- **visualizations/**: Contiene las visualizaciones generadas
- **notebooks/**: Notebooks de análisis
- **dashboard.py**: Código del dashboard interactivo de Streamlit

## Cómo ejecutar el dashboard
1. Instala las dependencias: `pip install streamlit pandas plotly`
2. Ejecuta el dashboard: `streamlit run dashboard.py`

## Autor
OldManJonny
