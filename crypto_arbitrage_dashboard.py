# Dashboard Interactivo para Análisis de Arbitraje en Criptomonedas
# Ejecutar con: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Arbitraje en Criptomonedas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título y descripción
st.title("📊 Análisis de Arbitraje y Microestructura de Mercado en Criptomonedas")
st.markdown("""
Este dashboard presenta un análisis detallado de las oportunidades de arbitraje entre diferentes 
exchanges (Binance, Coinbase, Kucoin y OKX) para Bitcoin (BTC), Ethereum (ETH) y Ripple (XRP).
""")

# Funciones auxiliares para cargar datos
@st.cache_data
def load_data():
    """Carga todos los datasets procesados"""
    data = {}
    
    # Resúmenes de arbitraje
    try:
        if os.path.exists('data/comparative/combined_arbitrage_summary.csv'):
            data['combined_summary'] = pd.read_csv('data/comparative/combined_arbitrage_summary.csv')
        else:
            # Cargar individualmente si no existe el combinado
            summaries = []
            for crypto in ['btc', 'eth', 'xrp']:
                if os.path.exists(f'data/processed/{crypto}_arbitrage_summary.csv'):
                    df = pd.read_csv(f'data/processed/{crypto}_arbitrage_summary.csv')
                    df['cryptocurrency'] = crypto.upper()
                    summaries.append(df)
            
            if summaries:
                data['combined_summary'] = pd.concat(summaries, ignore_index=True)
    except Exception as e:
        st.error(f"Error al cargar resúmenes de arbitraje: {e}")
    
    # Datos de arbitraje detallados
    for crypto in ['btc', 'eth', 'xrp']:
        try:
            if os.path.exists(f'data/processed/{crypto}_arbitrage.csv'):
                df = pd.read_csv(f'data/processed/{crypto}_arbitrage.csv')
                # Convertir timestamp a datetime si existe
                if 'timestamp' in df.columns: