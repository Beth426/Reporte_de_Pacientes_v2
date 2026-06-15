import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import date

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Centro Terapéutico · Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
# PALETA Y CONSTANTES
# ═══════════════════════════════════════════════════════════════════════════════
C = dict(
    bg       = "#0E1117",
    card     = "#161B22",
    border   = "#21262D",
    text1    = "#E6EDF3",
    text2    = "#8B949E",
    text3    = "#484F58",
    blue     = "#2E86AB",
    teal     = "#1B998B",
    coral    = "#E05263",
    amber    = "#F4A261",
    green    = "#2DC653",
    purple   = "#7B68EE",
    pink     = "#E07BE0",
    grid     = "rgba(139,148,158,0.08)",
    grid2    = "rgba(139,148,158,0.15)",
)

AREA_COLORS = {
    "Fisioterapia":      C["blue"],
    "Fonoaudiología":    C["amber"],
    "T. Ocupacional":    C["teal"],
    "Psicología":        C["purple"],
    "T. del Lenguaje":   C["pink"],
    "Neuropsicología":   C["coral"],
    "Integr. Sensorial": C["green"],
    "Otro":              C["text3"],
}

MESES_ES = {1:"Ene",2:"Feb",3:"Mar",4:"Abr",5:"May",6:"Jun",
            7:"Jul",8:"Ago",9:"Sep",10:"Oct",11:"Nov",12:"Dic"}
DIAS_ES  = {"Monday":"Lunes","Tuesday":"Martes","Wednesday":"Miércoles",
            "Thursday":"Jueves","Friday":"Viernes","Saturday":"Sábado","Sunday":"Domingo"}
DIAS_ORD = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]

# ═══════════════════════════════════════════════════════════════════════════════
# PLOTLY TEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════
pio.templates["centro"] = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, sans-serif", color=C["text2"], size=12),
        title=dict(font=dict(size=14, color=C["text1"])),
        xaxis=dict(gridcolor=C["grid"], zerolinecolor=C["grid2"],
                   tickfont=dict(size=11), title=dict(standoff=12)),
        yaxis=dict(gridcolor=C["grid"], zerolinecolor=C["grid2"],
                   tickfont=dict(size=11), title=dict(standoff=12)),
        legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        hoverlabel=dict(bgcolor=C["card"], bordercolor=C["border"],
                        font=dict(color=C["text1"], size=12)),
        margin=dict(l=10, r=10, t=36, b=10),
        colorway=[C["blue"], C["teal"], C["amber"], C["purple"],
                  C["coral"], C["green"], C["pink"]],
    )
)
pio.templates.default = "centro"

# ═══════════════════════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
    --bg: {C["bg"]};
    --card: {C["card"]};
    --border: {C["border"]};
    --text1: {C["text1"]};
    --text2: {C["text2"]};
    --blue: {C["blue"]};
    --teal: {C["teal"]};
    --coral: {C["coral"]};
    --amber: {C["amber"]};
    --green: {C["green"]};
}}

html, body, [data-testid="stApp"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

/* Sidebar */
[data-testid="stSidebar"] {{
    background: var(--card);
    border-right: 1px solid var(--border);
}}
[data-testid="stSidebar"] .stMarkdown h1 {{
    font-size: 1.15rem;
    font-weight: 600;
    letter-spacing: -0.01em;
}}

/* Ocultar el header default de Streamlit */
header[data-testid="stHeader"] {{
    background: transparent;
}}

/* KPI Cards */
.kpi-row {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}}
@media (max-width: 900px) {{
    .kpi-row {{
        grid-template-columns: repeat(3, 1fr);
    }}
}}
@media (max-width: 600px) {{
    .kpi-row {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}
.kpi-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px 20px;
    transition: border-color 0.2s, transform 0.15s;
}}
.kpi-card:hover {{
    border-color: var(--blue);
    transform: translateY(-1px);
}}
.kpi-icon {{
    width: 36px;
    height: 36px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 10px;
}}
.kpi-label {{
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--text2);
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 4px;
}}
.kpi-value {{
    font-size: 1.65rem;
    font-weight: 700;
    color: var(--text1);
    line-height: 1.1;
    letter-spacing: -0.02em;
}}
.kpi-trend {{
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 6px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
    padding: 2px 8px;
    border-radius: 6px;
}}
.kpi-trend.up {{
    color: #2DC653;
    background: rgba(45,198,83,0.1);
}}
.kpi-trend.down {{
    color: #E05263;
    background: rgba(224,82,99,0.1);
}}
.kpi-trend.neutral {{
    color: var(--text2);
    background: rgba(139,148,158,0.1);
}}

