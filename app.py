import streamlit as st
import joblib
import os
import pandas as pd
import pydeck as pdk
import unicodedata

# 1. UTILIDADES Y MAPEOS
def normalizar(t):
    if not isinstance(t, str): return ""
    t = unicodedata.normalize('NFD', t)
    return "".join([c for c in t if unicodedata.category(c) != 'Mn']).lower().strip()

COORDS = {
    'coruna': [43.36, -8.41], 'alava': [42.84, -2.67], 'albacete': [38.99, -1.85], 'alicante': [38.34, -0.48],
    'almeria': [36.83, -2.46], 'asturias': [43.36, -5.84], 'avila': [40.65, -4.69], 'badajoz': [38.87, -6.97],
    'balears': [39.56, 2.65], 'barcelona': [41.38, 2.17], 'burgos': [42.34, -3.70], 'caceres': [39.47, -6.37],
    'cadiz': [36.52, -6.28], 'cantabria': [43.46, -3.80], 'castellon': [39.98, -0.05], 'ciudad real': [38.98, -3.92],
    'cordoba': [37.88, -4.77], 'cuenca': [40.07, -2.13], 'girona': [41.97, 2.82], 'granada': [37.17, -3.59],
    'guadalajara': [40.63, -3.16], 'gipuzkoa': [43.31, -1.98], 'huelva': [37.26, -6.94], 'huesca': [42.13, -0.40],
    'jaen': [37.76, -3.78], 'leon': [42.59, -5.56], 'lleida': [41.61, 0.62], 'lugo': [43.01, -7.55],
    'madrid': [40.41, -3.70], 'malaga': [36.72, -4.42], 'murcia': [37.99, -1.13], 'navarra': [42.81, -1.64],
    'ourense': [42.33, -7.86], 'palencia': [42.01, -4.52], 'palmas': [28.12, -15.43], 'pontevedra': [42.43, -8.64],
    'rioja': [42.46, -2.44], 'salamanca': [40.97, -5.66], 'tenerife': [28.46, -16.25], 'segovia': [40.94, -4.11],
    'sevilla': [37.38, -5.98], 'soria': [41.76, -2.33], 'tarragona': [41.11, 1.24], 'teruel': [40.34, -1.10],
    'toledo': [39.86, -4.02], 'valencia': [39.46, -0.37], 'valladolid': [41.65, -4.72], 'bizkaia': [43.26, -2.93],
    'zamora': [41.50, -5.74], 'zaragoza': [41.64, -0.88], 'ceuta': [35.88, -5.31], 'melilla': [35.29, -2.93]
}

NOMBRES_TRIBUS = {
    1: "Tribu 1: Hubs Globales",
    2: "Tribu 2: Estabilidad Tradicional",
    3: "Tribu 3: Ejes Regionales Emergentes",
    4: "Tribu 4: Élite del Sol"
}

