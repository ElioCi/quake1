import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
from geopy.distance import geodesic
import numpy as np
from scipy.interpolate import griddata
from folium.plugins import MarkerCluster

# **Titolo**
st.title("Mappa Interattiva")
st.write('Trascina marker su posizione desiderata e clicca su di esso o inserisci coordinate nella sidebar e clicca sul pulsante "Aggiorna posizione" ')

# **Caricamento dati CSV**
file_path = "files/spettri2008.csv"

@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        if not {"ID", "LON", "LAT"}.issubset(df.columns):
            st.error("Errore: Il file CSV non contiene le colonne richieste ('ID', 'LON', 'LAT').")
            return None
        return df
    except FileNotFoundError:
        st.error("Errore: Il file 'spettri2008.csv' non è stato trovato.")
        return None

df = load_data(file_path)

def is_point_in_df(lat, lon, df, tolerance=0.0001):
    """Verifica se un punto (lat, lon) è presente nel DataFrame con una piccola tolleranza."""
    return any((abs(df["LAT"] - lat) < tolerance) & (abs(df["LON"] - lon) < tolerance))


# **Session State Initialization**
if "lat" not in st.session_state:
    st.session_state.lat = 41.869
    st.session_state.lon = 12.436
    st.session_state.zoom = 6
    st.session_state.needs_update = False

if "marker_moved" not in st.session_state:
    st.session_state.marker_moved = False

if "vis" not in st.session_state:
    st.session_state.vis = 7.5


# **Funzione per trovare i punti vicini**
def get_nearby_points(lat, lon, df, max_distance_km):
    return df[[geodesic((lat, lon), (row["LAT"], row["LON"])).km <= max_distance_km for _, row in df.iterrows()]]

# **Funzione per interpolazione bilineare**
def interpolate_values(lat, lon, df):
    if df is None or df.empty:
        return None
    
    columns_to_interpolate = [col for col in df.columns if col.startswith("T")]
    points = df[["LON", "LAT"]].values
    values = df[columns_to_interpolate].values
    interpolated_values = griddata(points, values, (lon, lat), method='linear')
    
    if interpolated_values is not None:
        return dict(zip(columns_to_interpolate, interpolated_values if isinstance(interpolated_values, (list, tuple, np.ndarray)) else [interpolated_values]))
    return None

# creazione file contenente i valori interpolati
def create_punto_scelto_file(interpolated_values, output_file="files/punto_scelto.csv"):
    # Definizione dei valori di T
    T_values = [30, 50, 72, 101, 140, 201, 475, 975, 2475]
    
    # Creazione del dataframe nel formato richiesto
    data = {
        "T": T_values,
        "ag": [interpolated_values[f"T{T}ag"]/10 for T in T_values],
        "F0": [interpolated_values[f"T{T}F0"] for T in T_values],
        "Tc": [interpolated_values[f"T{T}Tc"] for T in T_values],
    }
    
    df_punto_scelto = pd.DataFrame(data)
    
    # Salvataggio su file CSV
    df_punto_scelto.to_csv(output_file, index=False)
    #print(f"File '{output_file}' creato con successo!")

# Definisci i limiti di latitudine e longitudine (Bounding Box)
min_lat = 35.0  # Limite inferiore latitudine
max_lat = 48.0  # Limite superiore latitudine
min_lon = 3.0  # Limite inferiore longitudine
max_lon = 25.0  # Limite superiore longitudine
# Limiti di zoom
min_zoom_level = 4
# max_zoom_level = 10

with open('files/Coordinate.csv') as file_coordinate:
    dfcoord = pd.read_csv(file_coordinate)   # lettura file e creazione
    #dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

st.session_state.lat = dfcoord.loc[0,'Latitudine']
st.session_state.lon = dfcoord.loc[0,'Longitudine']

# **Interfaccia per inserimento manuale delle coordinate**
with st.sidebar:
    #vis_griglia = st.checkbox('visualizza griglia', key = "griglia")
    vis_griglia = st.radio ('Raggio griglia punti', ['7.5 km', '15 km', '30 km'])
    
    if vis_griglia=='7.5 km':
        griglia_distanza = 7.5
    elif vis_griglia == '15 km':
        griglia_distanza = 15.0    
    else:
        griglia_distanza = 30.0    

    if griglia_distanza != st.session_state.vis:
        st.session_state.needs_update = True
        st.session_state.vis = griglia_distanza
    
  

    st.write("### 📍 Coordinate")
    new_lat = st.number_input("Latitudine", value=st.session_state.lat, step=0.001)
    new_lon = st.number_input("Longitudine", value=st.session_state.lon, step=0.001)
    if st.button("Aggiorna Posizione"):
        if (new_lat, new_lon) != (st.session_state.lat, st.session_state.lon):
            st.session_state.lat = new_lat
            st.session_state.lon = new_lon
            st.session_state.needs_update = True
            st.rerun()