/* Chart containers */
.chart-box {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 18px 12px;
    margin-bottom: 16px;
}}
.chart-title {{
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text1);
    margin: 0 0 2px;
}}
.chart-subtitle {{
    font-size: 0.72rem;
    color: var(--text2);
    margin: 0 0 14px;
}}

/* Ocultar dividers de Streamlit (usamos los propios) */
[data-testid="stMarkdownContainer"] hr {{
    border-color: var(--border);
    opacity: 0.4;
}}

/* Multiselect pills */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {{
    background: rgba(46,134,171,0.15);
    border: 1px solid rgba(46,134,171,0.3);
    border-radius: 6px;
    color: var(--blue);
}}

/* File uploader */
[data-testid="stFileUploader"] > div:first-child {{
    border: 1px dashed var(--border);
    border-radius: 10px;
    background: rgba(46,134,171,0.04);
}}
[data-testid="stFileUploader"] > div:first-child:hover {{
    border-color: var(--blue);
    background: rgba(46,134,171,0.08);
}}

/* Metric default (ocultar, usamos custom) */
[data-testid="stMetric"] {{
    display: none;
}}

/* Tabs si los usamos */
.stTabs [data-baseweb="tab-list"] {{
    gap: 2px;
    background: var(--card);
    border-radius: 10px;
    padding: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 500;
}}

/* Footer */
.footer {{
    text-align: center;
    color: var(--text2);
    font-size: 0.7rem;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}}

/* Welcome screen */
.welcome {{
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
}}
.welcome-icon {{
    width: 72px;
    height: 72px;
    border-radius: 16px;
    background: rgba(46,134,171,0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    margin-bottom: 1.2rem;
}}
.welcome h2 {{
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text1);
    margin: 0 0 0.5rem;
}}
.welcome p {{
    font-size: 0.9rem;
    color: var(--text2);
    max-width: 420px;
    line-height: 1.6;
}}

/* Sidebar brand */
.brand {{
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 6px 0 4px;
}}
.brand-icon {{
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: linear-gradient(135deg, {C["blue"]}, {C["teal"]});
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}}
.brand-text {{
    font-size: 1rem;
    font-weight: 600;
    color: var(--text1);
    line-height: 1.2;
}}
.brand-sub {{
    font-size: 0.7rem;
    color: var(--text2);
}}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FUNCIONES DE DATOS
# ═══════════════════════════════════════════════════════════════════════════════
def normalizar_area(s):
    s = str(s).lower()
    if "fisioterap"  in s: return "Fisioterapia"
    if "fonoaud" in s or "foniatria" in s: return "Fonoaudiología"
    if "lenguaje"    in s: return "T. del Lenguaje"
    if "ocupacional" in s: return "T. Ocupacional"
    if "neuro"       in s: return "Neuropsicología"
    if "psicolog"    in s: return "Psicología"
    if "sensorial"   in s: return "Integr. Sensorial"
    return "Otro"

@st.cache_data(show_spinner=False)
def cargar(archivo):
    df = pd.read_excel(archivo, sheet_name=0, engine="openpyxl")
    mask = df["ESTADO-ACTUAL-CITA"].astype(str) != "FINALIZADA"
    for i in df[mask].index:
        df.at[i, "SERVICIO"]            = df.at[i, "PROFESIONAL-ATIENDE"]
        df.at[i, "PROFESIONAL-ATIENDE"] = df.at[i, "CONSENTIMIENTO-FIRMADO"]
        df.at[i, "FECHA-FIN-ATENCION"]  = df.at[i, "FECHA-CANCELA"]
    df["FFIN"]   = pd.to_datetime(df["FECHA-FIN-ATENCION"], errors="coerce")
    df["MES"]    = df["FFIN"].dt.to_period("M")
    df["DIA"]    = df["FFIN"].dt.day_name()
    df["CUMPLE"] = pd.to_datetime(df["CUMPLEANIOS"], errors="coerce")
    df["EDAD"]   = (df["FFIN"].dt.normalize() - df["CUMPLE"]).dt.days // 365
    df["DIA_ES"] = df["DIA"].map(DIAS_ES)
    df["AREA"]   = df["SERVICIO"].apply(normalizar_area)
    df["PACIENTE"] = (df["NOMBRES"].astype(str).str.strip() + " " +
                      df["APELLIDOS"].astype(str).str.strip()).str.strip()
    return df, int(mask.sum())

