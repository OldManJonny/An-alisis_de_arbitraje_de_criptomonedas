import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import os

# Configuración de la página
st.set_page_config(
    page_title="Análisis de Arbitraje en Criptomonedas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Función para cargar datos
@st.cache_data
def load_data():
    # Obtener la ruta del directorio base del proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construir las rutas a los archivos
    crypto_summary_path = os.path.join(base_dir, 'data', 'processed', 'crypto_summary.csv')
    combined_arbitrage_path = os.path.join(base_dir, 'data', 'processed', 'combined_arbitrage_summary.csv')
    best_pairs_path = os.path.join(base_dir, 'data', 'processed', 'best_pairs_by_crypto.csv')
    
    # Cargar los archivos
    try:
        crypto_summary = pd.read_csv(crypto_summary_path)
        combined_arbitrage = pd.read_csv(combined_arbitrage_path)
        best_pairs = pd.read_csv(best_pairs_path)
        return crypto_summary, combined_arbitrage, best_pairs
    except FileNotFoundError as e:
        # Alternativa: intentar cargar desde rutas relativas
        try:
            crypto_summary = pd.read_csv('data/processed/crypto_summary.csv')
            combined_arbitrage = pd.read_csv('data/processed/combined_arbitrage_summary.csv')
            best_pairs = pd.read_csv('data/processed/best_pairs_by_crypto.csv')
            return crypto_summary, combined_arbitrage, best_pairs
        except FileNotFoundError:
            st.error(f"No se pudieron encontrar los archivos CSV necesarios. Error: {e}")
            st.info(f"Buscando en: {crypto_summary_path}")
            st.info(f"Directorios disponibles: {os.listdir(base_dir)}")
            raise

# Cargar los datos
crypto_summary, combined_arbitrage, best_pairs = load_data()

# Funciones auxiliares
def get_pairs_for_crypto(df, crypto):
    return df[df['cryptocurrency'] == crypto]

def create_opportunity_chart(df, crypto):
    filtered_df = get_pairs_for_crypto(df, crypto)
    fig = px.bar(
        filtered_df.sort_values('Oportunidades', ascending=False),
        x='Par',
        y='Oportunidades',
        color='Spread Promedio',
        color_continuous_scale='Viridis',
        title=f'Oportunidades de Arbitraje para {crypto} por Par de Exchanges',
        labels={'Par': 'Par de Exchanges', 'Oportunidades': 'Número de Oportunidades'},
        height=500
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def create_spread_chart(df, crypto):
    filtered_df = get_pairs_for_crypto(df, crypto)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Añadir barras para Spread Promedio
    fig.add_trace(
        go.Bar(
            x=filtered_df['Par'],
            y=filtered_df['Spread Promedio'],
            name='Spread Promedio (%)',
            marker_color='rgb(55, 83, 109)'
        ),
        secondary_y=False,
    )
    
    # Añadir línea para Spread Máximo
    fig.add_trace(
        go.Scatter(
            x=filtered_df['Par'],
            y=filtered_df['Spread Máximo'],
            name='Spread Máximo (%)',
            line=dict(color='firebrick', width=3)
        ),
        secondary_y=True,
    )
    
    # Actualizar diseño
    fig.update_layout(
        title_text=f'Análisis de Spread para {crypto} por Par de Exchanges',
        xaxis_tickangle=-45,
        height=500
    )
    
    # Establecer títulos de los ejes
    fig.update_yaxes(title_text="Spread Promedio (%)", secondary_y=False)
    fig.update_yaxes(title_text="Spread Máximo (%)", secondary_y=True)
    
    return fig

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: #C9E4CA' if v else '' for v in is_max]

# Diccionario con las URLs de las imágenes para cada criptomoneda
crypto_images = {
    "BTC": "https://img.freepik.com/free-vector/cryptocurrency-bitcoin-golden-coin-background_1017-31505.jpg",
    "ETH": "https://e0.pxfuel.com/wallpapers/841/579/desktop-wallpaper-ethereum-eth-logo-zoom-animated-background.jpg",
    "XRP": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRQHnptiXWAMjV29ASP0YIGHBXAKDO07fOaAQ&s"
}

# Sidebar
st.sidebar.title("Análisis de Arbitraje en Criptomonedas")
st.sidebar.markdown("""
Explora oportunidades de arbitraje entre diferentes exchanges: 
**Binance, Coinbase, KuCoin y ORK**.
""")

# Selector de criptomoneda
selected_crypto = st.sidebar.selectbox(
    "Selecciona una Criptomoneda",
    options=crypto_summary['cryptocurrency'].unique(),
    index=0  # Default a BTC
)

# Mostrar la imagen correspondiente a la criptomoneda seleccionada
st.sidebar.image(crypto_images[selected_crypto], width=300)

# Explicación del arbitraje
with st.sidebar.expander("¿Qué es el Arbitraje?"):
    st.markdown("""
    El **arbitraje** en criptomonedas es una estrategia de trading que aprovecha las diferencias de precio 
    de un mismo activo entre diferentes mercados o exchanges. 
    
    Los traders compran la criptomoneda en el exchange donde está más barata y la venden 
    inmediatamente en otro exchange donde su precio es mayor, obteniendo un beneficio por la diferencia.
    
    **Spread**: Es la diferencia porcentual entre el precio en un exchange y otro.
    """)

# Indicadores principales
st.title(f"📊 Dashboard de Arbitraje: {selected_crypto}")

# Fila de métricas clave
best_pair_data = best_pairs[best_pairs['cryptocurrency'] == selected_crypto].iloc[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Mejor Par por Oportunidades", 
        best_pair_data['best_pair_by_opportunities'],
        f"{best_pair_data['max_opportunities']} oportunidades"
    )
with col2:
    st.metric(
        "Mejor Par por Spread Promedio", 
        best_pair_data['best_pair_by_avg_spread'],
        f"{best_pair_data['max_avg_spread']:.2f}%"
    )
with col3:
    st.metric(
        "Mejor Par por Spread Máximo", 
        best_pair_data['best_pair_by_max_spread'],
        f"{best_pair_data['absolute_max_spread']:.2f}%"
    )

# Comparativa general de criptomonedas
st.header("Comparativa General de Criptomonedas")
st.markdown("""
Este gráfico muestra un resumen comparativo de las oportunidades de arbitraje para BTC, ETH y XRP,
considerando el número total de oportunidades y el spread promedio observado.
""")

# Gráfico de burbujas para comparar criptomonedas
fig_bubble = px.scatter(
    crypto_summary,
    x="Oportunidades",
    y="Spread Promedio",
    size="Spread Máximo",
    color="cryptocurrency",
    hover_name="cryptocurrency",
    size_max=60,
    title="Comparativa de Oportunidades y Spread por Criptomoneda",
    labels={
        "Oportunidades": "Número de Oportunidades",
        "Spread Promedio": "Spread Promedio (%)",
        "Spread Máximo": "Spread Máximo (%)",
        "cryptocurrency": "Criptomoneda"
    },
    height=500
)
st.plotly_chart(fig_bubble, use_container_width=True)

# Sección de análisis detallado para la criptomoneda seleccionada
st.header(f"Análisis Detallado: {selected_crypto}")

# Dividir en pestañas
tab1, tab2, tab3 = st.tabs(["Oportunidades", "Análisis de Spread", "Datos Detallados"])

with tab1:
    st.markdown(f"""
    Este gráfico muestra el número de oportunidades de arbitraje detectadas para {selected_crypto} en cada par de exchanges.
    Los colores representan el spread promedio, donde tonos más oscuros indican mayor spread.
    """)
    fig_opps = create_opportunity_chart(combined_arbitrage, selected_crypto)
    st.plotly_chart(fig_opps, use_container_width=True)

with tab2:
    st.markdown(f"""
    Comparación entre el spread promedio (barras) y el spread máximo (línea) para {selected_crypto} en cada par de exchanges.
    Un mayor spread indica mayores oportunidades de beneficio.
    """)
    fig_spread = create_spread_chart(combined_arbitrage, selected_crypto)
    st.plotly_chart(fig_spread, use_container_width=True)

with tab3:
    st.markdown(f"""
    Tabla detallada con todas las métricas para {selected_crypto}. Las celdas destacadas muestran los valores máximos para cada columna.
    """)
    filtered_data = get_pairs_for_crypto(combined_arbitrage, selected_crypto)
    styled_df = filtered_data.style.apply(highlight_max, subset=['Oportunidades', 'Porcentaje', 'Spread Promedio', 'Spread Máximo'])
    st.dataframe(styled_df, use_container_width=True)

# Sección de análisis estratégico
st.header("Análisis Estratégico de Arbitraje")

# Crear un heatmap de pares de exchanges para la criptomoneda seleccionada
crypto_pairs = get_pairs_for_crypto(combined_arbitrage, selected_crypto)

# Crear una matriz para el heatmap
exchanges = set()
for pair in crypto_pairs['Par']:
    ex1, ex2 = pair.split('-')
    exchanges.add(ex1)
    exchanges.add(ex2)

exchanges = sorted(list(exchanges))
n = len(exchanges)
matrix = np.zeros((n, n))

# Rellenar la matriz con datos de spread promedio
for _, row in crypto_pairs.iterrows():
    ex1, ex2 = row['Par'].split('-')
    i = exchanges.index(ex1)
    j = exchanges.index(ex2)
    matrix[i][j] = row['Spread Promedio']
    matrix[j][i] = row['Spread Promedio']  # Hacerlo simétrico

# Crear heatmap
fig_heatmap = go.Figure(data=go.Heatmap(
    z=matrix,
    x=exchanges,
    y=exchanges,
    colorscale='Viridis',
    colorbar=dict(title='Spread Promedio (%)'),
))

fig_heatmap.update_layout(
    title=f'Heatmap de Spread Promedio entre Exchanges para {selected_crypto}',
    height=600
)

st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("""
El heatmap anterior muestra visualmente qué pares de exchanges ofrecen mejores oportunidades de arbitraje 
basándose en el spread promedio. Los colores más intensos indican mayor spread y, por tanto, 
potencialmente mejores oportunidades de beneficio.
""")

# Sección de simulador de estrategias
st.header("Simulador de Estrategias de Arbitraje")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Parámetros de la Estrategia")
    
    capital_inicial = st.number_input("Capital Inicial (USD)", min_value=100, max_value=100000, value=1000, step=100)
    comision = st.slider("Comisión por Operación (%)", min_value=0.0, max_value=1.0, value=0.1, step=0.05)
    tiempo_transaccion = st.slider("Tiempo de Transacción (minutos)", min_value=1, max_value=60, value=10, step=1)
    umbral_spread = st.slider("Umbral Mínimo de Spread (%)", min_value=0.1, max_value=5.0, value=0.5, step=0.1)
    
    # Botón para simular
    simulate = st.button("Simular Estrategia")

with col2:
    st.subheader("Resultados de la Simulación")
    
    if simulate:
        # Filtrar oportunidades que cumplan con el umbral
        valid_opportunities = crypto_pairs[crypto_pairs['Spread Promedio'] >= umbral_spread]
        num_valid_opps = len(valid_opportunities)
        
        # Calcular métricas simuladas
        if num_valid_opps > 0:
            avg_spread_valid = valid_opportunities['Spread Promedio'].mean()
            
            # Simulación simple
            operaciones_por_dia = (24 * 60) // tiempo_transaccion  # Número potencial de operaciones por día
            beneficio_por_op = capital_inicial * (avg_spread_valid / 100) * (1 - comision / 100)
            beneficio_diario_estimado = min(num_valid_opps, operaciones_por_dia) * beneficio_por_op
            beneficio_mensual_estimado = beneficio_diario_estimado * 30
            roi_mensual = (beneficio_mensual_estimado / capital_inicial) * 100
            
            # Mostrar resultados
            st.metric("Oportunidades Válidas", f"{num_valid_opps} de {len(crypto_pairs)}")
            st.metric("Operaciones Posibles por Día", f"{min(num_valid_opps, operaciones_por_dia)}")
            st.metric("Beneficio Diario Estimado", f"${beneficio_diario_estimado:.2f}")
            st.metric("ROI Mensual Estimado", f"{roi_mensual:.2f}%")
            
            # Advertencia
            st.warning("""
            **Nota**: Esta es una simulación simplificada y los resultados reales pueden variar debido a:
            - Volatilidad del mercado
            - Costos de transferencia entre exchanges
            - Tiempos de confirmación variables
            - Posibles slippage en las operaciones
            """)
        else:
            st.error(f"No se encontraron oportunidades que cumplan con el umbral mínimo de spread ({umbral_spread}%).")
    else:
        st.info("Ajusta los parámetros y haz clic en 'Simular Estrategia' para ver los resultados.")

# Pie de página
st.markdown("---")
st.markdown("""
Desarrollado por: John Ayala | Proyecto: Análisis de Arbitraje en Criptomonedas

Metodología: Los datos presentados en este dashboard fueron recopilados mediante el análisis de precios 
históricos en Binance, Coinbase, KuCoin y ORK para BTC, ETH y XRP. Se detectaron oportunidades de arbitraje 
cuando la diferencia de precio entre exchanges superó un umbral específico, calculando el spread resultante.
""")
