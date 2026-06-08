import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import math


st.set_page_config(page_title="Distancias 1ª RFEF", layout="wide", page_icon="⚽")


TEAMS = {
    "Pontevedra CF":              {"lat": 42.438590, "lon": -8.641360, "stadium": "Estadio Municipal de Pasaron",         "city": "Pontevedra",        "provincia": "Pontevedra"},
    "Barakaldo CF":               {"lat": 43.302103, "lon": -2.986659, "stadium": "Estadio de Lasesarre",                 "city": "Barakaldo",         "provincia": "Bizkaia/Vizcaya"},
    "Unionistas de Salamanca CF": {"lat": 40.946684, "lon": -5.665987, "stadium": "Estadio Municipal Reina Sofia",        "city": "Salamanca",         "provincia": "Salamanca"},
    "CD Lugo":                    {"lat": 43.003365, "lon": -7.570954, "stadium": "Estadio Anxo Carro",                   "city": "Lugo",              "provincia": "Lugo"},
    "AD Merida":                  {"lat": 38.913933, "lon": -6.336406, "stadium": "Estadio Romano Jose Fouto",            "city": "Merida",            "provincia": "Badajoz"},
    "Arenas Club":                {"lat": 43.331469, "lon": -3.006467, "stadium": "Campo Municipal de Gobela",            "city": "Getxo",             "provincia": "Bizkaia/Vizcaya"},
    "Racing Club Ferrol":         {"lat": 43.490726, "lon": -8.239403, "stadium": "Estadio Municipal de A Malata",        "city": "Ferrol",            "provincia": "A Coruna"},
    "Athletic Club B":            {"lat": 43.277500, "lon": -2.839320, "stadium": "Lezama",                               "city": "Lezama",            "provincia": "Bizkaia/Vizcaya"},
    "Real Aviles Industrial":     {"lat": 43.557500, "lon": -5.930600, "stadium": "Estadio Roman Suarez Puerta",          "city": "Aviles",            "provincia": "Asturias"},
    "CP Cacereno":                {"lat": 39.487130, "lon": -6.412350, "stadium": "Estadio Principe Felipe",              "city": "Caceres",           "provincia": "Caceres"},
    "FC Cartagena":               {"lat": 37.609746, "lon": -0.995977, "stadium": "Estadio Cartagonova",                  "city": "Cartagena",         "provincia": "Murcia"},
    "Antequera CF":               {"lat": 37.020600, "lon": -4.559368, "stadium": "Estadio El Mauli",                     "city": "Antequera",         "provincia": "Malaga"},
    "Algeciras CF":               {"lat": 36.163333, "lon": -5.465280, "stadium": "Estadio Nuevo Mirador",                "city": "Algeciras",         "provincia": "Cadiz"},
    "Hercules CF":                {"lat": 38.357204, "lon": -0.492754, "stadium": "Estadio Jose Rico Perez",              "city": "Alicante",          "provincia": "Alacant/Alicante"},
    "Real Murcia CF":             {"lat": 38.042250, "lon": -1.144730, "stadium": "Estadio Enrique Roca de Murcia",       "city": "Murcia",            "provincia": "Murcia"},
    "AD Alcorcon":                {"lat": 40.338889, "lon": -3.840556, "stadium": "Estadio Santo Domingo",                "city": "Alcorcon",          "provincia": "Madrid"},
    "UD Ibiza":                   {"lat": 38.913780, "lon":  1.415090, "stadium": "Estadio Can Misses",                   "city": "Ibiza",             "provincia": "Illes Balears"},
    "CD Teruel":                  {"lat": 40.332050, "lon": -1.105860, "stadium": "Estadio de Pinilla",                   "city": "Teruel",            "provincia": "Teruel"},
    "Nastic de Tarragona":        {"lat": 41.127003, "lon":  1.272830, "stadium": "Nou Estadi Costa Daurada",             "city": "Tarragona",         "provincia": "Tarragona"},
    "CD Torremolinos":            {"lat": 36.621460, "lon": -4.509930, "stadium": "Campo de Futbol El Pozuelo",           "city": "Torremolinos",      "provincia": "Malaga"},
    "Real Zaragoza":              {"lat": 41.683664, "lon": -0.895446, "stadium": "Ibercaja Estadio (modular)",           "city": "Zaragoza",          "provincia": "Zaragoza"},
    "SD Huesca":                  {"lat": 42.131944, "lon": -0.424444, "stadium": "Estadio El Alcoraz",                   "city": "Huesca",            "provincia": "Huesca"},
    "CyD Leonesa":                {"lat": 42.587470, "lon": -5.577040, "stadium": "Estadio Reino de Leon",                "city": "Leon",              "provincia": "Leon"},
    "Deportivo Fabril":           {"lat": 43.252470, "lon": -8.282840, "stadium": "Ciudad Deportiva de Abegondo",         "city": "Abegondo",          "provincia": "A Coruna"},
    "Real Union":                 {"lat": 43.345560, "lon": -1.785830, "stadium": "Stadium Gal",                          "city": "Irun",              "provincia": "Gipuzkoa/Guipuzcoa"},
    "UE Sant Andreu":             {"lat": 41.428836, "lon":  2.193047, "stadium": "Estadio Narcis Sala",                  "city": "Barcelona",         "provincia": "Barcelona"},
    "CD Extremadura":             {"lat": 38.684350, "lon": -6.414590, "stadium": "Estadio Francisco de la Hera",         "city": "Almendralejo",      "provincia": "Badajoz"},
    "Rayo Majadahonda":           {"lat": 40.457558, "lon": -3.860309, "stadium": "Estadio Cerro del Espino",             "city": "Majadahonda",       "provincia": "Madrid"},
    "CD Mirandes":                {"lat": 42.680786, "lon": -2.935436, "stadium": "Estadio Municipal de Anduva",          "city": "Miranda de Ebro",   "provincia": "Burgos"},
    "UD Ourense":                 {"lat": 42.340650, "lon": -7.875730, "stadium": "Estadio de O Couto",                   "city": "Ourense",           "provincia": "Ourense"},
    "UD Logrones":                {"lat": 42.452970, "lon": -2.453340, "stadium": "Estadio Las Gaunas",                   "city": "Logrono",           "provincia": "La Rioja"},
    "Aguilas FC":                 {"lat": 37.404300, "lon": -1.590040, "stadium": "Estadio El Rubial",                    "city": "Aguilas",           "provincia": "Murcia"},
    "Real Jaen CF":               {"lat": 37.776159, "lon": -3.786839, "stadium": "Estadio Municipal La Victoria",        "city": "Jaen",              "provincia": "Jaen"},
    "CD Coria":                   {"lat": 39.988190, "lon": -6.536300, "stadium": "Estadio La Isla",                      "city": "Coria",             "provincia": "Caceres"},
    "CE Europa":                  {"lat": 41.411800, "lon":  2.161500, "stadium": "Nou Sardenya",                         "city": "Barcelona",         "provincia": "Barcelona"},
    "Atletico de Madrid B":       {"lat": 40.481400, "lon": -3.330500, "stadium": "Centro Deportivo Alcala de Henares",   "city": "Alcala de Henares", "provincia": "Madrid"},
    "Real Madrid Castilla":       {"lat": 40.476856, "lon": -3.614287, "stadium": "Estadio Alfredo Di Stefano",           "city": "Madrid",            "provincia": "Madrid"},
    "Villarreal B":               {"lat": 39.939487, "lon": -0.114498, "stadium": "Ciudad Deportiva Jose Manuel Llaneza", "city": "Vila-real",         "provincia": "Castello/Castellon"},
    "Celta Fortuna*":             {"lat": 42.213500, "lon": -8.741200, "stadium": "Campo de Barreiro",                    "city": "Vigo",              "provincia": "Pontevedra"},
    "SD Ponferradina*":           {"lat": 42.557400, "lon": -6.599972, "stadium": "Estadio El Toralin",                   "city": "Ponferrada",        "provincia": "Leon"},
    "CE Sabadell*":               {"lat": 41.554722, "lon":  2.091944, "stadium": "Nova Creu Alta",                       "city": "Sabadell",          "provincia": "Barcelona"},
    "Zamora CF*":                 {"lat": 41.486390, "lon": -5.748060, "stadium": "Estadio Ruta de la Plata",             "city": "Zamora",            "provincia": "Zamora"},
}