def mes_label(p):
    return f"{MESES_ES[p.month]} {p.year}"

# ═══════════════════════════════════════════════════════════════════════════════
# COMPONENTES UI
# ═══════════════════════════════════════════════════════════════════════════════
def render_kpi(icon, icon_bg, label, value, trend_text="", trend_dir="neutral"):
    trend_html = ""
    if trend_text:
        arrow = "↑" if trend_dir == "up" else ("↓" if trend_dir == "down" else "→")
        trend_html = f'<div class="kpi-trend {trend_dir}">{arrow} {trend_text}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon" style="background:{icon_bg}">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {trend_html}
    </div>"""

def chart_container(title, subtitle=""):
    sub = f'<p class="chart-subtitle">{subtitle}</p>' if subtitle else ""
    return f'<div class="chart-box"><p class="chart-title">{title}</p>{sub}'

def chart_close():
    return '</div>'

def calc_trend(df, meses_sorted):
    if len(meses_sorted) < 2:
        return {}, {}
    prev = meses_sorted[-2]
    curr = meses_sorted[-1]
    d_prev = df[df["MES"] == prev]
    d_curr = df[df["MES"] == curr]
    vals = {
        "evol": (len(d_curr), len(d_prev)),
        "pac":  (d_curr["DOCUMENTO"].nunique(), d_prev["DOCUMENTO"].nunique()),
        "prof": (d_curr["PROFESIONAL-ATIENDE"].nunique(), d_prev["PROFESIONAL-ATIENDE"].nunique()),
    }
    trends = {}
    for k, (c, p) in vals.items():
        if p == 0:
            trends[k] = ("", "neutral")
        else:
            pct = ((c - p) / p) * 100
            direction = "up" if pct > 2 else ("down" if pct < -2 else "neutral")
            trends[k] = (f"{abs(pct):.0f}% vs {mes_label(prev)}", direction)
    return trends

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="brand">
        <div class="brand-icon">🩺</div>
        <div>
            <div class="brand-text">Centro Terapéutico</div>
            <div class="brand-sub">Dashboard de evoluciones</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    archivo = st.file_uploader("📂  Subir archivo semestral", type=["xlsx"],
                               help="Arrastra tu archivo .xlsx o haz clic para seleccionarlo")

    if archivo:
        with st.spinner("Procesando archivo..."):
            df, correcciones = cargar(archivo)

        meses_periodo = sorted(df["MES"].dropna().unique())
        mes_opts      = [mes_label(p) for p in meses_periodo]
        mes_map       = {mes_label(p): p for p in meses_periodo}
        areas_opts    = sorted(df["AREA"].unique())

        st.markdown("---")
        st.markdown(f"<p style='font-size:0.75rem;font-weight:600;color:{C['text2']};text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px'>Filtros</p>", unsafe_allow_html=True)
        sel_meses = st.multiselect("Meses", mes_opts, default=mes_opts, label_visibility="collapsed",
                                   placeholder="Seleccionar meses...")
        sel_areas = st.multiselect("Áreas terapéuticas", areas_opts, default=areas_opts,
                                   label_visibility="collapsed", placeholder="Seleccionar áreas...")

        if correcciones:
            st.markdown("---")
            st.success(f"Corrección automática: {correcciones} fila(s) realineadas", icon="✅")

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:0.7rem;color:{C['text3']};line-height:1.6;padding:4px 0">
            <strong style="color:{C['text2']}">Resumen del archivo</strong><br>
            {len(df):,} evoluciones · {df['DOCUMENTO'].nunique()} pacientes<br>
            {mes_opts[0]} – {mes_opts[-1]}
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
if not archivo:
    st.markdown(f"""
    <div class="welcome">
        <div class="welcome-icon">📊</div>
        <h2>Dashboard · Centro Terapéutico</h2>
        <p>Sube el archivo semestral de evoluciones (.xlsx) en el panel izquierdo
           para visualizar las métricas del centro.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