# 2. CONFIGURACIÓN UI
st.set_page_config(
    page_title="TIMI", 
    page_icon="logo_timi.png", 
    layout="centered"
)

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; max-width: 480px !important; }
    header { visibility: hidden; }
    .stSlider { margin-top: -10px !important; }
    .precio-final { background-color: #f0f7ff; padding: 20px; border-radius: 10px; border: 2px solid #1a3a5a; text-align: center; margin-top: 15px; }
    .footer { text-align: center; color: #666; font-size: 11px; margin-top: 40px; border-top: 1px solid #eee; padding-top: 20px; }
    .tribu-box { background-color: #e8f4f8; padding: 10px; border-radius: 5px; color: #005a87; font-weight: bold; font-size: 14px; margin-bottom: 15px; text-align: center;}
    </style>
    """, unsafe_allow_html=True)

# CARGA ASSETS
ruta_base = os.path.dirname(__file__)
@st.cache_resource
def load_assets():
    try:
        m = joblib.load(os.path.join(ruta_base, 'modelo_precio_suelo.pkl'))
        s = joblib.load(os.path.join(ruta_base, 'escalador_datos.pkl'))
        d = pd.read_csv(os.path.join(ruta_base, 'df_prov_mean.csv'))
        return m, s, d
    except: return None, None, None

rf, scaler, df_ref = load_assets()

# 3. INTERFAZ PRINCIPAL
col_head1, col_head2 = st.columns([4, 1])

with col_head1:
    st.title("TIMI")
    st.markdown("<h3 style='margin-top:-20px; color: #1a3a5a; font-size: 20px;'>Tool for Intelligent Market Inference</h3>", unsafe_allow_html=True)
    st.caption("Sistema Avanzado de Inferencia Demográfica e Inteligencia Inmobiliaria")

with col_head2:
    ruta_logo = os.path.join(ruta_base, 'logo_timi.png')
    if os.path.exists(ruta_logo):
        st.image(ruta_logo, use_container_width=True)
    else:
        st.write("")

st.markdown("---")

if df_ref is not None:
    lista_prov = sorted(df_ref['PROV'].unique().tolist(), key=normalizar)
    prov_sel = st.selectbox("📍 Seleccione provincia", lista_prov)

    r = df_ref[df_ref['PROV'] == prov_sel].iloc[0]
    v_cluster = int(r.get('CLUSTER_RAW', 2))
    nombre_tribu = NOMBRES_TRIBUS.get(v_cluster, "Tribu Desconocida")

    st.markdown(f'<div class="tribu-box">{nombre_tribu}</div>', unsafe_allow_html=True)

    # 4. MAPA
    centro = [40.41, -3.70]
    prov_norm = normalizar(prov_sel)
    for k, v in COORDS.items():
        if k in prov_norm or prov_norm in k: centro = v; break
    
    st.pydeck_chart(pdk.Deck(
        map_style='road',
        initial_view_state=pdk.ViewState(latitude=centro[0], longitude=centro[1], zoom=7.5),
        layers=[pdk.Layer("ScatterplotLayer", data=pd.DataFrame({'lat':[centro[0]], 'lon':[centro[1]]}), 
                get_position='[lon, lat]', get_color='[200, 30, 0, 160]', get_radius=7000)],
        height=120 
    ))

    st.markdown("---")
    st.subheader("⚙️ Simulación de Escenarios")
    st.caption("Ajuste la variación porcentual sobre los datos reales actuales.")

    def crear_input_simulacion(label, val_base, key_suffix, unidad="%"):
        st.markdown(f"**{label}**")
        
        delta = st.slider(
            label, 
            -50, 50, 0, 
            format="%d%%", 
            key=f"s_{prov_sel}_{key_suffix}",
            label_visibility="collapsed"
        )
        
        val_final = float(val_base * (1 + delta/100))
        
        st.markdown(f"""
            <div style="margin-top: -15px; margin-bottom: 35px; border-bottom: 1px solid #f0f2f6; padding-bottom: 10px;">
                <span style="font-size: 14px; color: #666;">Base: {val_base:.2f}{unidad}</span>
                <span style="font-size: 14px; color: #1a3a5a; font-weight: bold; margin-left: 20px;">
                    → Simulado: {val_final:.2f}{unidad}
                </span>
            </div>
        """, unsafe_allow_html=True)
        
        return val_final

    v1 = crear_input_simulacion("Crecimiento General de la Población", r['VAR_ANUAL_POB'], "pob")
    v2 = crear_input_simulacion("Población Senior (>60 años)", r['PORC_60_MAS'], "sen")
    v3 = crear_input_simulacion("Población en Edad de Demanda (25-49 años)", r['PORC_EDAD_DEMANDA'], "dem")
    v4 = crear_input_simulacion("Extranjeros Europeos", r['PORC_EUROPEOS_NO_ESP'], "eur")
    v5 = crear_input_simulacion("Resto de Extranjeros", r['PORC_RESTO_EXTRANJEROS'], "ext")
    v6 = crear_input_simulacion("Densidad de Vivienda (nº de compraventas por cada 1.000 hab.)", r['INTENSIDAD_VIV'], "den", unidad="")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("CALCULAR IMPACTO EN PRECIO", type="primary", use_container_width=True):
        input_vector = [[v1, v2, v3, v4, v5, v6, v_cluster]]
        scaled_input = scaler.transform(input_vector)
        pred = rf.predict(scaled_input)[0]
        
        precio_base = r['PRECIO_M2']
        dif_percent = ((pred - precio_base) / precio_base) * 100
        color_dif = "#28a745" if dif_percent >= 0 else "#dc3545"
        signo = "+" if dif_percent >= 0 else ""

        st.markdown(f"""
            <div class="precio-final">
                <p style="margin:0; color:#1a3a5a; font-weight:bold; font-size:13px;">PRECIO ESTIMADO DEL SUELO</p>
                <h1 style="margin:0; color:#1a3a5a; font-size:32px;">{pred:,.2f} €/m²</h1>
                <p style="margin:0; color:{color_dif}; font-weight:bold; font-size:14px;">
                    {signo}{dif_percent:.2f}% respecto al valor actual
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="footer">
            <b>Ignacio Alonso De Vaya</b><br>
            TFM MAGABI26 | TIMI<br>
            <i>Modelización basada en Random Forest | Datos Recientes 2020-2025</i>
        </div>
    """, unsafe_allow_html=True)
