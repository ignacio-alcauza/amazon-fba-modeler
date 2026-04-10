import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import json
from datetime import datetime

st.set_page_config(
    page_title="Amazon FBA — Modelo Económico",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# DARK MODE STATE
# ─────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ─────────────────────────────────────────────
# PARÁMETROS POR DEFECTO (fuente única de verdad)
# ─────────────────────────────────────────────
DEFAULTS = {
    "p_name":               "Mi Producto",
    "p_coste_unitario":     4.50,
    "p_moq":                500,
    "p_coste_packaging":    0.30,
    "p_coste_inspeccion":   300.0,
    "p_coste_agente":       0.0,
    "p_metodo_envio":       "Marítimo",
    "p_peso_unidad":        0.45,
    "p_coste_kg":           1.20,
    "p_arancel_pct":        6.5,
    "p_despacho_fijo":      200.0,
    "p_seguro_pct":         0.50,
    "p_costes_portuarios":  150.0,
    "p_transporte_interno": 180.0,
    "p_pvp":                24.99,
    "p_comision_pct":       15.0,
    "p_coste_fba":          3.50,
    "p_almacenamiento_mes": 0.35,
    "p_devolucion_pct":     5.0,
    "p_coste_devolucion":   1.50,
    "p_cpc":                0.55,
    "p_conversion_pct":     12.0,
    "p_presupuesto_diario": 15.0,
    "p_iva_pct":            21.0,
    "p_re_pct":             5.2,
    "p_impuesto_pct":       25.0,
}

# Inicializar session_state con defaults solo la primera vez
for _k, _v in DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────
# RGBA HELPER
# ─────────────────────────────────────────────
def rgba(hex_color, alpha):
    """Convert a #rrggbb hex string to rgba(r,g,b,alpha)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

# ─────────────────────────────────────────────
# THEME VARIABLES
# ─────────────────────────────────────────────
if st.session_state.dark_mode:
    BG         = "#0f1117"
    BG2        = "#1a1d27"
    BG3        = "#22263a"
    TEXT       = "#e8eaf6"
    TEXT_MUTED = "#8892b0"
    ACCENT     = "#7c6ff7"
    ACCENT2    = "#06d6a0"
    DANGER     = "#ff6b6b"
    WARNING    = "#ffd166"
    SUCCESS    = "#06d6a0"
    PLOT_THEME = "plotly_dark"
    PLOT_BG    = "#1a1d27"
    PLOT_PAPER = "#1a1d27"
    PLOT_FONT  = "#e8eaf6"
    SIDEBAR_BG = "#13161f"
    CARD_BG    = "rgba(255,255,255,0.04)"
    CARD_BORD  = "rgba(255,255,255,0.08)"
    GRID_COLOR = "rgba(255,255,255,0.07)"
    TH_BG      = "#22263a"
    TD_BG      = "#1a1d27"
    TD_BG_ALT  = "#1e2233"
    ROW_HILITE_WARN = "rgba(255,209,102,0.18)"
    ROW_HILITE_OK   = "rgba(6,214,160,0.18)"
    ROW_HILITE_BAD  = "rgba(255,107,107,0.18)"
else:
    BG         = "#f0f2f8"
    BG2        = "#ffffff"
    BG3        = "#e8eaf4"
    TEXT       = "#1a1a2e"
    TEXT_MUTED = "#6b7280"
    ACCENT     = "#6c63ff"
    ACCENT2    = "#00c896"
    DANGER     = "#ef4444"
    WARNING    = "#f59e0b"
    SUCCESS    = "#10b981"
    PLOT_THEME = "plotly_white"
    PLOT_BG    = "#ffffff"
    PLOT_PAPER = "#f0f2f8"
    PLOT_FONT  = "#1a1a2e"
    SIDEBAR_BG = "#ffffff"
    CARD_BG    = "rgba(255,255,255,0.85)"
    CARD_BORD  = "rgba(120,120,180,0.15)"
    GRID_COLOR = "rgba(0,0,0,0.05)"
    TH_BG      = "#e8eaf4"
    TD_BG      = "#ffffff"
    TD_BG_ALT  = "#f7f8fc"
    ROW_HILITE_WARN = "rgba(245,158,11,0.15)"
    ROW_HILITE_OK   = "rgba(16,185,129,0.15)"
    ROW_HILITE_BAD  = "rgba(239,68,68,0.15)"

# ─────────────────────────────────────────────
# HTML TABLE HELPER  (replaces st.dataframe)
# ─────────────────────────────────────────────
def html_table(rows: list[dict], highlight: dict | None = None) -> str:
    """
    Render a list-of-dicts as a styled HTML table that respects the current theme.
    highlight: {row_index: 'warn'|'ok'|'bad'|'bold'}
    """
    hl_map = {
        "warn": ROW_HILITE_WARN,
        "ok":   ROW_HILITE_OK,
        "bad":  ROW_HILITE_BAD,
    }
    if not rows:
        return ""
    cols = list(rows[0].keys())
    th_style = (
        f"padding:9px 14px; text-align:left; font-size:0.76rem; font-weight:800;"
        f"text-transform:uppercase; letter-spacing:0.07em;"
        f"color:{TEXT_MUTED}; background:{TH_BG}; border-bottom:2px solid {CARD_BORD};"
    )
    header = "".join(f"<th style='{th_style}'>{c}</th>" for c in cols)

    body_rows = []
    for i, row in enumerate(rows):
        bg = TD_BG if i % 2 == 0 else TD_BG_ALT
        fw = "normal"
        if highlight and i in highlight:
            h = highlight[i]
            if h in hl_map:
                bg = hl_map[h]
            fw = "700"
        td_style = (
            f"padding:8px 14px; font-size:0.9rem; font-weight:{fw};"
            f"color:{TEXT}; background:{bg}; border-bottom:1px solid {CARD_BORD};"
        )
        cells = "".join(f"<td style='{td_style}'>{row[c]}</td>" for c in cols)
        body_rows.append(f"<tr>{cells}</tr>")

    table_style = (
        f"width:100%; border-collapse:collapse; border-radius:14px; overflow:hidden;"
        f"font-family:'Nunito',sans-serif; box-shadow:0 2px 16px {rgba(ACCENT,0.08)};"
    )
    wrapper_style = (
        f"border-radius:14px; overflow:hidden; border:1px solid {CARD_BORD};"
        f"margin-bottom:12px;"
    )
    return (
        f"<div style='{wrapper_style}'>"
        f"<table style='{table_style}'>"
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        f"</table></div>"
    )

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap');

  html, body, [class*="css"], .stApp, .stMarkdown, .stMetric,
  button, input, label, p, span, div {{
    font-family: 'Nunito', sans-serif !important;
  }}

  .stApp {{
    background: {BG} !important;
    transition: background 0.35s ease;
  }}
  .stApp > header {{ background: transparent !important; }}

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {{
    background: {SIDEBAR_BG} !important;
    border-right: 1px solid {CARD_BORD};
    box-shadow: 4px 0 24px {rgba("#000000", 0.08)};
  }}
  [data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

  /* ── Slider ── */
  [data-testid="stSlider"] > div > div > div > div {{
    background: linear-gradient(90deg, {ACCENT}, {ACCENT2}) !important;
    border-radius: 99px;
  }}
  [data-testid="stSlider"] [role="slider"] {{
    background: {BG2} !important;
    border: 3px solid {ACCENT} !important;
    box-shadow: 0 0 0 4px {rgba(ACCENT, 0.2)} !important;
    transition: box-shadow 0.2s ease;
  }}
  [data-testid="stSlider"] [role="slider"]:hover {{
    box-shadow: 0 0 0 8px {rgba(ACCENT, 0.28)} !important;
  }}
  [data-testid="stSlider"] label {{
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    color: {TEXT_MUTED} !important;
    letter-spacing: 0.01em;
  }}

  /* ── Expander ── */
  [data-testid="stExpander"] {{
    background: {CARD_BG} !important;
    border: 1px solid {CARD_BORD} !important;
    border-radius: 14px !important;
    margin-bottom: 10px !important;
    backdrop-filter: blur(12px);
    transition: box-shadow 0.2s ease;
  }}
  [data-testid="stExpander"]:hover {{
    box-shadow: 0 4px 20px {rgba(ACCENT, 0.13)};
  }}
  [data-testid="stExpander"] summary {{
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    color: {TEXT} !important;
    padding: 10px 14px !important;
  }}

  /* ── Tabs ── */
  [data-testid="stTabs"] [role="tablist"] {{
    gap: 6px;
    background: {BG3};
    padding: 6px;
    border-radius: 16px;
    border: none;
  }}
  [data-testid="stTabs"] [role="tab"] {{
    border-radius: 12px !important;
    font-size: 0.88rem !important;
    font-weight: 700 !important;
    color: {TEXT_MUTED} !important;
    padding: 8px 18px !important;
    border: none !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
  }}
  [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
    background: {ACCENT} !important;
    color: white !important;
    box-shadow: 0 4px 14px {rgba(ACCENT, 0.4)} !important;
  }}
  [data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]) {{
    background: {CARD_BG} !important;
    color: {TEXT} !important;
  }}
  [data-testid="stTabs"] [role="tabpanel"] {{
    padding-top: 20px !important;
  }}

  /* ── Metrics ── */
  [data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORD};
    border-radius: 16px;
    padding: 18px 20px !important;
    backdrop-filter: blur(12px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }}
  [data-testid="stMetric"]:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px {rgba("#000000", 0.12)};
  }}
  [data-testid="stMetric"] label {{
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: {TEXT_MUTED} !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }}
  [data-testid="stMetric"] [data-testid="stMetricValue"] {{
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: {TEXT} !important;
    line-height: 1.1;
  }}
  [data-testid="stMetric"] [data-testid="stMetricDelta"] {{
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: {TEXT_MUTED} !important;
  }}

  /* ── Buttons (toda la app) ── */
  button[kind="secondary"],
  button[kind="primary"],
  [data-testid="stBaseButton-secondary"] button,
  [data-testid="stBaseButton-primary"] button,
  [data-testid="stDownloadButton"] button,
  .stButton > button,
  .stDownloadButton > button {{
    background: {ACCENT} !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    font-family: 'Nunito', sans-serif !important;
    padding: 8px 16px !important;
    cursor: pointer !important;
    transition: opacity 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 3px 12px {rgba(ACCENT, 0.35)} !important;
  }}
  .stButton > button:hover,
  .stDownloadButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px {rgba(ACCENT, 0.45)} !important;
  }}

  /* ── Text inputs ── */
  [data-testid="stTextInput"] input {{
    background: {BG2} !important;
    color: {TEXT} !important;
    border: 1px solid {CARD_BORD} !important;
    border-radius: 10px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    padding: 8px 12px !important;
  }}
  [data-testid="stTextInput"] input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {rgba(ACCENT, 0.2)} !important;
    outline: none !important;
  }}
  [data-testid="stTextInput"] label {{
    color: {TEXT_MUTED} !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
  }}

  /* ── File uploader (toda la app) ── */
  [data-testid="stFileUploader"] {{
    background: {BG2} !important;
    border: 2px dashed {CARD_BORD} !important;
    border-radius: 12px !important;
    padding: 4px 8px !important;
  }}
  [data-testid="stFileUploaderDropzone"] {{
    background: transparent !important;
  }}
  [data-testid="stFileUploader"] label,
  [data-testid="stFileUploader"] span,
  [data-testid="stFileUploader"] p,
  [data-testid="stFileUploader"] small {{
    color: {TEXT} !important;
    font-family: 'Nunito', sans-serif !important;
  }}
  [data-testid="stFileUploaderDropzone"] button {{
    background: {CARD_BG} !important;
    color: {ACCENT} !important;
    border: 1px solid {ACCENT} !important;
    box-shadow: none !important;
  }}

  /* ── Alerts ── */
  [data-testid="stAlert"] {{
    border-radius: 14px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border: none !important;
  }}

  /* ── Progress bar ── */
  [data-testid="stProgressBar"] > div > div {{
    background: linear-gradient(90deg, {ACCENT}, {ACCENT2}) !important;
    border-radius: 99px !important;
  }}
  [data-testid="stProgressBar"] > div {{
    background: {BG3} !important;
    border-radius: 99px !important;
  }}

  /* ── General text ── */
  hr {{ border-color: {CARD_BORD} !important; margin: 20px 0 !important; }}
  h1 {{ font-size:2rem !important; font-weight:800 !important; color:{TEXT} !important; }}
  h2 {{ font-size:1.5rem !important; font-weight:700 !important; color:{TEXT} !important; }}
  h3 {{ font-size:1.2rem !important; font-weight:700 !important; color:{TEXT} !important; }}
  h4 {{ font-size:1rem !important; font-weight:700 !important; color:{TEXT} !important; }}
  p, span {{ color:{TEXT} !important; font-size:0.95rem !important; }}

  [data-testid="stSelectbox"] > div > div {{
    background: {CARD_BG} !important;
    border: 1px solid {CARD_BORD} !important;
    border-radius: 10px !important;
    color: {TEXT} !important;
  }}

  /* ── Badges / pills ── */
  .badge-green  {{ display:inline-block; padding:2px 10px; border-radius:99px;
                   background:{rgba(SUCCESS,0.18)}; color:{SUCCESS};
                   font-weight:700; font-size:0.78rem; }}
  .badge-yellow {{ display:inline-block; padding:2px 10px; border-radius:99px;
                   background:{rgba(WARNING,0.18)}; color:{WARNING};
                   font-weight:700; font-size:0.78rem; }}
  .badge-red    {{ display:inline-block; padding:2px 10px; border-radius:99px;
                   background:{rgba(DANGER,0.18)}; color:{DANGER};
                   font-weight:700; font-size:0.78rem; }}

  .section-label {{
    font-size:0.72rem; font-weight:800; text-transform:uppercase;
    letter-spacing:0.1em; color:{ACCENT}; margin-bottom:8px; margin-top:6px;
  }}
  .header-title {{
    font-size:1.9rem; font-weight:800;
    background: linear-gradient(135deg, {ACCENT}, {ACCENT2});
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; line-height:1.2;
  }}
  .header-sub {{ font-size:0.88rem; color:{TEXT_MUTED}; margin-top:2px; font-weight:500; }}

  ::-webkit-scrollbar {{ width:6px; height:6px; }}
  ::-webkit-scrollbar-track {{ background:{BG}; }}
  ::-webkit-scrollbar-thumb {{ background:{rgba(ACCENT,0.4)}; border-radius:99px; }}
  ::-webkit-scrollbar-thumb:hover {{ background:{ACCENT}; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER + DARK MODE TOGGLE
# ─────────────────────────────────────────────
col_title, col_toggle = st.columns([5, 1])
with col_title:
    product_name = st.session_state.get("p_name", "Mi Producto")
    st.markdown(f"""
    <div style="padding-bottom:12px">
      <div class="header-title">📦 Amazon FBA Modeler</div>
      <div class="header-sub">
        Análisis de viabilidad · Importación desde China · Tiempo real
        &nbsp;·&nbsp;
        <span style="font-weight:800;color:{ACCENT}">{product_name}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
with col_toggle:
    st.markdown("<div style='padding-top:14px'></div>", unsafe_allow_html=True)
    dark = st.toggle("🌙 Dark", value=st.session_state.dark_mode, key="dark_toggle")
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.rerun()

# ─────────────────────────────────────────────
# BARRA GUARDAR / CARGAR — visible en contenido principal
# ─────────────────────────────────────────────
def build_export():
    params = {k: st.session_state[k] for k in DEFAULTS if k != "p_name"}
    return json.dumps({
        "product_name": st.session_state["p_name"],
        "version": "1.0",
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "params": params,
    }, indent=2, ensure_ascii=False).encode("utf-8")

with st.container():
    st.markdown(
        f"<div style='background:{CARD_BG};border:1px solid {CARD_BORD};border-radius:14px;"
        f"padding:14px 20px;margin-bottom:16px;display:flex;align-items:center;gap:12px'>",
        unsafe_allow_html=True,
    )
    bar_c1, bar_c2, bar_c3, bar_c4 = st.columns([3, 2, 2, 3])

    with bar_c1:
        st.text_input("📦 Nombre del producto", key="p_name", label_visibility="visible")

    with bar_c2:
        st.markdown("<div style='padding-top:28px'></div>", unsafe_allow_html=True)
        filename = f"{(st.session_state.get('p_name') or 'producto').replace(' ', '_')}.json"
        st.download_button(
            label="⬇️ Exportar .json",
            data=build_export(),
            file_name=filename,
            mime="application/json",
            use_container_width=True,
            key="btn_export",
        )

    with bar_c3:
        st.markdown("<div style='padding-top:28px'></div>", unsafe_allow_html=True)
        if st.button("⬆️ Importar .json", use_container_width=True, key="btn_open_import"):
            st.session_state["show_import"] = True

    with bar_c4:
        if st.session_state.get("show_import"):
            uploaded = st.file_uploader(
                "Selecciona un archivo .json",
                type="json",
                key="uploader",
            )
            if uploaded is not None:
                if st.session_state.get("_last_loaded") != uploaded.name + str(uploaded.size):
                    try:
                        data = json.load(uploaded)
                        for k, v in data.get("params", {}).items():
                            if k in DEFAULTS:
                                st.session_state[k] = v
                        st.session_state["p_name"] = data.get("product_name", "")
                        st.session_state["_last_loaded"] = uploaded.name + str(uploaded.size)
                        st.session_state["show_import"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al cargar: {e}")
        else:
            if st.session_state.get("_last_loaded"):
                st.markdown(
                    f"<div style='padding-top:30px;font-size:0.85rem;color:{SUCCESS};font-weight:700'>"
                    f"✅ {st.session_state.get('p_name','')}</div>",
                    unsafe_allow_html=True,
                )

    st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — INPUTS
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"<div class='section-label'>⚙️ Parámetros del modelo</div>", unsafe_allow_html=True)

    with st.expander("🏭 Producto", expanded=True):
        coste_unitario   = st.slider("Coste unitario (EUR)", 0.5, 100.0,
                               step=0.10, key="p_coste_unitario",
                               help="Precio EXW o FOB negociado con fábrica")
        moq              = st.slider("MOQ (unidades)", 50, 10000,
                               step=50, key="p_moq")
        coste_packaging  = st.slider("Packaging / ud (EUR)", 0.0, 5.0,
                               step=0.05, key="p_coste_packaging")
        coste_inspeccion = st.slider("Inspección origen (EUR)", 0.0, 1000.0,
                               step=25.0, key="p_coste_inspeccion")
        coste_agente     = st.slider("Agente / intermediario (EUR)", 0.0, 2000.0,
                               step=50.0, key="p_coste_agente")

    with st.expander("🚢 Logística"):
        metodo_envio      = st.selectbox("Método de envío", ["Marítimo", "Aéreo", "Tren"],
                              index=["Marítimo","Aéreo","Tren"].index(st.session_state["p_metodo_envio"]),
                              key="p_metodo_envio")
        peso_unidad       = st.slider("Peso / unidad (kg)", 0.05, 20.0,
                              step=0.05, key="p_peso_unidad")
        coste_kg          = st.slider("Coste / kg (EUR)", 0.5, 15.0,
                              step=0.10, key="p_coste_kg",
                              help="Marítimo ~0.8–1.5 · Aéreo ~4–8 · Tren ~1.5–3")
        arancel_pct       = st.slider("Aranceles (%)", 0.0, 45.0,
                              step=0.5, key="p_arancel_pct",
                              help="Depende del código HS")
        despacho_fijo     = st.slider("Despacho aduanero (EUR)", 0.0, 800.0,
                              step=25.0, key="p_despacho_fijo")
        seguro_pct        = st.slider("Seguro transporte (%)", 0.0, 3.0,
                              step=0.1, key="p_seguro_pct")
        costes_portuarios = st.slider("Costes portuarios (EUR)", 0.0, 500.0,
                              step=25.0, key="p_costes_portuarios")
        transporte_interno= st.slider("Transporte interno (EUR)", 0.0, 600.0,
                              step=20.0, key="p_transporte_interno")

    with st.expander("🛒 Amazon"):
        pvp               = st.slider("PVP (EUR)", 5.0, 200.0,
                              step=0.50, key="p_pvp")
        comision_pct      = st.slider("Comisión Amazon (%)", 6.0, 20.0,
                              step=0.5, key="p_comision_pct",
                              help="Hogar/Juguetes: 15% · Electrónica: 8% · Ropa: 17%")
        coste_fba         = st.slider("Coste FBA / ud (EUR)", 1.0, 15.0,
                              step=0.10, key="p_coste_fba")
        almacenamiento_mes= st.slider("Almacenamiento mensual (EUR)", 0.05, 2.0,
                              step=0.05, key="p_almacenamiento_mes")
        devolucion_pct    = st.slider("Tasa devoluciones (%)", 0.0, 20.0,
                              step=0.5, key="p_devolucion_pct")
        coste_devolucion  = st.slider("Coste por devolución (EUR)", 0.5, 10.0,
                              step=0.25, key="p_coste_devolucion")

    with st.expander("📣 Marketing / PPC"):
        cpc               = st.slider("CPC medio (EUR / clic)", 0.10, 3.0,
                              step=0.05, key="p_cpc")
        conversion_pct    = st.slider("Conversión (%)", 1.0, 30.0,
                              step=0.5, key="p_conversion_pct")
        presupuesto_diario= st.slider("Presupuesto diario (EUR)", 1.0, 200.0,
                              step=1.0, key="p_presupuesto_diario")

    with st.expander("💶 Fiscal — Recargo de equivalencia", expanded=True):
        st.markdown(
            f"<div style='font-size:0.8rem;color:{TEXT_MUTED};line-height:1.5;"
            f"background:{rgba(ACCENT,0.07)};border-radius:10px;padding:10px 12px;"
            f"margin-bottom:10px;border-left:3px solid {ACCENT}'>"
            f"<b>Régimen RE activo</b><br>"
            f"✅ El IVA cobrado al cliente <b>es tuyo</b> (ingreso real = PVP completo)<br>"
            f"❌ IVA + recargo en importación son <b>costes no recuperables</b>"
            f"</div>",
            unsafe_allow_html=True,
        )
        iva_pct     = st.slider("IVA ventas / importación (%)", 0.0, 27.0,
                        step=1.0, key="p_iva_pct",
                        help="Se aplica al PVP como ingreso y sobre (FOB+aranceles) como coste en aduanas")
        re_pct      = st.slider("Recargo de equivalencia (%)", 0.0, 10.0,
                        step=0.1, key="p_re_pct",
                        help="RE sobre (FOB + aranceles) en aduanas. Tipo general 2024: 5,2%")
        impuesto_pct= st.slider("IS / IRPF (%)", 0.0, 40.0,
                        step=1.0, key="p_impuesto_pct")

# ─────────────────────────────────────────────
# CÁLCULOS CENTRALES
# ─────────────────────────────────────────────
coste_prod_ud = coste_unitario + coste_packaging + (coste_inspeccion / moq) + (coste_agente / moq)

flete_total           = peso_unidad * coste_kg * moq
valor_fob_lote        = coste_unitario * moq
arancel_total         = valor_fob_lote * (arancel_pct / 100)
seguro_total          = valor_fob_lote * (seguro_pct / 100)
costes_fijos_logistica= despacho_fijo + costes_portuarios + transporte_interno

# IVA + Recargo de Equivalencia en aduanas — ambos son COSTE no recuperable para RE
base_iva_re       = valor_fob_lote + arancel_total          # base imponible en aduana
iva_importacion   = base_iva_re * (iva_pct / 100)           # IVA (21%) pagado en aduana
re_importacion    = base_iva_re * (re_pct / 100)            # Recargo Equivalencia pagado en aduana

logistica_total       = flete_total + arancel_total + seguro_total + costes_fijos_logistica + iva_importacion + re_importacion
coste_logistica_ud    = logistica_total / moq

# En RE el autónomo cobra IVA al cliente y se lo queda → ingreso real = PVP completo
pvp_neto       = pvp                                        # PVP íntegro = base de todos los cálculos
comision_amazon= pvp * (comision_pct / 100)                 # Amazon cobra % sobre precio total
coste_dev_ud   = (devolucion_pct / 100) * coste_devolucion
coste_amazon_ud= comision_amazon + coste_fba + almacenamiento_mes + coste_dev_ud

clics_por_venta  = 1 / (conversion_pct / 100)
coste_ads_ud     = cpc * clics_por_venta
acos_real        = (coste_ads_ud / pvp_neto) * 100 if pvp_neto > 0 else 0
clics_diarios    = presupuesto_diario / cpc
ventas_diarias   = clics_diarios * (conversion_pct / 100)
ventas_mensuales = ventas_diarias * 30

coste_total_ud      = coste_prod_ud + coste_logistica_ud + coste_amazon_ud + coste_ads_ud
beneficio_bruto_ud  = pvp_neto - coste_total_ud
margen_neto_pct     = (beneficio_bruto_ud / pvp_neto * 100) if pvp_neto > 0 else 0
impuesto_ud         = max(0, beneficio_bruto_ud * (impuesto_pct / 100))
beneficio_neto_ud   = beneficio_bruto_ud - impuesto_ud
margen_neto_real_pct= (beneficio_neto_ud / pvp_neto * 100) if pvp_neto > 0 else 0

beneficio_total_lote= beneficio_neto_ud * moq
inversion_total     = (coste_unitario + coste_packaging) * moq + logistica_total + coste_inspeccion + coste_agente
roi_pct             = (beneficio_total_lote / inversion_total * 100) if inversion_total > 0 else 0

costes_fijos_lote  = costes_fijos_logistica + coste_inspeccion + coste_agente
margen_contribucion= pvp_neto - (
    coste_prod_ud
    + (coste_logistica_ud - costes_fijos_lote / moq)
    + coste_amazon_ud + coste_ads_ud
)
break_even_uds = int(np.ceil(costes_fijos_lote / margen_contribucion)) if margen_contribucion > 0 else None
dias_retorno   = (moq / ventas_diarias) if ventas_diarias > 0 else None
beneficio_mensual = beneficio_neto_ud * ventas_mensuales

# ─────────────────────────────────────────────
# SEMÁFORO
# ─────────────────────────────────────────────
def semaforo(valor, verde, amarillo, invertido=False):
    if invertido:
        return "green" if valor <= verde else ("yellow" if valor <= amarillo else "red")
    return "green" if valor >= verde else ("yellow" if valor >= amarillo else "red")

color_margen = semaforo(margen_neto_real_pct, 20, 10)
color_roi    = semaforo(roi_pct, 50, 25)
color_acos   = semaforo(acos_real, 20, 30, invertido=True)
color_be     = ("green" if (break_even_uds and break_even_uds < moq * 0.5) else
                "yellow" if (break_even_uds and break_even_uds < moq) else "red")
emoji_color  = {"green": "🟢", "yellow": "🟡", "red": "🔴"}

# ─────────────────────────────────────────────
# PLOTLY BASE LAYOUT
# ─────────────────────────────────────────────
def base_layout(**kw):
    d = dict(
        template=PLOT_THEME,
        paper_bgcolor=PLOT_PAPER,
        plot_bgcolor=PLOT_BG,
        font=dict(family="Nunito", color=PLOT_FONT, size=13),
        margin=dict(t=24, b=36, l=44, r=16),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
    )
    d.update(kw)
    return d

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Resumen", "💰 Costes", "🎯 Escenarios", "📉 Sensibilidad", "✅ Checklist"
])