PROVISIONAL = {name for name in TEAMS if name.endswith("*")}
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


def provincia_color(count, max_count):
    if count == 0:
        return "#f0f0f0"
    intensity = count / max_count
    r = int(220 - 170 * intensity)
    g = int(240 - 80  * intensity)
    b = int(220 - 170 * intensity)
    return f"#{r:02x}{g:02x}{b:02x}"


def dot_marker_html(km=None, provisional=False):
    color = "#e67e22" if provisional else "#2980b9"
    km_label = (
        f'<div style="font-size:8px;font-weight:bold;color:#1a252f;text-align:center;'
        f'background:rgba(255,255,255,0.85);border-radius:3px;padding:0 3px;margin-top:1px">'
        f'{km} km</div>'
    ) if km else ""
    return (
        f'<div style="text-align:center">'
        f'<div style="width:14px;height:14px;background:{color};border-radius:50%;'
        f'border:2px solid white;box-shadow:0 1px 3px rgba(0,0,0,0.3);margin:0 auto"></div>'
        f'{km_label}</div>'
    )


st.markdown(
    "<style>[data-testid='metric-container']{"
    "background:#f8f9fa;border-radius:10px;padding:12px 16px;"
    "border:1px solid #e9ecef;}</style>",
    unsafe_allow_html=True,
)