periodos_sel = [mes_map[m] for m in sel_meses if m in mes_map]
df_f = df[df["MES"].isin(periodos_sel) & df["AREA"].isin(sel_areas)]

if df_f.empty:
    st.warning("No hay datos para la combinación de filtros seleccionada.")
    st.stop()

meses_sorted = sorted(df_f["MES"].dropna().unique())
trends = calc_trend(df, sorted(df["MES"].dropna().unique()))

# ── KPIs ──────────────────────────────────────────────────────────────────────
evol_t = trends.get("evol", ("","neutral"))
pac_t  = trends.get("pac",  ("","neutral"))
prof_t = trends.get("prof", ("","neutral"))

kpi_html = '<div class="kpi-row">'
kpi_html += render_kpi("📋", "rgba(46,134,171,0.12)", "Evoluciones",
                       f"{len(df_f):,}", evol_t[0], evol_t[1])
kpi_html += render_kpi("👥", "rgba(27,153,139,0.12)", "Pacientes únicos",
                       f"{df_f['DOCUMENTO'].nunique():,}", pac_t[0], pac_t[1])
kpi_html += render_kpi("🧑‍⚕️", "rgba(123,104,238,0.12)", "Profesionales",
                       f"{df_f['PROFESIONAL-ATIENDE'].nunique()}", prof_t[0], prof_t[1])
kpi_html += render_kpi("🏥", "rgba(244,162,97,0.12)", "Áreas activas",
                       f"{df_f['AREA'].nunique()}")