# ════════════════════════════════════════════
# TAB 1 — RESUMEN
# ════════════════════════════════════════════
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(f"{emoji_color[color_margen]} Margen neto",
              f"{margen_neto_real_pct:.1f}%", "objetivo >20%", delta_color="off")
    c2.metric(f"{emoji_color[color_roi]} ROI lote",
              f"{roi_pct:.1f}%", "objetivo >50%", delta_color="off")
    c3.metric(f"{emoji_color[color_acos]} ACOS real",
              f"{acos_real:.1f}%", "objetivo <20%", delta_color="off")
    c4.metric(f"{emoji_color[color_be]} Break-even",
              f"{break_even_uds:,} uds" if break_even_uds else "No viable",
              f"MOQ: {moq:,}", delta_color="off")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-label'>Desglose por unidad</div>", unsafe_allow_html=True)
        coste_amz_rest = coste_fba + almacenamiento_mes + coste_dev_ud
        iva_importacion_ud = iva_importacion / moq
        re_importacion_ud  = re_importacion  / moq
        pct = lambda v: f"{v / pvp_neto * 100:.1f}%" if pvp_neto else "—"
        rows_costes = [
            {"Concepto": "Producto (ud + pkg + inspec)",
             "EUR / ud": f"{coste_prod_ud:.3f}",           "% PVP": pct(coste_prod_ud)},
            {"Concepto": "Logística + flete + aduana",
             "EUR / ud": f"{coste_logistica_ud - iva_importacion_ud - re_importacion_ud:.3f}",
                                                            "% PVP": pct(coste_logistica_ud - iva_importacion_ud - re_importacion_ud)},
            {"Concepto": "  ↳ IVA importación (no recup.)",
             "EUR / ud": f"{iva_importacion_ud:.3f}",       "% PVP": pct(iva_importacion_ud)},
            {"Concepto": "  ↳ Recargo equiv. (no recup.)",
             "EUR / ud": f"{re_importacion_ud:.3f}",        "% PVP": pct(re_importacion_ud)},
            {"Concepto": "Comisión Amazon (sobre PVP c/IVA)",
             "EUR / ud": f"{comision_amazon:.3f}",          "% PVP": pct(comision_amazon)},
            {"Concepto": "FBA + almacén + devoluc.",
             "EUR / ud": f"{coste_amz_rest:.3f}",           "% PVP": pct(coste_amz_rest)},
            {"Concepto": "Publicidad (ads)",
             "EUR / ud": f"{coste_ads_ud:.3f}",             "% PVP": pct(coste_ads_ud)},
            {"Concepto": "COSTE TOTAL",
             "EUR / ud": f"{coste_total_ud:.3f}",           "% PVP": pct(coste_total_ud)},
            {"Concepto": "PVP (ingreso real RE, IVA incluido)",
             "EUR / ud": f"{pvp_neto:.3f}",                 "% PVP": "100.0%"},
            {"Concepto": "Beneficio bruto / ud",
             "EUR / ud": f"{beneficio_bruto_ud:+.3f}",      "% PVP": pct(beneficio_bruto_ud)},
            {"Concepto": "IRPF estimado",
             "EUR / ud": f"{-impuesto_ud:+.3f}",            "% PVP": pct(-impuesto_ud)},
            {"Concepto": "BENEFICIO NETO / ud",
             "EUR / ud": f"{beneficio_neto_ud:+.3f}",       "% PVP": pct(beneficio_neto_ud)},
        ]
        hl_costes = {
            7: "warn",
            11: "ok" if beneficio_neto_ud > 0 else "bad",
        }
        st.markdown(html_table(rows_costes, hl_costes), unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='section-label'>Distribución del PVP (ingreso real RE)</div>", unsafe_allow_html=True)
        pie_labels = ["Producto", "Logística", "Comisión Amazon", "FBA/Almacén/Devol.", "Publicidad", "Beneficio neto"]
        pie_values = [
            max(0, coste_prod_ud / pvp_neto * 100) if pvp_neto else 0,
            max(0, coste_logistica_ud / pvp_neto * 100) if pvp_neto else 0,
            max(0, comision_amazon / pvp_neto * 100) if pvp_neto else 0,
            max(0, coste_amz_rest / pvp_neto * 100) if pvp_neto else 0,
            max(0, coste_ads_ud / pvp_neto * 100) if pvp_neto else 0,
            max(0, beneficio_neto_ud / pvp_neto * 100) if pvp_neto else 0,
        ]
        pie_colors = [ACCENT, "#f28e2b", DANGER, "#06b6d4", "#8b5cf6", ACCENT2]
        fig_pie = go.Figure(data=[go.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.56,
            marker=dict(colors=pie_colors, line=dict(color=PLOT_BG, width=3)),
            # Solo % dentro — evita etiquetas rotadas
            textinfo="percent",
            textposition="inside",
            insidetextorientation="horizontal",
            textfont=dict(size=14, family="Nunito", color="#ffffff"),
            hovertemplate="<b>%{label}</b><br>%{value:.1f}% del PVP<extra></extra>",
            # Espaciado entre segmentos
            pull=[0.03] * len(pie_labels),
        )])
        # Anotación central grande y clara
        fig_pie.add_annotation(
            text=f"<b style='font-size:18px'>{pvp:.2f}€</b><br>"
                 f"<span style='font-size:11px;color:{PLOT_FONT}88'>ingreso real</span>",
            x=0.5, y=0.5, showarrow=False, align="center",
            font=dict(size=17, color=PLOT_FONT, family="Nunito"),
        )
        fig_pie.update_layout(**base_layout(
            height=400,
            margin=dict(t=16, b=8, l=8, r=8),
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom", y=-0.22,
                xanchor="center", x=0.5,
                font=dict(size=13, family="Nunito", color=PLOT_FONT),
                itemwidth=80,
                traceorder="normal",
            ),
        ))
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("<div class='section-label'>KPIs del lote</div>", unsafe_allow_html=True)
        ck1, ck2, ck3 = st.columns(3)
        ck1.metric("Inversión lote",  f"€{inversion_total:,.0f}")
        ck2.metric("Beneficio lote",  f"€{beneficio_total_lote:,.0f}")
        ck3.metric("Beneficio/mes",   f"€{beneficio_mensual:,.0f}")
        ck1.metric("Ventas / día",    f"{ventas_diarias:.1f} uds")
        ck2.metric("Días retorno",    f"{dias_retorno:.0f} d" if dias_retorno else "N/A")
        ck3.metric("Clics / día",     f"{clics_diarios:.0f}")

    st.divider()
    verde_count = sum([
        margen_neto_real_pct >= 20, roi_pct >= 50, acos_real <= 20,
        break_even_uds is not None and break_even_uds < moq,
        beneficio_neto_ud > 0,
    ])
    if verde_count >= 4:
        st.success("### 🚀 VEREDICTO: LANZAR — El producto cumple los criterios de rentabilidad")
    elif verde_count >= 2:
        st.warning("### ⚠️ VEREDICTO: AJUSTAR — Revisar costes o precio antes de lanzar")
    else:
        st.error("### 🛑 VEREDICTO: NO LANZAR — Producto no viable con estos parámetros")

