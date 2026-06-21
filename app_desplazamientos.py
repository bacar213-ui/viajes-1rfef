import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math
import pandas as pd
from itertools import combinations

st.set_page_config(page_title="Distancias 1ª RFEF", layout="wide", page_icon="⚽")

TEAMS = {
    # ── GRUPO 1 ──────────────────────────────────────────────────────────────
    "Pontevedra CF":              {"lat": 42.438590, "lon": -8.641360, "stadium": "Estadio Municipal de Pasaron",         "city": "Pontevedra",        "provincia": "Pontevedra",         "grupo": 1},
    "Deportivo Fabril":           {"lat": 43.252470, "lon": -8.282840, "stadium": "Ciudad Deportiva de Abegondo",         "city": "Abegondo",          "provincia": "A Coruña",           "grupo": 1},
    "Racing Club Ferrol":         {"lat": 43.490726, "lon": -8.239403, "stadium": "Estadio Municipal de A Malata",        "city": "Ferrol",            "provincia": "A Coruña",           "grupo": 1},
    "UD Ourense":                 {"lat": 42.340650, "lon": -7.875730, "stadium": "Estadio de O Couto",                   "city": "Ourense",           "provincia": "Ourense",            "grupo": 1},
    "CD Lugo":                    {"lat": 43.003365, "lon": -7.570954, "stadium": "Estadio Anxo Carro",                   "city": "Lugo",              "provincia": "Lugo",               "grupo": 1},
    "Real Avilés Industrial":     {"lat": 43.557500, "lon": -5.930600, "stadium": "Estadio Roman Suarez Puerta",          "city": "Aviles",            "provincia": "Asturias",           "grupo": 1},
    "Barakaldo CF":               {"lat": 43.302103, "lon": -2.986659, "stadium": "Estadio de Lasesarre",                 "city": "Barakaldo",         "provincia": "Bizkaia/Vizcaya",    "grupo": 1},
    "Arenas Club":                {"lat": 43.331469, "lon": -3.006467, "stadium": "Campo Municipal de Gobela",            "city": "Getxo",             "provincia": "Bizkaia/Vizcaya",    "grupo": 1},
    "Athletic Club B":            {"lat": 43.277500, "lon": -2.839320, "stadium": "Lezama",                               "city": "Lezama",            "provincia": "Bizkaia/Vizcaya",    "grupo": 1},
    "Real Unión":                 {"lat": 43.345560, "lon": -1.785830, "stadium": "Stadium Gal",                          "city": "Irun",              "provincia": "Gipuzkoa/Guipúzcoa", "grupo": 1},
    "UD Logroñés":                {"lat": 42.452970, "lon": -2.453340, "stadium": "Estadio Las Gaunas",                   "city": "Logrono",           "provincia": "La Rioja",           "grupo": 1},
    "CD Mirandés":                {"lat": 42.680786, "lon": -2.935436, "stadium": "Estadio Municipal de Anduva",          "city": "Miranda de Ebro",   "provincia": "Burgos",             "grupo": 1},
    "CyD Leonesa":                {"lat": 42.587470, "lon": -5.577040, "stadium": "Estadio Reino de Leon",                "city": "Leon",              "provincia": "León",               "grupo": 1},
    "Unionistas de Salamanca CF": {"lat": 40.946684, "lon": -5.665987, "stadium": "Estadio Municipal Reina Sofia",        "city": "Salamanca",         "provincia": "Salamanca",          "grupo": 1},
    "CP Cacereño":                {"lat": 39.487130, "lon": -6.412350, "stadium": "Estadio Principe Felipe",              "city": "Caceres",           "provincia": "Cáceres",            "grupo": 1},
    "CD Coria":                   {"lat": 39.988190, "lon": -6.536300, "stadium": "Estadio La Isla",                      "city": "Coria",             "provincia": "Cáceres",            "grupo": 1},
    "AD Mérida":                  {"lat": 38.913933, "lon": -6.336406, "stadium": "Estadio Romano Jose Fouto",            "city": "Merida",            "provincia": "Badajoz",            "grupo": 1},
    "CD Extremadura":             {"lat": 38.684350, "lon": -6.414590, "stadium": "Estadio Francisco de la Hera",         "city": "Almendralejo",      "provincia": "Badajoz",            "grupo": 1},
    "SD Ponferradina":            {"lat": 42.557400, "lon": -6.599972, "stadium": "Estadio El Toralin",                   "city": "Ponferrada",        "provincia": "León",               "grupo": 1},
    "Zamora CF":                  {"lat": 41.486390, "lon": -5.748060, "stadium": "Estadio Ruta de la Plata",             "city": "Zamora",            "provincia": "Zamora",             "grupo": 1},
    # ── GRUPO 2 ──────────────────────────────────────────────────────────────
    "Real Zaragoza":              {"lat": 41.683664, "lon": -0.895446, "stadium": "Ibercaja Estadio (modular)",           "city": "Zaragoza",          "provincia": "Zaragoza",           "grupo": 2},
    "SD Huesca":                  {"lat": 42.131944, "lon": -0.424444, "stadium": "Estadio El Alcoraz",                   "city": "Huesca",            "provincia": "Huesca",             "grupo": 2},
    "CD Teruel":                  {"lat": 40.332050, "lon": -1.105860, "stadium": "Estadio de Pinilla",                   "city": "Teruel",            "provincia": "Teruel",             "grupo": 2},
    "Nàstic de Tarragona":        {"lat": 41.127003, "lon":  1.272830, "stadium": "Nou Estadi Costa Daurada",             "city": "Tarragona",         "provincia": "Tarragona",          "grupo": 2},
    "UE Sant Andreu":             {"lat": 41.428836, "lon":  2.193047, "stadium": "Estadio Narcis Sala",                  "city": "Barcelona",         "provincia": "Barcelona",          "grupo": 2},
    "CE Europa":                  {"lat": 41.411800, "lon":  2.161500, "stadium": "Nou Sardenya",                         "city": "Barcelona",         "provincia": "Barcelona",          "grupo": 2},
    "UD Ibiza":                   {"lat": 38.913780, "lon":  1.415090, "stadium": "Estadio Can Misses",                   "city": "Ibiza",             "provincia": "Illes Balears",      "grupo": 2},
    "AD Alcorcon":                {"lat": 40.338889, "lon": -3.840556, "stadium": "Estadio Santo Domingo",                "city": "Alcorcon",          "provincia": "Madrid",             "grupo": 2},
    "Rayo Majadahonda":           {"lat": 40.457558, "lon": -3.860309, "stadium": "Estadio Cerro del Espino",             "city": "Majadahonda",       "provincia": "Madrid",             "grupo": 2},
    "Atlético de Madrid B":       {"lat": 40.481400, "lon": -3.330500, "stadium": "Centro Deportivo Alcala de Henares",   "city": "Alcala de Henares", "provincia": "Madrid",             "grupo": 2},
    "Real Madrid Castilla":       {"lat": 40.476856, "lon": -3.614287, "stadium": "Estadio Alfredo Di Stefano",           "city": "Madrid",            "provincia": "Madrid",             "grupo": 2},
    "Hércules CF":                {"lat": 38.357204, "lon": -0.492754, "stadium": "Estadio Jose Rico Perez",              "city": "Alicante",          "provincia": "Alacant/Alicante",   "grupo": 2},
    "Villarreal B":               {"lat": 39.939487, "lon": -0.114498, "stadium": "Ciudad Deportiva Jose Manuel Llaneza", "city": "Vila-real",         "provincia": "Castelló/Castellón", "grupo": 2},
    "FC Cartagena":               {"lat": 37.609746, "lon": -0.995977, "stadium": "Estadio Cartagonova",                  "city": "Cartagena",         "provincia": "Murcia",             "grupo": 2},
    "Real Murcia CF":             {"lat": 38.042250, "lon": -1.144730, "stadium": "Estadio Enrique Roca de Murcia",       "city": "Murcia",            "provincia": "Murcia",             "grupo": 2},
    "Águilas FC":                 {"lat": 37.404300, "lon": -1.590040, "stadium": "Estadio El Rubial",                    "city": "Aguilas",           "provincia": "Murcia",             "grupo": 2},
    "Antequera CF":               {"lat": 37.020600, "lon": -4.559368, "stadium": "Estadio El Mauli",                     "city": "Antequera",         "provincia": "Málaga",             "grupo": 2},
    "Algeciras CF":               {"lat": 36.163333, "lon": -5.465280, "stadium": "Estadio Nuevo Mirador",                "city": "Algeciras",         "provincia": "Cádiz",              "grupo": 2},
    "CD Torremolinos":            {"lat": 36.621460, "lon": -4.509930, "stadium": "Campo de Futbol El Pozuelo",           "city": "Torremolinos",      "provincia": "Málaga",             "grupo": 2},
    "Real Jaén CF":               {"lat": 37.776159, "lon": -3.786839, "stadium": "Estadio Municipal La Victoria",        "city": "Jaen",              "provincia": "Jaén",               "grupo": 2},
}