# **Creazione della mappa**
if "mappa" not in st.session_state or st.session_state.needs_update:
    st.session_state.mappa = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=st.session_state.zoom, min_zoom = min_zoom_level)
    
    # Crea una lista di coordinate per il bounding box (area delimitata)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    st.session_state.mappa.fit_bounds(bounds)

    # Imposta i limiti massimi della mappa (maxBounds)
    st.session_state.mappa.options['maxBounds'] = bounds

    # Aggiungi un rettangolo per delimitare la zona visibile
    #folium.Rectangle(bounds=[[min_lat, min_lon], [max_lat, max_lon]], color="blue", weight=2, fill=True, fill_opacity=0.07).add_to(st.session_state.mappa)

    # **Aggiunta del marker principale con trascinamento rilevabile**
    marker = folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        icon=folium.Icon(color="blue"),
        popup=f"📍 Posizione: {st.session_state.lat}, {st.session_state.lon}",
        draggable=True
    )
    marker.add_to(st.session_state.mappa)
    

    # **Aggiunta dei punti vicini**
    if df is not None:
        
        #nearby_points = get_nearby_points(st.session_state.lat, st.session_state.lon, df, max_distance_km=griglia_distanza)
        nearby_points = get_nearby_points(st.session_state.lat, st.session_state.lon, df, griglia_distanza)
        for _, row in nearby_points.iterrows():
            folium.CircleMarker(
                location=[row["LAT"], row["LON"]],
                radius=6,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.6,
                #popup=f"ID: {row['ID']}<br>📍 Lat: {row['LAT']}, Lon: {row['LON']}",
                tooltip=f"ID: {row['ID']}<br>📍 Lat: {row['LAT']}, Lon: {row['LON']}",
            ).add_to(st.session_state.mappa)
        
    st.session_state.needs_update = False


# **Mostra la mappa**
map_data = st_folium(st.session_state.mappa, height=500, width=700, key="map")


# **Cattura il rilascio del marker e aggiorna la posizione SOLO se è stato spostato**
if map_data:
    # Se il marker è stato spostato (drag & drop)
    if "last_object_clicked" in map_data and map_data["last_object_clicked"]:
        clicked = map_data["last_object_clicked"]
        new_lat = clicked.get("lat", None)
        new_lon = clicked.get("lng", None)
        #print('clicked=', clicked)
    # Verifica se il punto cliccato è tra quelli nel file CSV
    if is_point_in_df(new_lat, new_lon, df):
        aaa = 1
        #st.warning("⚠️ Hai cliccato su un punto del dataset, il marker principale non verrà spostato.")
    else:
        # Aggiorna le coordinate del marker principale
        if (new_lat, new_lon) != (st.session_state.lat, st.session_state.lon):
            st.session_state.lat = new_lat
            st.session_state.lon = new_lon
            st.session_state.needs_update = True
            st.success(f"📍Marker spostato a: {st.session_state.lat}, {st.session_state.lon}")
            
            
            st.session_state['coordinate'] = [{

                'Latitudine': st.session_state.lat,
                'Longitudine':st.session_state.lon,
            
            }]
            df_coordinate = pd.DataFrame(st.session_state['coordinate'])
            df_coordinate.to_csv("files/Coordinate.csv", index=False)   # salva coordinate sito scelto
            st.rerun()
  
# **Ricalcola i punti vicini SOLO se serve un aggiornamento**
if st.session_state.needs_update:
    nearby_points = get_nearby_points(st.session_state.lat, st.session_state.lon, df, griglia_distanza)

    # Ricrea la mappa con i nuovi punti
    st.session_state.mappa = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=st.session_state.zoom)

    # Aggiungi il marker principale con la posizione aggiornata
    marker = folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        icon=folium.Icon(color="blue"),
        draggable=True
    )
    st.session_state.mappa.add_child(marker)

    # Aggiungi i nuovi punti vicini sulla mappa
    for _, row in nearby_points.iterrows():
        folium.CircleMarker(
            location=[row["LAT"], row["LON"]],
            radius=6,
            color="red",
            fill=True,
            fill_color="red",
            fill_opacity=0.6,
            popup=f"ID: {row['ID']}<br>📍 Lat: {row['LAT']}, Lon: {row['LON']}",
        ).add_to(st.session_state.mappa)

    st.session_state.needs_update = False  # Reset flag

    
# **Mostra le coordinate quando si clicca su un punto qualsiasi della mappa**
if map_data and "last_clicked" in map_data and map_data["last_clicked"]:
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    
    st.write(f"📍 Coordinate posizione click su mappa: {clicked_lat}, {clicked_lon}")

# **Interpolazione dei valori nel punto selezionato**
if df is not None:
    interpolated_values = interpolate_values(st.session_state.lat, st.session_state.lon, df)
    if interpolated_values:
        st.write("### 📊 Valori Interpolati nel Punto Selezionato:")
        st.write(interpolated_values)

    # Creazione del file
    create_punto_scelto_file(interpolated_values)