kpi_html += render_kpi("📅", "rgba(45,198,83,0.12)", "Período",
                       f"{len(meses_sorted)} meses")
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICAS — FILA 1
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    st.markdown(chart_container("Evoluciones por mes",
                "Tendencia mensual de sesiones realizadas"), unsafe_allow_html=True)
    evol_mes = df_f.groupby("MES").size().reset_index(name="Evoluciones")
    evol_mes["Mes"] = evol_mes["MES"].apply(mes_label)
    fig1 = go.Figure()
    fig1.add_scatter(x=evol_mes["Mes"], y=evol_mes["Evoluciones"], mode="lines+markers",
                     line=dict(color=C["blue"], width=3, shape="spline"),
                     marker=dict(size=9, color=C["blue"], line=dict(width=2, color=C["card"])),
                     fill="tozeroy", fillcolor="rgba(46,134,171,0.08)",
                     hovertemplate="<b>%{x}</b><br>%{y:,} evoluciones<extra></extra>")
    fig1.update_layout(height=300, xaxis_title="", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

with col2:
    st.markdown(chart_container("Evoluciones vs pacientes únicos",
                "Comparativa de carga operativa por mes"), unsafe_allow_html=True)
    pac_mes = df_f.groupby("MES")["DOCUMENTO"].nunique().reset_index(name="Pacientes")
    pac_mes["Mes"] = pac_mes["MES"].apply(mes_label)
    evol2 = evol_mes[["Mes","Evoluciones"]].merge(pac_mes[["Mes","Pacientes"]], on="Mes")
    fig2 = go.Figure()
    fig2.add_bar(x=evol2["Mes"], y=evol2["Evoluciones"], name="Evoluciones",
                 marker=dict(color=C["blue"], cornerradius=4),
                 hovertemplate="%{y:,} evoluciones<extra></extra>")
    fig2.add_bar(x=evol2["Mes"], y=evol2["Pacientes"], name="Pacientes",
                 marker=dict(color=C["teal"], cornerradius=4),
                 hovertemplate="%{y:,} pacientes<extra></extra>")
    fig2.update_layout(barmode="group", height=300, bargap=0.25,
                       legend=dict(orientation="h", y=1.1, x=0, font=dict(size=11)))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICAS — FILA 2 (ancha)
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(chart_container("Evoluciones por área terapéutica",
            "Tendencia mensual desglosada por cada área de servicio"), unsafe_allow_html=True)
area_mes = df_f.groupby(["AREA","MES"]).size().reset_index(name="Evoluciones")
area_mes["Mes"] = area_mes["MES"].apply(mes_label)
fig3 = go.Figure()
for area_name in sorted(area_mes["AREA"].unique()):
    sub = area_mes[area_mes["AREA"] == area_name]
    fig3.add_scatter(x=sub["Mes"], y=sub["Evoluciones"], mode="lines+markers",
                     name=area_name, line=dict(width=2.5, shape="spline",
                     color=AREA_COLORS.get(area_name, C["text3"])),
                     marker=dict(size=7),
                     hovertemplate=f"<b>{area_name}</b><br>"+"%{x}: %{y:,}<extra></extra>")
fig3.update_layout(height=340, legend=dict(orientation="h", y=-0.18, x=0),
                   hovermode="x unified")
st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
st.markdown(chart_close(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICAS — FILA 3
# ═══════════════════════════════════════════════════════════════════════════════
col3, col4 = st.columns(2)

with col3:
    st.markdown(chart_container("Top 10 profesionales",
                "Ranking por número de evoluciones atendidas"), unsafe_allow_html=True)
    top_prof = (df_f.groupby("PROFESIONAL-ATIENDE").size()
                    .reset_index(name="Evoluciones")
                    .sort_values("Evoluciones", ascending=True).tail(10))
    max_val = top_prof["Evoluciones"].max()
    colors4 = [f"rgba(46,134,171,{0.35 + 0.65*(v/max_val)})"
               for v in top_prof["Evoluciones"]]
    fig4 = go.Figure()
    fig4.add_bar(y=top_prof["PROFESIONAL-ATIENDE"], x=top_prof["Evoluciones"],
                 orientation="h", marker=dict(color=colors4, cornerradius=4),
                 text=top_prof["Evoluciones"].apply(lambda x: f"{x:,}"),
                 textposition="outside", textfont=dict(size=11, color=C["text2"]),
                 hovertemplate="<b>%{y}</b><br>%{x:,} evoluciones<extra></extra>")
    fig4.update_layout(height=360, xaxis=dict(visible=False),
                       yaxis=dict(tickfont=dict(size=11)))
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

with col4:
    st.markdown(chart_container("Actividad por día de semana",
                "Distribución de evoluciones en la semana"), unsafe_allow_html=True)
    dia_c = (df_f.groupby("DIA_ES").size().reindex(DIAS_ORD, fill_value=0)
                 .reset_index(name="Evoluciones").rename(columns={"DIA_ES":"Día"}))
    max_dia = dia_c["Evoluciones"].max()
    colors5 = [C["amber"] if v == max_dia else f"rgba(244,162,97,0.45)"
               for v in dia_c["Evoluciones"]]
    fig5 = go.Figure()
    fig5.add_bar(x=dia_c["Día"], y=dia_c["Evoluciones"],
                 marker=dict(color=colors5, cornerradius=4),
                 text=dia_c["Evoluciones"].apply(lambda x: f"{x:,}"),
                 textposition="outside", textfont=dict(size=11, color=C["text2"]),
                 hovertemplate="<b>%{x}</b><br>%{y:,} evoluciones<extra></extra>")
    fig5.update_layout(height=360, yaxis=dict(visible=False))
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICAS — FILA 4
# ═══════════════════════════════════════════════════════════════════════════════
col5, col6 = st.columns(2)

with col5:
    st.markdown(chart_container("Pacientes únicos por área",
                "Distribución de la cartera activa por área terapéutica"), unsafe_allow_html=True)
    pac_area = (df_f.drop_duplicates("DOCUMENTO").groupby("AREA").size()
                    .reset_index(name="Pacientes").sort_values("Pacientes", ascending=False))
    area_colors_list = [AREA_COLORS.get(a, C["text3"]) for a in pac_area["AREA"]]
    fig6 = go.Figure()
    fig6.add_pie(labels=pac_area["AREA"], values=pac_area["Pacientes"],
                 hole=0.55, marker=dict(colors=area_colors_list, line=dict(color=C["card"], width=2)),
                 textfont=dict(size=11, color=C["text1"]),
                 textinfo="label+percent", textposition="outside",
                 hovertemplate="<b>%{label}</b><br>%{value:,} pacientes (%{percent})<extra></extra>")
    fig6.update_layout(height=360, showlegend=False)
    st.plotly_chart(fig6, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

with col6:
    st.markdown(chart_container("Top 8 EPS por evoluciones",
                "Concentración de actividad por aseguradora"), unsafe_allow_html=True)
    top_eps = df_f["EPS"].value_counts().head(8).reset_index()
    top_eps.columns = ["Aseguradora", "Evoluciones"]
    top_eps = top_eps.sort_values("Evoluciones", ascending=True)
    max_eps = top_eps["Evoluciones"].max()
    colors7 = [f"rgba(123,104,238,{0.3 + 0.7*(v/max_eps)})"
               for v in top_eps["Evoluciones"]]
    fig7 = go.Figure()
    fig7.add_bar(y=top_eps["Aseguradora"], x=top_eps["Evoluciones"],
                 orientation="h", marker=dict(color=colors7, cornerradius=4),
                 text=top_eps["Evoluciones"].apply(lambda x: f"{x:,}"),
                 textposition="outside", textfont=dict(size=11, color=C["text2"]),
                 hovertemplate="<b>%{y}</b><br>%{x:,} evoluciones<extra></extra>")
    fig7.update_layout(height=360, xaxis=dict(visible=False),
                       yaxis=dict(tickfont=dict(size=10)))
    st.plotly_chart(fig7, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# GRÁFICAS — FILA 5
# ═══════════════════════════════════════════════════════════════════════════════
col7, col8 = st.columns(2)

with col7:
    st.markdown(chart_container("Distribución por edad y sexo",
                "Perfil demográfico de pacientes únicos"), unsafe_allow_html=True)
    RANGOS = ["0-5","6-10","11-18","19-30","31-50","50+"]
    bins = [0,5,10,18,30,50,120]
    dup_pac = df_f.drop_duplicates("DOCUMENTO").copy()
    dup_pac["RANGO"] = pd.cut(dup_pac["EDAD"], bins=bins, labels=RANGOS)
    edad_sexo = (dup_pac.groupby(["RANGO","SEXO"], observed=True).size()
                        .reset_index(name="Pacientes"))
    edad_sexo["RANGO"] = edad_sexo["RANGO"].astype(str)
    fig8 = go.Figure()
    for sexo, color, name in [("M", C["blue"], "Masculino"), ("F", C["coral"], "Femenino")]:
        sub = edad_sexo[edad_sexo["SEXO"] == sexo]
        fig8.add_bar(x=sub["RANGO"], y=sub["Pacientes"], name=name,
                     marker=dict(color=color, cornerradius=4),
                     hovertemplate=f"<b>{name}</b><br>"+"%{x}: %{y} pacientes<extra></extra>")
    fig8.update_layout(barmode="group", height=360, bargap=0.2,
                       legend=dict(orientation="h", y=1.08, x=0),
                       xaxis=dict(categoryorder="array", categoryarray=RANGOS))
    st.plotly_chart(fig8, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

with col8:
    st.markdown(chart_container("Intensidad de atención",
                "Pacientes agrupados por cantidad de sesiones en el período"), unsafe_allow_html=True)
    intens = df_f.groupby("DOCUMENTO").size()
    rangos_i = ["1 – 19", "20 – 49", "50 – 100", "Más de 100"]
    vals_i   = [int((intens < 20).sum()),
                int(((intens >= 20) & (intens < 50)).sum()),
                int(((intens >= 50) & (intens <= 100)).sum()),
                int((intens > 100).sum())]
    colors9 = [C["teal"], "rgba(27,153,139,0.7)", "rgba(27,153,139,0.45)", "rgba(27,153,139,0.25)"]
    fig9 = go.Figure()
    fig9.add_bar(x=rangos_i, y=vals_i,
                 marker=dict(color=colors9, cornerradius=4),
                 text=[f"{v}" for v in vals_i],
                 textposition="outside", textfont=dict(size=12, color=C["text2"]),
                 hovertemplate="<b>%{x}</b><br>%{y} pacientes<extra></extra>")
    fig9.update_layout(height=360, yaxis=dict(visible=False),
                       xaxis_title="Sesiones en el período")
    st.plotly_chart(fig9, use_container_width=True, config={"displayModeBar": False})
    st.markdown(chart_close(), unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer">
    Centro Terapéutico · Dashboard generado automáticamente desde archivo semestral
    · Última actualización: {date.today().strftime('%d/%m/%Y')}
</div>
""", unsafe_allow_html=True)