# ════════════════════════════════════════════
# TAB 2 — COSTES
# ════════════════════════════════════════════
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-label'>Logística — detalle del lote</div>", unsafe_allow_html=True)
        rows_log = [
            {"Concepto": "Flete internacional",              "EUR lote": f"€{flete_total:,.2f}"},
            {"Concepto": "Aranceles aduaneros",              "EUR lote": f"€{arancel_total:,.2f}"},
            {"Concepto": "Seguro transporte",                "EUR lote": f"€{seguro_total:,.2f}"},
            {"Concepto": "Despacho aduanero",                "EUR lote": f"€{despacho_fijo:,.2f}"},
            {"Concepto": "Costes portuarios",                "EUR lote": f"€{costes_portuarios:,.2f}"},
            {"Concepto": "Transporte interno",               "EUR lote": f"€{transporte_interno:,.2f}"},
            {"Concepto": "IVA importación 🔴 no recuperable","EUR lote": f"€{iva_importacion:,.2f}"},
            {"Concepto": "Recargo equiv. 🔴 no recuperable", "EUR lote": f"€{re_importacion:,.2f}"},
            {"Concepto": "TOTAL LOGÍSTICA LOTE",             "EUR lote": f"€{logistica_total:,.2f}"},
            {"Concepto": "Logística / unidad",               "EUR lote": f"€{coste_logistica_ud:,.3f}"},
        ]
        st.markdown(html_table(rows_log, {6: "bad", 7: "bad", 8: "warn", 9: "warn"}), unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Publicidad — métricas</div>", unsafe_allow_html=True)
        rows_ads = [
            {"Métrica": "CPC",                     "Valor": f"€{cpc:.2f}"},
            {"Métrica": "Conversión",              "Valor": f"{conversion_pct}%"},
            {"Métrica": "Clics / venta",           "Valor": f"{clics_por_venta:.1f}"},
            {"Métrica": "Coste ads / venta",       "Valor": f"€{coste_ads_ud:.2f}"},
            {"Métrica": "ACOS real",               "Valor": f"{acos_real:.1f}%"},
            {"Métrica": "Clics / día",             "Valor": f"{clics_diarios:.1f}"},
            {"Métrica": "Ventas / día",            "Valor": f"{ventas_diarias:.1f}"},
        ]
        st.markdown(html_table(rows_ads), unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-label'>Amazon — detalle / unidad</div>", unsafe_allow_html=True)
        iva_ud = pvp * iva_pct / 100
        rows_amz = [
            {"Concepto": "PVP cobrado al cliente",               "EUR/ud": f"€{pvp:.3f}"},
            {"Concepto": "  del que: IVA (te lo quedas ✅ RE)",  "EUR/ud": f"€{iva_ud:.3f}"},
            {"Concepto": "  del que: precio sin IVA",            "EUR/ud": f"€{pvp - iva_ud:.3f}"},
            {"Concepto": "INGRESO REAL / ud (RE)",               "EUR/ud": f"€{pvp:.3f}"},
            {"Concepto": "— Comisión Amazon (sobre PVP c/IVA)",  "EUR/ud": f"€{-comision_amazon:+.3f}"},
            {"Concepto": "— Coste FBA",                          "EUR/ud": f"€{-coste_fba:+.3f}"},
            {"Concepto": "— Almacenamiento mensual",             "EUR/ud": f"€{-almacenamiento_mes:+.3f}"},
            {"Concepto": "— Coste devoluciones",                 "EUR/ud": f"€{-coste_dev_ud:+.3f}"},
            {"Concepto": "TOTAL COSTES AMAZON",                  "EUR/ud": f"€{-(comision_amazon+coste_fba+almacenamiento_mes+coste_dev_ud):+.3f}"},
        ]
        st.markdown(html_table(rows_amz, {1: "ok", 3: "ok", 8: "warn"}), unsafe_allow_html=True)

        st.markdown("<div class='section-label'>Break-even</div>", unsafe_allow_html=True)
        if break_even_uds:
            pct_moq = break_even_uds / moq * 100
            cb1, cb2 = st.columns(2)
            cb1.metric("Break-even (uds)", f"{break_even_uds:,}")
            cb2.metric("% del MOQ", f"{pct_moq:.0f}%")

            uds_r = np.linspace(0, moq, 80)
            ing_be = uds_r * pvp_neto
            cos_be = uds_r * (coste_total_ud - costes_fijos_lote / moq) + costes_fijos_lote

            fig_be = go.Figure()
            fig_be.add_trace(go.Scatter(
                x=uds_r, y=ing_be, name="Ingresos",
                line=dict(color=ACCENT2, width=2.5),
                fill="tozeroy", fillcolor=rgba(ACCENT2, 0.08),
            ))
            fig_be.add_trace(go.Scatter(
                x=uds_r, y=cos_be, name="Costes",
                line=dict(color=DANGER, width=2.5),
                fill="tozeroy", fillcolor=rgba(DANGER, 0.08),
            ))
            fig_be.add_vline(x=break_even_uds, line_dash="dash", line_color=WARNING,
                             annotation_text=f" BE: {break_even_uds} uds",
                             annotation_font_color=WARNING, annotation_font_size=12)
            fig_be.update_layout(**base_layout(
                height=240, xaxis_title="Unidades vendidas", yaxis_title="EUR",
                legend=dict(orientation="h", y=1.1, font=dict(size=11))
            ))
            st.plotly_chart(fig_be, use_container_width=True)
        else:
            st.error("Break-even no alcanzable — margen de contribución negativo.")

# ════════════════════════════════════════════
# TAB 3 — ESCENARIOS
# ════════════════════════════════════════════
with tab3:
    st.caption("Los escenarios ajustan PVP, CPC, conversión y logística respecto al caso base.")

    def calcular_escenario(pvp_s, cpc_s, conv_s, log_factor):
        pvp_n  = pvp_s / (1 + iva_pct / 100)
        log_ud = coste_logistica_ud * log_factor
        ads_ud = cpc_s / (conv_s / 100)
        amz_ud = pvp_n * (comision_pct / 100) + coste_fba + almacenamiento_mes + coste_dev_ud
        total  = coste_prod_ud + log_ud + amz_ud + ads_ud
        ben    = pvp_n - total
        margen = (ben / pvp_n * 100) if pvp_n > 0 else 0
        acos_s = (ads_ud / pvp_n * 100) if pvp_n > 0 else 0
        ben_net= ben - max(0, ben * impuesto_pct / 100)
        b_lote = ben_net * moq
        inv    = (coste_unitario + coste_packaging) * moq + logistica_total * log_factor + coste_inspeccion + coste_agente
        roi_s  = (b_lote / inv * 100) if inv > 0 else 0
        dec    = "LANZAR" if margen >= 20 and roi_s >= 50 else ("AJUSTAR" if margen >= 10 else "NO LANZAR")
        return dict(
            PVP=f"€{pvp_s:.2f}", CPC=f"€{cpc_s:.2f}",
            Conversión=f"{conv_s:.1f}%", LogFactor=f"×{log_factor:.2f}",
            AdsUd=f"€{ads_ud:.2f}", ACOS=f"{acos_s:.1f}%",
            BenNeto=f"€{ben_net:.2f}", Margen=f"{margen:.1f}%",
            BenLote=f"€{b_lote:,.0f}", ROI=f"{roi_s:.1f}%",
            Decisión=dec,
            _margen=margen,
        )

    e_pes = calcular_escenario(pvp * 0.88, cpc * 1.35, conversion_pct * 0.67, 1.30)
    e_rea = calcular_escenario(pvp,        cpc,        conversion_pct,        1.00)
    e_opt = calcular_escenario(pvp * 1.12, cpc * 0.64, conversion_pct * 1.33, 0.78)

    # HTML table for scenarios (columns = scenarios, rows = metrics)
    display_keys = ["PVP","CPC","Conversión","LogFactor","AdsUd","ACOS","BenNeto","Margen","BenLote","ROI","Decisión"]
    labels_map = {
        "PVP":"PVP","CPC":"CPC","Conversión":"Conversión","LogFactor":"Factor logística",
        "AdsUd":"Ads / ud","ACOS":"ACOS","BenNeto":"Beneficio neto/ud",
        "Margen":"Margen neto","BenLote":"Beneficio lote","ROI":"ROI","Decisión":"Decisión",
    }
    def dec_color(d):
        return {"LANZAR": SUCCESS, "AJUSTAR": WARNING, "NO LANZAR": DANGER}.get(d, TEXT)

    th_s = (f"padding:9px 14px; font-size:0.76rem; font-weight:800; text-transform:uppercase;"
            f"letter-spacing:0.07em; color:{TEXT_MUTED}; background:{TH_BG}; border-bottom:2px solid {CARD_BORD};")
    td_label_s = (f"padding:8px 14px; font-size:0.88rem; font-weight:700; color:{TEXT_MUTED};"
                  f"background:{TD_BG}; border-bottom:1px solid {CARD_BORD};")

    esc_html = (
        f"<div style='border-radius:14px;overflow:hidden;border:1px solid {CARD_BORD};"
        f"box-shadow:0 2px 16px {rgba(ACCENT,0.08)};margin-bottom:16px'>"
        f"<table style='width:100%;border-collapse:collapse;font-family:Nunito,sans-serif'>"
        f"<thead><tr>"
        f"<th style='{th_s}'>Métrica</th>"
        f"<th style='{th_s}'>🔴 Pesimista</th>"
        f"<th style='{th_s}'>🟡 Realista</th>"
        f"<th style='{th_s}'>🟢 Optimista</th>"
        f"</tr></thead><tbody>"
    )
    for i, k in enumerate(display_keys):
        bg = TD_BG if i % 2 == 0 else TD_BG_ALT
        td_s = (f"padding:8px 14px; font-size:0.9rem; color:{TEXT};"
                f"background:{bg}; border-bottom:1px solid {CARD_BORD};")
        vals = [e_pes[k], e_rea[k], e_opt[k]]
        cells = ""
        for v in vals:
            fw = "700" if k == "Decisión" else "normal"
            col = dec_color(v) if k == "Decisión" else TEXT
            cells += f"<td style='{td_s} font-weight:{fw}; color:{col}'>{v}</td>"
        esc_html += f"<tr><td style='{td_label_s}'>{labels_map[k]}</td>{cells}</tr>"
    esc_html += "</tbody></table></div>"
    st.markdown(esc_html, unsafe_allow_html=True)

    # Bar chart
    scenarios  = ["Pesimista", "Realista", "Optimista"]
    margenes   = [e_pes["_margen"], e_rea["_margen"], e_opt["_margen"]]
    rois_v     = [float(e["ROI"].replace("%","")) for e in [e_pes, e_rea, e_opt]]
    bar_colors = [DANGER if m < 10 else WARNING if m < 20 else ACCENT2 for m in margenes]

    fig_esc = go.Figure()
    fig_esc.add_trace(go.Bar(
        name="Margen neto %", x=scenarios, y=margenes,
        marker=dict(color=bar_colors, line=dict(width=0)),
        text=[f"{m:.1f}%" for m in margenes], textposition="outside",
        textfont=dict(size=13, family="Nunito", color=PLOT_FONT),
    ))
    fig_esc.add_trace(go.Scatter(
        name="ROI %", x=scenarios, y=rois_v, mode="lines+markers+text",
        yaxis="y2", text=[f"{r:.1f}%" for r in rois_v], textposition="top center",
        textfont=dict(size=12, family="Nunito"),
        line=dict(color=ACCENT, width=2.5),
        marker=dict(size=10, color=ACCENT, line=dict(color=PLOT_BG, width=2)),
    ))
    fig_esc.add_hline(y=20, line_dash="dash", line_color=ACCENT2, line_width=1.5,
                      annotation_text=" objetivo 20%",
                      annotation_font_color=ACCENT2, annotation_font_size=11)
    fig_esc.update_layout(**base_layout(
        height=360, bargap=0.35,
        yaxis=dict(title="Margen neto (%)", gridcolor=GRID_COLOR, linecolor=GRID_COLOR),
        yaxis2=dict(title="ROI (%)", overlaying="y", side="right"),
        legend=dict(orientation="h", y=1.08, font=dict(size=12)),
    ))
    st.plotly_chart(fig_esc, use_container_width=True)

# ════════════════════════════════════════════
# TAB 4 — SENSIBILIDAD
# ════════════════════════════════════════════
with tab4:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='section-label'>Margen neto vs CPC</div>", unsafe_allow_html=True)
        cpcs_r = np.arange(0.15, 1.55, 0.04)
        marg_cpc = [(pvp_neto - (coste_prod_ud + coste_logistica_ud + coste_amazon_ud + c / (conversion_pct / 100))) / pvp_neto * 100
                    if pvp_neto else 0 for c in cpcs_r]

        fig_cpc = go.Figure()
        fig_cpc.add_trace(go.Scatter(
            x=cpcs_r, y=marg_cpc, mode="lines",
            line=dict(color=ACCENT, width=2.5),
            fill="tozeroy", fillcolor=rgba(ACCENT, 0.10),
        ))
        fig_cpc.add_hline(y=20, line_dash="dash", line_color=ACCENT2, line_width=1.5,
                          annotation_text=" 20% objetivo", annotation_font_color=ACCENT2)
        fig_cpc.add_hline(y=0, line_dash="solid", line_color=DANGER, line_width=1,
                          annotation_text=" break-even", annotation_font_color=DANGER)
        fig_cpc.add_vline(x=cpc, line_dash="dot", line_color=WARNING, line_width=1.5,
                          annotation_text=f" actual €{cpc:.2f}", annotation_font_color=WARNING)
        fig_cpc.update_layout(**base_layout(height=280, xaxis_title="CPC (EUR)", yaxis_title="Margen neto (%)"))
        st.plotly_chart(fig_cpc, use_container_width=True)

        cpcs_t = [0.20, 0.30, 0.40, 0.55, 0.65, 0.75, 0.90, 1.10]
        rows_cpc = []
        for c in cpcs_t:
            ads = c / (conversion_pct / 100)
            ben = pvp_neto - (coste_prod_ud + coste_logistica_ud + coste_amazon_ud + ads)
            m   = ben / pvp_neto * 100 if pvp_neto else 0
            rows_cpc.append({"CPC": f"€{c:.2f}", "Ads/ud": f"€{ads:.2f}",
                              "Beneficio/ud": f"€{ben:.2f}", "Margen": f"{m:.1f}%"})
        st.markdown(html_table(rows_cpc), unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='section-label'>Margen neto vs Precio de venta</div>", unsafe_allow_html=True)
        pvps_r = np.linspace(pvp * 0.65, pvp * 1.45, 60)
        marg_pvp = []
        for p in pvps_r:
            pn  = p / (1 + iva_pct / 100)
            amz = pn * (comision_pct / 100) + coste_fba + almacenamiento_mes + coste_dev_ud
            ben = pn - (coste_prod_ud + coste_logistica_ud + amz + coste_ads_ud)
            marg_pvp.append(ben / pn * 100 if pn else 0)

        fig_pvp = go.Figure()
        fig_pvp.add_trace(go.Scatter(
            x=pvps_r, y=marg_pvp, mode="lines",
            line=dict(color="#f28e2b", width=2.5),
            fill="tozeroy", fillcolor=rgba("#f28e2b", 0.10),
        ))
        fig_pvp.add_hline(y=20, line_dash="dash", line_color=ACCENT2, line_width=1.5,
                          annotation_text=" 20% objetivo", annotation_font_color=ACCENT2)
        fig_pvp.add_hline(y=0, line_dash="solid", line_color=DANGER, line_width=1)
        fig_pvp.add_vline(x=pvp, line_dash="dot", line_color=WARNING, line_width=1.5,
                          annotation_text=f" PVP actual €{pvp:.2f}", annotation_font_color=WARNING)
        fig_pvp.update_layout(**base_layout(height=280, xaxis_title="PVP (EUR)", yaxis_title="Margen neto (%)"))
        st.plotly_chart(fig_pvp, use_container_width=True)

    st.markdown("<div class='section-label'>Mapa de calor — Beneficio/ud · CPC × Conversión</div>", unsafe_allow_html=True)
    cpcs_h  = [0.20, 0.30, 0.40, 0.55, 0.70, 0.85, 1.00]
    convs_h = [6, 8, 10, 12, 15, 18, 22]
    heat_z  = [
        [round(pvp_neto - (coste_prod_ud + coste_logistica_ud + coste_amazon_ud + c / (cv / 100)), 2)
         for cv in convs_h]
        for c in cpcs_h
    ]

    fig_heat = go.Figure(data=go.Heatmap(
        z=heat_z,
        x=[f"{cv}%" for cv in convs_h],
        y=[f"€{c:.2f}" for c in cpcs_h],
        colorscale=[[0, DANGER], [0.35, WARNING], [0.6, "#FFEB3B"], [1, ACCENT2]],
        text=[[f"€{v:.2f}" for v in row] for row in heat_z],
        texttemplate="%{text}",
        textfont=dict(size=12, family="Nunito"),
        colorbar=dict(title="€/ud", tickfont=dict(family="Nunito", size=11)),
    ))
    fig_heat.update_layout(**base_layout(
        height=300, xaxis_title="Tasa de conversión", yaxis_title="CPC (EUR)",
        margin=dict(t=10, b=40, l=64, r=16),
    ))
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Verde = rentable · Rojo = pérdidas. Cada celda = beneficio neto/ud en ese escenario.")

# ════════════════════════════════════════════
# TAB 5 — CHECKLIST
# ════════════════════════════════════════════
with tab5:
    checks = [
        ("Margen neto ≥ 20%",                    margen_neto_real_pct >= 20),
        ("ROI por lote ≥ 50%",                   roi_pct >= 50),
        ("Break-even < MOQ",                     break_even_uds is not None and break_even_uds < moq),
        ("PVP ≥ 3× coste landed",                pvp_neto >= (coste_prod_ud + coste_logistica_ud) * 3),
        ("ACOS sostenible (< margen bruto)",      acos_real < (beneficio_bruto_ud / pvp_neto * 100 + acos_real) if pvp_neto > 0 else False),
        ("Beneficio neto / ud > 0",               beneficio_neto_ud > 0),
        ("Inversión recuperable en < 90 días",    dias_retorno is not None and dias_retorno < 90),
        ("Coste ads < 25% del PVP neto",          coste_ads_ud < pvp_neto * 0.25),
    ]
    manual_checks = [
        "Demanda validada (BSR < 50,000 en categoría)",
        "≥ 3 competidores con reviews al precio objetivo",
        "Proveedor verificado y muestra aprobada",
        "Reposición posible en < 45 días",
    ]

    col1, col2 = st.columns(2)
    ok_count = 0
    with col1:
        st.markdown("<div class='section-label'>Criterios automáticos</div>", unsafe_allow_html=True)
        for label, passed in checks:
            if passed:
                ok_count += 1
            badge_cls = "badge-green" if passed else "badge-red"
            badge_txt = "CUMPLE" if passed else "FALLA"
            icon = "✅" if passed else "❌"
            st.markdown(
                f"<div style='padding:6px 0; font-size:0.95rem; color:{TEXT}'>"
                f"{icon} {label} &nbsp;<span class='{badge_cls}'>{badge_txt}</span></div>",
                unsafe_allow_html=True
            )

    manual_ok = 0
    with col2:
        st.markdown("<div class='section-label'>Criterios manuales</div>", unsafe_allow_html=True)
        for item in manual_checks:
            if st.checkbox(item):
                manual_ok += 1

    st.divider()
    total_ok     = ok_count + manual_ok
    total_checks = len(checks) + len(manual_checks)
    st.markdown(f"### Puntuación: **{total_ok} / {total_checks}**")
    st.progress(total_ok / total_checks)

    if total_ok >= int(total_checks * 0.75):
        st.success("### 🚀 RECOMENDACIÓN: LANZAR — Cumples los criterios de rentabilidad")
    elif total_ok >= int(total_checks * 0.5):
        st.warning("### ⚠️ RECOMENDACIÓN: AJUSTAR — Revisa los puntos en rojo")
    else:
        st.error("### 🛑 RECOMENDACIÓN: NO LANZAR — Demasiados criterios sin cumplir")

    st.divider()
    st.markdown("<div class='section-label'>Errores típicos a evitar</div>", unsafe_allow_html=True)
    for titulo, desc in [
        ("IVA en el PVP",              "Trabaja siempre con PVP sin IVA. El IVA no es ingreso tuyo."),
        ("CPC optimista",              "Valida el CPC real con Helium10 o JungleScout antes de proyectar."),
        ("Peso volumétrico ignorado",  "El transitario factura por max(peso real, peso vol). Mide la caja real."),
        ("Aranceles desconocidos",     "Verifica el código HS antes de encargar. Pueden ser 0–45%."),
        ("Sin provisión devoluciones", "En Amazon EU las devoluciones son obligatorias. Provisiona ≥ 5%."),
        ("Almacenamiento en Q4",       "El almacenamiento entre oct–dic puede ser 3× más caro."),
        ("Sin colchón de stock",       "Un stockout destruye tu BSR. Ten siempre ≥ 30 días de cobertura."),
    ]:
        with st.expander(f"⚠️ {titulo}"):
            st.write(desc)
