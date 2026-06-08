import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math

st.set_page_config(page_title="Distancias 1ª RFEF", layout="wide", page_icon="⚽")

TEAMS = {
    "Pontevedra CF":              {"lat": 42.438590, "lon": -8.641360, "stadium": "Estadio Municipal de Pasarón",    "city": "Pontevedra"},
    "Barakaldo CF":               {"lat": 43.302103, "lon": -2.986659, "stadium": "Estadio de Lasesarre",            "city": "Barakaldo"},
    "Unionistas de Salamanca CF": {"lat": 40.946684, "lon": -5.665987, "stadium": "Estadio Municipal Reina Sofía",   "city": "Salamanca"},
    "CD Lugo":                    {"lat": 43.003365, "lon": -7.570954, "stadium": "Estadio Anxo Carro",              "city": "Lugo"},
    "AD Mérida":                  {"lat": 38.913933, "lon": -6.336406, "stadium": "Estadio Romano José Fouto",      "city": "Mérida"},
    "Arenas Club":                {"lat": 43.331469, "lon": -3.006467, "stadium": "Campo Municipal de Gobela",       "city": "Getxo"},
    "Racing Club Ferrol":         {"lat": 43.490726, "lon": -8.239403, "stadium": "Estadio Municipal de A Malata",   "city": "Ferrol"},
    "Athletic Club 'B'":          {"lat": 43.277500, "lon": -2.839320, "stadium": "Lezama",                          "city": "Lezama"},
    "Real Avilés Industrial":     {"lat": 43.557500, "lon": -5.930600, "stadium": "Estadio Román Suárez Puerta",     "city": "Avilés"},
    "CP Cacereño":                {"lat": 39.487130, "lon": -6.412350, "stadium": "Estadio Príncipe Felipe",         "city": "Cáceres"},
    "FC Cartagena":               {"lat": 37.609746, "lon": -0.995977, "stadium": "Estadio Cartagonova",             "city": "Cartagena"},
    "Antequera CF":               {"lat": 37.020600, "lon": -4.559368, "stadium": "Estadio El Maulí",                "city": "Antequera"},
    "Algeciras CF":               {"lat": 36.163333, "lon": -5.465280, "stadium": "Estadio Nuevo Mirador",           "city": "Algeciras"},
    "Hércules CF":                {"lat": 38.357204, "lon": -0.492754, "stadium": "Estadio José Rico Pérez",         "city": "Alicante"},
    "Real Murcia CF":             {"lat": 38.042250, "lon": -1.144730, "stadium": "Estadio Enrique Roca de Murcia",  "city": "Murcia"},
    "AD Alcorcón":                {"lat": 40.338889, "lon": -3.840556, "stadium": "Estadio Santo Domingo",           "city": "Alcorcón"},
    "UD Ibiza":                   {"lat": 38.913780, "lon":  1.415090, "stadium": "Estadio Can Misses",              "city": "Ibiza"},
    "CD Teruel":                  {"lat": 40.332050, "lon": -1.105860, "stadium": "Estadio de Pinilla",              "city": "Teruel"},
    "Nàstic de Tarragona":        {"lat": 41.127003, "lon":  1.272830, "stadium": "Nou Estadi Costa Daurada",        "city": "Tarragona"},
    "CD Torremolinos":            {"lat": 36.621460, "lon": -4.509930, "stadium": "Campo de Fútbol El Pozuelo",      "city": "Torremolinos"},
    "Real Zaragoza":              {"lat": 41.683664, "lon": -0.895446, "stadium": "Ibercaja Estadio (modular)",      "city": "Zaragoza"},
    "SD Huesca":                  {"lat": 42.131944, "lon": -0.424444, "stadium": "Estadio El Alcoraz",              "city": "Huesca"},
    "CyD Leonesa":                {"lat": 42.587470, "lon": -5.577040, "stadium": "Estadio Reino de León",           "city": "León"},
    "Deportivo Fabril":           {"lat": 43.252470, "lon": -8.282840, "stadium": "Ciudad Deportiva de Abegondo",    "city": "Abegondo"},
    "Real Unión":                 {"lat": 43.345560, "lon": -1.785830, "stadium": "Stadium Gal",                     "city": "Irún"},
    "UE Sant Andreu":             {"lat": 41.428836, "lon":  2.193047, "stadium": "Estadio Narcís Sala",             "city": "Barcelona"},
    "CD Extremadura":             {"lat": 38.684350, "lon": -6.414590, "stadium": "Estadio Francisco de la Hera",    "city": "Almendralejo"},
    "Rayo Majadahonda":           {"lat": 40.457558, "lon": -3.860309, "stadium": "Estadio Cerro del Espino",        "city": "Majadahonda"},
    "CD Mirandés":               {"lat": 42.680786, "lon": -2.935436, "stadium": "Estadio Municipal de Anduva",    "city": "Miranda de Ebro"},
    "UD Ourense":                 {"lat": 42.340650, "lon": -7.875730, "stadium": "Estadio de O Couto",              "city": "Ourense"},
    "UD Logroñés":               {"lat": 42.452970, "lon": -2.453340, "stadium": "Estadio Las Gaunas",             "city": "Logroño"},
    "Águilas FC":                 {"lat": 37.404300, "lon": -1.590040, "stadium": "Estadio El Rubial",               "city": "Águilas"},
    "Real Jaén CF":               {"lat": 37.776159, "lon": -3.786839, "stadium": "Estadio Municipal La Victoria",  "city": "Jaén"},
    "CD Coria":                   {"lat": 39.988190, "lon": -6.536300, "stadium": "Estadio La Isla",                 "city": "Coria"},
}