st.title("Herramienta de Desplazamientos - 1a RFEF 2026/27")
st.caption("42 equipos (38 confirmados + 4 provisionales*) - Rutas reales por carretera (OSRM/OpenStreetMap)")
st.caption("Equipos marcados con * son provisionales - Provincias coloreadas segun num. de equipos")

team_names = sorted(TEAMS.keys())


def label(name):
    d = TEAMS[name]
    prov = " (provisional)" if name in PROVISIONAL else ""
    return f"{name}  --  {d['stadium']} ({d['city']}){prov}"


selected = st.selectbox("Selecciona un equipo", team_names, format_func=label)

st.info(
    "FERRY - Trayecto a/desde Ibiza: El desplazamiento incluye el ferry "
    "Denia -> Ibiza (o viceversa). La travesia cubre aproximadamente "
    "104 km por mar y dura unas 2h 30min. El km total mostrado incluye "
    "ese tramo; la ruta dibujada en el mapa entre Denia e Ibiza es en linea recta."
)

if selected:
    sel_city    = TEAMS[selected]["city"]
    sel_stadium = TEAMS[selected]["stadium"]
    rivals      = [t for t in team_names if t != selected]

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
            "rival": rival, "rival_city": rv["city"], "km": km,
            "stadium": rv["stadium"], "path": path,
            "provisional": rival in PROVISIONAL,
        })
        progress.progress((i + 1) / len(rivals), text=f"Calculando rutas... {i+1}/{len(rivals)}")
    progress.empty()

    total_km = sum(t["km"] for t in trips)
    avg_km   = total_km / len(trips)
    shortest = min(trips, key=lambda x: x["km"])
    longest  = max(trips, key=lambda x: x["km"])
    km_min, km_max = shortest["km"], longest["km"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total km (visitante)", f"{total_km:,} km")
    c2.metric("Media por viaje",      f"{avg_km:,.0f} km")
    c3.metric("Mas corto", f"{shortest['rival_city']}  --  {km_min} km", delta=shortest["rival"], delta_color="off")
    c4.metric("Mas largo", f"{longest['rival_city']}  --  {km_max} km",  delta=longest["rival"],  delta_color="off")

    st.markdown("---")
    col_map, col_table = st.columns([3, 2])

    with col_map:
        st.subheader(f"Desplazamientos desde {sel_city}")
        m = folium.Map(location=[40.4, -3.5], zoom_start=5, tiles="CartoDB positron")

        geojson = load_geojson()
        if geojson:
            prov_count = {}
            for t in TEAMS.values():
                p = t["provincia"]
                prov_count[p] = prov_count.get(p, 0) + 1
            max_count = max(prov_count.values())

            def style_fn(feature):
                cnt = prov_count.get(feature["properties"]["name"], 0)
                return {
                    "fillColor":   provincia_color(cnt, max_count),
                    "color":       "#aaaaaa",
                    "weight":      0.8,
                    "fillOpacity": 0.55 if cnt > 0 else 0.0,
                }

            folium.GeoJson(
                geojson,
                style_function=style_fn,
                highlight_function=lambda f: {"weight": 2, "color": "#555", "fillOpacity": 0.75},
                tooltip=folium.GeoJsonTooltip(fields=["name"], aliases=["Provincia:"]),
            ).add_to(m)

        for trip in trips:
            ratio      = (trip["km"] - km_min) / max(1, km_max - km_min)
            line_color = "#e67e22" if trip["provisional"] else color_from_ratio(ratio)
            folium.PolyLine(
                locations=trip["path"], color=line_color,
                weight=3 if not trip["provisional"] else 2,
                opacity=0.85 if not trip["provisional"] else 0.5,
                dash_array="6 4" if trip["provisional"] else None,
                tooltip=(
                    f"<b>{sel_city}</b> -> <b>{trip['rival_city']}</b>"
                    f"<br>{selected} -> {trip['rival']}"
                    f"<br>{trip['km']} km"
                    + (" (provisional)" if trip["provisional"] else "")
                )
            ).add_to(m)

        for trip in trips:
            rv = TEAMS[trip["rival"]]
            folium.Marker(
                location=[rv["lat"], rv["lon"]],
                icon=folium.DivIcon(
                    html=dot_marker_html(trip["km"], trip["provisional"]),
                    icon_size=(40, 50), icon_anchor=(20, 25),
                ),
                tooltip=(
                    f"<b>{trip['rival_city']}</b> ({trip['rival']})"
                    + (" - provisional" if trip["provisional"] else "")
                    + f"<br>{trip['stadium']}"
                    + f"<br>{trip['km']} km"
                )
            ).add_to(m)

        sel_data = TEAMS[selected]
        folium.Marker(
            location=[sel_data["lat"], sel_data["lon"]],
            icon=folium.Icon(color="red", icon="star", prefix="fa"),
            tooltip=f"<b>{sel_city}</b> ({selected})<br>{sel_stadium}"
        ).add_to(m)

        legend_html = """
        <div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
                    padding:10px 14px;border-radius:8px;border:1px solid #ccc;
                    font-size:12px;box-shadow:2px 2px 6px rgba(0,0,0,0.2)">
          <b>Equipos por provincia</b><br>
          <span style="display:inline-block;width:14px;height:14px;background:#dcf0dc;border:1px solid #aaa;vertical-align:middle"></span> 1 equipo<br>
          <span style="display:inline-block;width:14px;height:14px;background:#94d494;border:1px solid #aaa;vertical-align:middle"></span> 2 equipos<br>
          <span style="display:inline-block;width:14px;height:14px;background:#50aa50;border:1px solid #aaa;vertical-align:middle"></span> 3+ equipos<br>
          <hr style="margin:4px 0">
          <span style="display:inline-block;width:14px;height:14px;background:#2980b9;border-radius:50%;vertical-align:middle"></span> Confirmado<br>
          <span style="display:inline-block;width:14px;height:14px;background:#e67e22;border-radius:50%;vertical-align:middle"></span> Provisional*
        </div>
        """
        m.get_root().html.add_child(folium.Element(legend_html))
        st_folium(m, width=700, height=540, returned_objects=[])

    with col_table:
        st.subheader("Todos los desplazamientos")
        import pandas as pd
        df = pd.DataFrame([
            {"Ciudad rival": t["rival_city"], "Club": t["rival"], "Km": t["km"]}
            for t in trips
        ]).sort_values("Km").reset_index(drop=True)
        df.index += 1

        def highlight(row):
            if "*" in str(row["Club"]):     return ["background-color:#fff3cd"] * len(row)
            if row["Km"] == df["Km"].min(): return ["background-color:#d4edda"] * len(row)
            if row["Km"] == df["Km"].max(): return ["background-color:#f8d7da"] * len(row)
            return [""] * len(row)

        st.dataframe(df.style.apply(highlight, axis=1), use_container_width=True, height=540)
        st.caption("Amarillo = equipo provisional")

    st.caption(
        f"Mas corto: {shortest['rival_city']} ({shortest['rival']}, {km_min} km) - "
        f"Mas largo: {longest['rival_city']} ({longest['rival']}, {km_max} km) - "
        f"Datos: OSRM / OpenStreetMap"
    )