GRUPO_COLORS = {1: "#1a6fb5", 2: "#c0392b"}
IBIZA = "UD Ibiza"

# Puertos peninsulares y su puerto de llegada en Ibiza
# Gandia  → Sant Antoni de Portmany
# Dénia   → Eivissa (puerto de Ibiza ciudad)
RUTAS_FERRY = [
    {
        "origen_nombre": "Gandia",
        "origen":  {"lat": 38.9960, "lon": -0.1540},  # muelle ferry Gandia
        "destino_nombre": "Sant Antoni de Portmany",
        "destino": {"lat": 38.9808, "lon":  1.2980},  # muelle Sant Antoni
        "ferry_km": 108,
        # waypoints que rodean la isla de Conejera por el norte
        "waypoints": [[39.00499773748464, 1.2106378435059044]],
    },
    {
        "origen_nombre": "Dénia",
        "origen":  {"lat": 38.8390, "lon":  0.1140},  # muelle ferry Dénia
        "destino_nombre": "Eivissa (puerto)",
        "destino": {"lat": 38.9040, "lon":  1.4420},  # muelle Eivissa
        "ferry_km": 90,
        # waypoints que rodean la isla de Conejera por el norte
        "waypoints": [[38.80959953974597, 1.4141062763630279]],
    },
]