SHIELDS = {
    "AD Alcorcón":   "https://upload.wikimedia.org/wikipedia/en/thumb/3/32/AD_Alcorcon_crest.png/50px-AD_Alcorcon_crest.png",
    "AD Mérida":     "https://upload.wikimedia.org/wikipedia/en/thumb/3/3e/M%C3%A9rida_AD_logo.png/50px-M%C3%A9rida_AD_logo.png",
    "Águilas FC":    "https://upload.wikimedia.org/wikipedia/en/thumb/a/a0/Aguilas_FC.png/50px-Aguilas_FC.png",
    "Algeciras CF":  "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/Algeciras_CF_logo.svg/50px-Algeciras_CF_logo.svg.png",
    "Antequera CF":  "https://upload.wikimedia.org/wikipedia/en/thumb/1/16/Antequera_CF_logo.svg/50px-Antequera_CF_logo.svg.png",
}

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

def haversine_fallback(lat1, lon1, lat2, lon2):
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2)
    return round(2 * 6371 * math.asin(math.sqrt(a)) * 1.3)

def color_from_ratio(ratio):
    r = int(50 + 200 * ratio)
    g = int(210 - 160 * ratio)
    return f"#{r:02x}{g:02x}50"

def shield_marker_html(team_name, km=None):
    km_label = (
        f'<div style="font-size:8px;font-weight:bold;color:#1a252f;text-align:center;'
        f'background:rgba(255,255,255,0.85);border-radius:3px;padding:0 3px;margin-top:1px">'
        f'{km} km</div>'
    ) if km else ""
    if team_name in SHIELDS:
        return (
            f'<div style="text-align:center">'
            f'<img src="{SHIELDS[team_name]}" style="width:32px;height:32px;object-fit:contain;'
            f'background:white;border-radius:50%;border:2px solid #2980b9;'
            f'box-shadow:0 1px 4px rgba(0,0,0,0.3)">'
            f'{km_label}</div>'
        )
    else:
        return (
            f'<div style="text-align:center">'
            f'<div style="width:14px;height:14px;background:#2980b9;border-radius:50%;'
            f'border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3);margin:0 auto"></div>'
            f'{km_label}</div>'
        )

st.markdown(
    "<style>[data-testid='metric-container']{"
    "background:#f8f9fa;border-radius:10px;padding:12px 16px;"
    "border:1px solid #e9ecef;}</style>",
    unsafe_allow_html=True
)

st.title("⚽ Herramienta de Desplazamientos — 1ª RFEF 2026/27")
st.caption("34 equipos confirmados · Rutas reales por carretera (OSRM/OpenStreetMap) · Coordenadas verificadas")

team_names = sorted(TEAMS.keys())

def label(name):
    d = TEAMS[name]
    return f"{name}  —  {d['stadium']} ({d['city']})"

selected = st.selectbox("🔍 Selecciona un equipo", team_names, format_func=label)

if selected and selected in SHIELDS:
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px">'
        f'<img src="{SHIELDS[selected]}" style="height:48px;object-fit:contain">'
        f'<span style="font-size:1.1rem;font-weight:600">{selected} — {TEAMS[selected]["city"]}</span>'
        f'</div>',
        unsafe_allow_html=True
    )

if selected:
    sel_city    = TEAMS[selected]["city"]
    sel_stadium = TEAMS[selected]["stadium"]
    rivals = [t for t in team_names if t != selected]

    progress = st.progress(0, text="Calculando rutas por carretera...")
    trips = []
    for i, rival in enumerate(rivals):
        s  = TEAMS[selected]
        rv = TEAMS[rival]
        path, km = get_osrm_route(s["lon"], s["lat"], rv["lon"], rv["lat"])
        if km is None:
            km   = haversine_fallback(s["lat"], s["lon"], rv["lat"], rv["lon"])
            path = [[s["lat"], s["lon"]], [rv["lat"], rv["lon"]]]
        trips.append({
            "rival": rival,
            "rival_city": rv["city"],
            "km": km,
            "stadium": rv["stadium"],
            "path": path
        })
        progress.progress((i + 1) / len(rivals), text=f"Calculando rutas… {i+1}/{len(rivals)}")
    progress.empty()

    total_km = sum(t["km"] for t in trips)
    avg_km   = total_km / len(trips)
    shortest = min(trips, key=lambda x: x["km"])
    longest  = max(trips, key=lambda x: x["km"])
    km_min   = shortest["km"]
    km_max   = longest["km"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📏 Total km (visitante)", f"{total_km:,} km")
    c2.metric("📊 Media por viaje", f"{avg_km:,.0f} km")
    c3.metric(
        "🟢 Desplazamiento más corto",
        f"{shortest['rival_city']}  —  {km_min} km",
        delta=shortest["rival"], delta_color="off"
    )
    c4.metric(
        "🔴 Desplazamiento más largo",
        f"{longest['rival_city']}  —  {km_max} km",
        delta=longest["rival"], delta_color="off"
    )

    st.markdown("---")
    col_map, col_table = st.columns([3, 2])

    with col_map:
        st.subheader(f"🗺️ Desplazamientos desde {sel_city}")
        m = folium.Map(location=[40.4, -3.5], zoom_start=5, tiles="CartoDB positron")

        for trip in trips:
            ratio = (trip["km"] - km_min) / max(1, km_max - km_min)
            folium.PolyLine(
                locations=trip["path"],
                color=color_from_ratio(ratio),
                weight=3, opacity=0.85,
                tooltip=(
                    f"<b>{sel_city}</b> → <b>{trip['rival_city']}</b>"
                    f"<br>{selected} → {trip['rival']}"
                    f"<br>🛣️ {trip['km']} km"
                )
            ).add_to(m)

        for trip in trips:
            rv = TEAMS[trip["rival"]]
            folium.Marker(
                location=[rv["lat"], rv["lon"]],
                icon=folium.DivIcon(
                    html=shield_marker_html(trip["rival"], trip["km"]),
                    icon_size=(40, 50),
                    icon_anchor=(20, 25),
                ),
                tooltip=(
                    f"<b>{trip['rival_city']}</b> ({trip['rival']})"
                    f"<br>📍 {trip['stadium']}"
                    f"<br>🛣️ {trip['km']} km"
                )
            ).add_to(m)

        sel_data = TEAMS[selected]
        if selected in SHIELDS:
            sel_html = (
                f'<div style="text-align:center">'
                f'<img src="{SHIELDS[selected]}" style="width:38px;height:38px;object-fit:contain;'
                f'background:white;border-radius:50%;border:3px solid #e74c3c;'
                f'box-shadow:0 2px 6px rgba(0,0,0,0.4)"></div>'
            )
            folium.Marker(
                location=[sel_data["lat"], sel_data["lon"]],
                icon=folium.DivIcon(html=sel_html, icon_size=(44, 44), icon_anchor=(22, 22)),
                tooltip=f"<b>⭐ {sel_city}</b> ({selected})<br>📍 {sel_stadium}"
            ).add_to(m)
        else:
            folium.Marker(
                location=[sel_data["lat"], sel_data["lon"]],
                icon=folium.Icon(color="red", icon="star", prefix="fa"),
                tooltip=f"<b>⭐ {sel_city}</b> ({selected})<br>📍 {sel_stadium}"
            ).add_to(m)

        st_folium(m, width=700, height=540, returned_objects=[])

    with col_table:
        st.subheader("📋 Todos los desplazamientos")
        import pandas as pd
        df = pd.DataFrame([
            {"Ciudad rival": t["rival_city"], "Club": t["rival"], "Km": t["km"]}
            for t in trips
        ]).sort_values("Km").reset_index(drop=True)
        df.index += 1

        def highlight(row):
            if row["Km"] == df["Km"].min(): return ["background-color:#d4edda"] * len(row)
            if row["Km"] == df["Km"].max(): return ["background-color:#f8d7da"] * len(row)
            return [""] * len(row)

        st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True, height=510)

    st.caption(
        f"🟢 Más corto: **{shortest['rival_city']}** ({shortest['rival']}, {km_min} km) · "
        f"🔴 Más largo: **{longest['rival_city']}** ({longest['rival']}, {km_max} km) · "
        f"Datos: OSRM / OpenStreetMap · 🛡️ Escudos: Wikimedia Commons"
    )