# ── DATOS PRECALCULADOS DE RÉCORDS (hardcoded) ───────────────────────────────
RECORDS = {
    1: {
        "top3_largos": [
            {"eq_a": "Real Unión", "eq_b": "CD Extremadura", "km": 774, "ferry": False, "puerto_orig": None, "puerto_dest": None},
            {"eq_a": "Racing Club Ferrol", "eq_b": "CD Extremadura", "km": 773, "ferry": False, "puerto_orig": None, "puerto_dest": None},
            {"eq_a": "Pontevedra CF", "eq_b": "Real Unión", "km": 755, "ferry": False, "puerto_orig": None, "puerto_dest": None},
        ],
        "top3_cortos": [
            {"eq_a": "Barakaldo CF", "eq_b": "Arenas Club", "km": 11},
            {"eq_a": "Barakaldo CF", "eq_b": "Athletic Club B", "km": 17},
            {"eq_a": "Arenas Club", "eq_b": "Athletic Club B", "km": 18},
        ],
        "eq_mas": "CD Extremadura", "km_mas": 10273,
        "eq_menos": "CyD Leonesa", "km_menos": 5865,
        "km_totales": [
            ("CD Extremadura", 10273), ("AD Mérida", 9812), ("Real Unión", 9109),
            ("CP Cacereño", 8700), ("Pontevedra CF", 8482), ("Racing Club Ferrol", 8393),
            ("CD Coria", 8236), ("Deportivo Fabril", 8086), ("UD Logroñés", 7779),
            ("UD Ourense", 7688), ("Athletic Club B", 7667), ("Arenas Club", 7604),
            ("Barakaldo CF", 7557), ("CD Mirandés", 7146), ("CD Lugo", 7142),
            ("Real Avilés Industrial", 6737), ("SD Ponferradina", 6355),
            ("Unionistas de Salamanca CF", 6348), ("Zamora CF", 5913), ("CyD Leonesa", 5865),
        ],
    },
    2: {
        "top3_largos": [
            {"eq_a": "UE Sant Andreu", "eq_b": "Algeciras CF", "km": 1104, "ferry": False, "puerto_orig": None, "puerto_dest": None},
            {"eq_a": "CE Europa", "eq_b": "Algeciras CF", "km": 1091, "ferry": False, "puerto_orig": None, "puerto_dest": None},
            {"eq_a": "SD Huesca", "eq_b": "Algeciras CF", "km": 1031, "ferry": False, "puerto_orig": None, "puerto_dest": None},
        ],
        "top3_cortos": [
            {"eq_a": "UE Sant Andreu", "eq_b": "CE Europa", "km": 5},
            {"eq_a": "AD Alcorcon", "eq_b": "Rayo Majadahonda", "km": 18},
            {"eq_a": "Rayo Majadahonda", "eq_b": "Real Madrid Castilla", "km": 28},
        ],
        "eq_mas": "Algeciras CF", "km_mas": 13027,
        "eq_menos": "Real Murcia CF", "km_menos": 7142,
        "km_totales": [
            ("Algeciras CF", 13027), ("CD Torremolinos", 10906), ("UE Sant Andreu", 10814),
            ("CE Europa", 10638), ("Antequera CF", 10108), ("SD Huesca", 9523),
            ("Nàstic de Tarragona", 9315), ("UD Ibiza", 9274), ("Real Jaén CF", 8637),
            ("Real Zaragoza", 8600), ("Águilas FC", 8137), ("Rayo Majadahonda", 7910),
            ("FC Cartagena", 7782), ("AD Alcorcon", 7748), ("Atlético de Madrid B", 7627),
            ("Real Madrid Castilla", 7621), ("Villarreal B", 7469), ("CD Teruel", 7427),
            ("Hércules CF", 7287), ("Real Murcia CF", 7142),
        ],
    },
}

# Estadio Can Misses (destino final en Ibiza)
IBIZA_ESTADIO = TEAMS[IBIZA]

GEOJSON_URL = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/spain-provinces.geojson"

@st.cache_data(show_spinner=False)
def load_geojson():
    try:
        r = requests.get(GEOJSON_URL, timeout=15)
        return r.json()
    except Exception:
        return None

@st.cache_data(show_spinner=False)
def get_osrm_route(lon1, lat1, lon2, lat2):
    url = (
        f"http://router.project-osrm.org/route/v1/driving/"
        f"{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    )
    try:
        r = requests.get(url, timeout=15)
        data = r.json()
        if data.get("code") == "Ok":
            route = data["routes"][0]
            km = round(route["distance"] / 1000)
            path = [[c[1], c[0]] for c in route["geometry"]["coordinates"]]
            return path, km
    except Exception:
        pass
    return None, None

def haversine(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    return round(2 * 6371 * math.asin(math.sqrt(a)) * 1.3)

def mejor_ruta_con_ibiza(lat_tierra, lon_tierra, hacia_ibiza=True):
    """
    Prueba las dos rutas ferry (Gandia→Sant Antoni, Dénia→Eivissa) y elige la más corta.
    Devuelve:
      path_tierra, path_ibiza, km_total, ruta_ferry_dict, km_carr_tierra, km_carr_ibiza
    """
    mejor = None
    for ruta in RUTAS_FERRY:
        po = ruta["origen"]   # puerto peninsular
        pd = ruta["destino"]  # puerto ibicenco

        if hacia_ibiza:
            # tierra → puerto peninsular
            p1, km1 = get_osrm_route(lon_tierra, lat_tierra, po["lon"], po["lat"])
            if km1 is None:
                km1 = haversine(lat_tierra, lon_tierra, po["lat"], po["lon"]); p1 = None
            # puerto ibicenco → estadio Can Misses
            p2, km2 = get_osrm_route(pd["lon"], pd["lat"],
                                     IBIZA_ESTADIO["lon"], IBIZA_ESTADIO["lat"])
            if km2 is None:
                km2 = haversine(pd["lat"], pd["lon"],
                                IBIZA_ESTADIO["lat"], IBIZA_ESTADIO["lon"]); p2 = None
        else:
            # estadio Can Misses → puerto ibicenco
            p1, km1 = get_osrm_route(IBIZA_ESTADIO["lon"], IBIZA_ESTADIO["lat"],
                                     pd["lon"], pd["lat"])
            if km1 is None:
                km1 = haversine(IBIZA_ESTADIO["lat"], IBIZA_ESTADIO["lon"],
                                pd["lat"], pd["lon"]); p1 = None
            # puerto peninsular → destino tierra
            p2, km2 = get_osrm_route(po["lon"], po["lat"], lon_tierra, lat_tierra)
            if km2 is None:
                km2 = haversine(po["lat"], po["lon"], lat_tierra, lon_tierra); p2 = None

        km_total = km1 + ruta["ferry_km"] + km2

        if mejor is None or km_total < mejor["km_total"]:
            mejor = {
                "km_total": km_total,
                "ruta_ferry": ruta,
                "path_tierra": p1,
                "path_ibiza":  p2,
                "km_carr_tierra": km1,
                "km_carr_ibiza":  km2,
            }
    return mejor

def color_from_km(km):
    ratio = min(km / 1200, 1.0)
    r = int(50 + 200 * ratio)
    g = int(210 - 160 * ratio)
    return f"#{r:02x}{g:02x}50"

# Colores fijos por grupo para provincias con equipo
GRUPO_PROV_COLOR = {
    1: "#a8c8f0",   # azul claro grupo 1
    2: "#f0a8a8",   # rojo claro grupo 2
}
PROV_EMPTY_COLOR = "#f0f0f0"

@st.cache_data(show_spinner=False)
def calcular_todas_distancias_grupo(grupo):
    equipos = [k for k, v in TEAMS.items() if v["grupo"] == grupo]
    resultados = []
    for a, b in combinations(equipos, 2):
        ta, tb = TEAMS[a], TEAMS[b]
        if a == IBIZA or b == IBIZA:
            eq_tierra = a if b == IBIZA else b
            t = TEAMS[eq_tierra]
            res = mejor_ruta_con_ibiza(t["lat"], t["lon"], hacia_ibiza=True)
            resultados.append({"eq_a": a, "eq_b": b, "km": res["km_total"], "ferry": True,
                                "puerto_orig": res["ruta_ferry"]["origen_nombre"],
                                "puerto_dest": res["ruta_ferry"]["destino_nombre"]})
        else:
            _, km = get_osrm_route(ta["lon"], ta["lat"], tb["lon"], tb["lat"])
            if km is None: km = haversine(ta["lat"], ta["lon"], tb["lat"], tb["lon"])
            resultados.append({"eq_a": a, "eq_b": b, "km": km, "ferry": False,
                                "puerto_orig": None, "puerto_dest": None})
    return resultados

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
st.sidebar.title("⚽ 1ª RFEF 2026/27")
st.sidebar.markdown("---")
grupo_sel = st.sidebar.radio("🏆 Selecciona grupo", options=[1, 2],
    format_func=lambda x: f"Grupo {x} — {'Norte/Oeste' if x==1 else 'Sur/Este'}", index=0)
equipos_grupo = sorted([k for k, v in TEAMS.items() if v["grupo"] == grupo_sel])
equipo_ref = st.sidebar.selectbox(f"📍 Equipo del Grupo {grupo_sel}", options=equipos_grupo)
st.sidebar.markdown("---")
ver_records = st.sidebar.checkbox("🏅 Mostrar Records del grupo", value=False)

# ── TÍTULO ────────────────────────────────────────────────────────────────────
color_grupo = GRUPO_COLORS[grupo_sel]
city_ref = ref["city"]
st.markdown(f"<h2 style='color:{color_grupo};'>Grupo {grupo_sel} — Distancias para el <em>{equipo_ref}</em> desde {city_ref}</h2>",
            unsafe_allow_html=True)
ref = TEAMS[equipo_ref]

# ── CALCULAR RUTAS ────────────────────────────────────────────────────────────
with st.spinner("Calculando rutas..."):
    rutas = {}
    for nombre in equipos_grupo:
        if nombre == equipo_ref: continue
        t = TEAMS[nombre]
        if equipo_ref == IBIZA or nombre == IBIZA:
            hacia_ibiza = (nombre == IBIZA)
            lat_t = ref["lat"] if hacia_ibiza else t["lat"]
            lon_t = ref["lon"] if hacia_ibiza else t["lon"]
            res = mejor_ruta_con_ibiza(lat_t, lon_t, hacia_ibiza)
            rutas[nombre] = {"km": res["km_total"], "ferry": res, "path": None}
        else:
            path, km = get_osrm_route(ref["lon"], ref["lat"], t["lon"], t["lat"])
            if path is None: km = haversine(ref["lat"], ref["lon"], t["lat"], t["lon"])
            rutas[nombre] = {"km": km, "ferry": None, "path": path}

# ── AVISO FERRY ───────────────────────────────────────────────────────────────
tiene_ferry = any(v["ferry"] for v in rutas.values())
if equipo_ref == IBIZA:
    st.info("⛴️ **UD Ibiza** juega en isla. Cada ruta usa el puerto óptimo según destino: "
            "**Gandia → Sant Antoni** o **Dénia → Eivissa**. El total incluye los tres tramos.")
elif tiene_ferry:
    r_f = rutas[IBIZA]["ferry"]
    rf  = r_f["ruta_ferry"]
    st.info(
        f"⛴️ Ruta a **UD Ibiza** via **{rf['origen_nombre']} → {rf['destino_nombre']}**:  \n"
        f"🚗 {equipo_ref} → {rf['origen_nombre']}: **{r_f['km_carr_tierra']} km** · "
        f"⛴️ Ferry: **{rf['ferry_km']} km** · "
        f"🚗 {rf['destino_nombre']} → Can Misses: **{r_f['km_carr_ibiza']} km** · "
        f"**Total: {r_f['km_total']} km**"
    )

# ── MAPA ──────────────────────────────────────────────────────────────────────
m = folium.Map(location=[ref["lat"], ref["lon"]], zoom_start=6, tiles="CartoDB positron")

geojson_data = load_geojson()
if geojson_data:
    # Provincias por grupo (independiente del equipo seleccionado)
    prov_grupo = {}
    for v in TEAMS.values():
        prov = v["provincia"]
        g = v["grupo"]
        # Si una provincia tiene equipos en ambos grupos, priorizar el grupo activo
        if prov not in prov_grupo:
            prov_grupo[prov] = g
        elif prov_grupo[prov] != g:
            prov_grupo[prov] = grupo_sel  # conflicto: usar color del grupo activo

    for feature in geojson_data.get("features", []):
        pname = feature["properties"].get("name", "")
        g = prov_grupo.get(pname)
        color = GRUPO_PROV_COLOR.get(g, PROV_EMPTY_COLOR)
        opacity = 0.5 if g else 0.15
        folium.GeoJson(feature, style_function=lambda f, c=color, o=opacity: {
            "fillColor": c, "color": "#aaa", "weight": 0.5, "fillOpacity": o
        }).add_to(m)

for nombre, info in rutas.items():
    t = TEAMS[nombre]
    lc = color_from_km(info["km"])
    if info["ferry"]:
        res = info["ferry"]
        rf  = res["ruta_ferry"]
        po  = rf["origen"]   # puerto peninsular
        pd_ = rf["destino"]  # puerto ibicenco

        # Tramo 1: carretera tierra → puerto peninsular (o viceversa)
        if res["path_tierra"]:
            folium.PolyLine(res["path_tierra"], color=lc, weight=3, opacity=0.8,
                            tooltip=f"🚗 Carretera → {rf['origen_nombre']}").add_to(m)
        # Tramo 2: ferry (línea discontinua azul marina con waypoints para rodear Conejera)
        ferry_coords = ([[po["lat"], po["lon"]]] +
                        rf.get("waypoints", []) +
                        [[pd_["lat"], pd_["lon"]]])
        folium.PolyLine(
            ferry_coords,
            color="#1a5276", weight=2, opacity=0.9, dash_array="7 5",
            tooltip=f"⛴️ Ferry {rf['origen_nombre']}→{rf['destino_nombre']}: {rf['ferry_km']} km"
        ).add_to(m)
        # Tramo 3: carretera puerto ibicenco → estadio (o viceversa)
        if res["path_ibiza"]:
            folium.PolyLine(res["path_ibiza"], color=lc, weight=3, opacity=0.8,
                            tooltip=f"🚗 {rf['destino_nombre']} → Can Misses").add_to(m)

        # Marcadores de puertos
        for p_info, p_nombre in [(po, rf["origen_nombre"]), (pd_, rf["destino_nombre"])]:
            folium.Marker(
                [p_info["lat"], p_info["lon"]],
                tooltip=f"⛴️ Puerto de {p_nombre}",
                icon=folium.DivIcon(
                    html='<div style="font-size:20px;line-height:1;">⛴️</div>',
                    icon_size=(24, 24), icon_anchor=(12, 12)
                )
            ).add_to(m)
    else:
        if info["path"]:
            folium.PolyLine(info["path"], color=lc, weight=3, opacity=0.75,
                            tooltip=f"{nombre}: {info['km']} km").add_to(m)

# Marcadores de equipos
for nombre in equipos_grupo:
    t = TEAMS[nombre]
    es_origen = (nombre == equipo_ref)
    if es_origen:
        icon = folium.Icon(color="orange", icon="home")
        tooltip_txt = f"🏠 {nombre} (origen)"
    else:
        info = rutas[nombre]
        color_hex = GRUPO_COLORS[grupo_sel]
        badge = f"⛴️ {info['km']} km" if info["ferry"] else f"{info['km']} km"
        icon = folium.DivIcon(
            html=f'<div style="background:{color_hex};color:#fff;font-size:10px;'
                 f'padding:2px 5px;border-radius:4px;white-space:nowrap;font-weight:bold;">{badge}</div>',
            icon_size=(75, 20), icon_anchor=(37, 10)
        )
        tooltip_txt = f"{nombre} · {info['km']} km" + (" ⛴️" if info["ferry"] else "")

    popup_lines = [f"<b>{nombre}</b>", f"🏟️ {t['stadium']}", f"📍 {t['city']} ({t['provincia']})"]
    if not es_origen:
        info = rutas[nombre]
        if info["ferry"]:
            res = info["ferry"]; rf = res["ruta_ferry"]
            popup_lines += [
                f"🚗 Hasta {rf['origen_nombre']}: {res['km_carr_tierra']} km",
                f"⛴️ Ferry {rf['origen_nombre']}→{rf['destino_nombre']}: {rf['ferry_km']} km",
                f"🚗 {rf['destino_nombre']}→Can Misses: {res['km_carr_ibiza']} km",
                f"<b>Total: {res['km_total']} km</b>",
            ]
        else:
            popup_lines.append(f"🛣️ {info['km']} km desde {equipo_ref}")
    folium.Marker(
        location=[t["lat"], t["lon"]],
        popup=folium.Popup("<br>".join(popup_lines), max_width=270),
        tooltip=tooltip_txt,
        icon=icon
    ).add_to(m)

st_folium(m, use_container_width=True, height=580)

# ── TABLA ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader(f"📊 Todas las distancias desde {equipo_ref}")
filas = []
for nombre, info in rutas.items():
    t = TEAMS[nombre]
    if info["ferry"]:
        res = info["ferry"]; rf = res["ruta_ferry"]
        desglose = (f"🚗 {res['km_carr_tierra']} km (→{rf['origen_nombre']}) + "
                    f"⛴️ {rf['ferry_km']} km + "
                    f"🚗 {res['km_carr_ibiza']} km (→Can Misses)")
    else:
        desglose = "carretera" if info["path"] else "estimada"
    filas.append({"Equipo rival": nombre, "Ciudad": t["city"], "Km": info["km"], "Desglose": desglose})

df = pd.DataFrame(filas).sort_values("Km", ascending=False).reset_index(drop=True)
df.index += 1
c1, c2, c3 = st.columns(3)
c1.metric("Desplazamiento máximo", f"{df['Km'].max()} km", df.iloc[0]["Equipo rival"])
c2.metric("Desplazamiento mínimo", f"{df['Km'].min()} km", df.iloc[-1]["Equipo rival"])
c3.metric("Media del grupo", f"{int(df['Km'].mean())} km")
st.dataframe(df, use_container_width=True)

# ── RECORDS ───────────────────────────────────────────────────────────────────
if ver_records:
    st.markdown("---")
    st.markdown(f"## 🏅 Récords — Grupo {grupo_sel}")
    st.caption("Distancias calculadas por OSRM. Rutas con UD Ibiza incluyen 3 tramos: carretera + ferry + carretera en isla.")
    rec = RECORDS[grupo_sel]

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### 🔴 Top 3 viajes más largos")
        for i, row in enumerate(rec["top3_largos"]):
            extra = f" ⛴️ ({row['puerto_orig']}→{row['puerto_dest']})" if row["ferry"] else ""
            st.markdown(f"**{i+1}.** {row['eq_a']} → {row['eq_b']}{extra}  \n&nbsp;&nbsp;&nbsp;&nbsp;`{row['km']} km`")
        st.markdown("#### 🟢 Top 3 viajes más cortos")
        for row in rec["top3_cortos"]:
            st.markdown(f"- {row['eq_a']} → {row['eq_b']}  \n&nbsp;&nbsp;&nbsp;&nbsp;`{row['km']} km`")

    with col_r:
        st.markdown("#### 🧳 Equipo que más km recorre en total")
        st.markdown(f"**{rec['eq_mas']}**  \n`{rec['km_mas']:,} km`")
        st.markdown("#### 🏡 Equipo que menos km recorre en total")
        st.markdown(f"**{rec['eq_menos']}**  \n`{rec['km_menos']:,} km`")
        st.markdown("#### 📋 Km totales por equipo")
        df_km = pd.DataFrame(rec["km_totales"], columns=["Equipo", "Km totales"])
        df_km.index += 1
        st.dataframe(df_km, use_container_width=True)
