import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import HeatMap
import branca.colormap as cm
import re

# Caricare il file CSV
@st.cache_data
def load_data():
    df = pd.read_csv("files/spettri2008.csv")
    return df

data = load_data()

# Custom CSS per allineare le opzioni su una riga
st.markdown(
        """
        <style>
        .stRadio > div {
            flex-direction: row;
        }
        .col3Radio > div {
            flex-direction: row;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3, col4 = st.columns([2,1,1,1])
opzioniVariabile = ["ag", "F0", "Tc"]
varSelected = col1.radio("Parametro da mappare", options=opzioniVariabile)

match varSelected:
    case "ag":
        testoVar = "ag"
        opzioni_ag = [col for col in data.columns if "ag" in col]

    case "F0":
        testoVar = "F0"
        opzioni_ag = [col for col in data.columns if "F0" in col]

    case "Tc":
        testoVar = "Tc"
        opzioni_ag = [col for col in data.columns if "Tc" in col]

# Selezione della colonna "ag" desiderata
#opzioni_ag = [col for col in data.columns if "ag" in col]
scelta_ag = col2.selectbox("Seleziona periodo:", opzioni_ag)

match = re.search(r'T(\d+)', scelta_ag)  # Trova il numero tra 'T' e il testo finale
parteNumerica = int(match.group(1)) if match else None


with col4:
    #st.write("")  # Aggiunge spazio vuoto
    st.write("")  # Puoi ripetere per abbassare ancora di più
    pulsante = st.button("🪄 vis. mappa")

with st.expander("🆘 Help"):
    st.write('**ag**: accelerazione orizzontale massima al sito;')
    st.write('**F0**: valore massimo del fattore di amplificazione dello spettro in accelerazione orizzontale;')
    st.write('**Tc**: valore di riferimento per la determinazione del periodo di inizio tratto a velocità costante dello spettro in accelerazione orizzontale.')
    st.write('**TXXX**: Tempo di ritorno TR pari a XXX anni')
    
if pulsante:

    # Creazione della mappa
    #st.title(f"Pericolosità sismica - Intensità {testoVar} per TR = {parteNumerica} anni")
    
    st.title("Mappa pericolosità sismica Italia")
    #st.markdown(f"### Intensità **{testoVar}** per TR = {parteNumerica} anni ###")
    st.markdown(f'### Intensità <b>"{testoVar}"</b> per TR = {parteNumerica} anni ###', unsafe_allow_html=True)

    # Definisci i limiti di latitudine e longitudine (Bounding Box)
    min_lat = 35.0  # Limite inferiore latitudine
    max_lat = 48.0  # Limite superiore latitudine
    min_lon = 3.0  # Limite inferiore longitudine
    max_lon = 25.0  # Limite superiore longitudine
    # Limiti di zoom
    min_zoom_level = 4
    # max_zoom_level = 10


    mappaColori = folium.Map(location=[42.5, 12.5], zoom_start=6, min_zoom = min_zoom_level)
    # Crea una lista di coordinate per il bounding box (area delimitata)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    mappaColori.fit_bounds(bounds)
    # Imposta i limiti massimi della mappa (maxBounds)
    mappaColori.options['maxBounds'] = bounds

    # Normalizzazione dei valori di ag per la scala colori
    min_ag, max_ag = data[scelta_ag].min(), data[scelta_ag].max()
    colormap1 = cm.linear.YlOrRd_09.scale(min_ag, max_ag) # Yellow Orange Red - originale
    colormap2 = cm.linear.Blues_09.scale(min_ag, max_ag) # blu
    colormap3 = cm.linear.Greens_09.scale(min_ag, max_ag) # verde

    if varSelected == 'ag':
        colormap = colormap1
    elif varSelected == 'F0':
        colormap = colormap2
    elif varSelected == 'Tc':
        colormap = colormap3

    # Numero di righe da saltare
    skip = 9  # Salta 9 righe ogni 10 (cioè carica una ogni 10)

    # Carica solo una riga ogni 10
    #data_ridotto = pd.read_csv('files/spettri2008.csv', skiprows=lambda x: x % 10 != 0)

    # Aggiunta dei marker alla mappa con tooltip
    progress1 = st.empty()
    progress1_bar = st.progress(0)
    progress1_text = st.empty()
    numero_righe = data.shape[0]

    i = 0
    #for _, row in data.iterrows():
    for i, row in data.iterrows():
        
        percent_complete = int(((i+1)/ (numero_righe)) * 100)
        # Aggiorna la progress bar
        progress1_bar.progress(percent_complete)
        progress1_text.text(f"Progress: {i+1}/{numero_righe} ({percent_complete}%)")
        # Aumenta la barra di avanzamento
        folium.CircleMarker(
            location=[row["LAT"], row["LON"]],
            radius=5,
            color=None,
            fill=True,
            fill_color=colormap(row[scelta_ag]),
            fill_opacity=0.7,
            popup=folium.Popup(f"Lat: {row['LAT']}, Lon: {row['LON']}, {testoVar}: {row[scelta_ag]:.4f}", max_width=300)
            #tooltip=f"Lat: {row['LAT']}, Lon: {row['LON']}, ag: {row[scelta_ag]:.4f}"
        ).add_to(mappaColori)

    progress1_text.text("Caricamento dati completato. Visualizzazione mappa in corso... Attendere prego!")
    # Aggiunta della legenda
    colormap.add_to(mappaColori)
    # Visualizzazione della mappa
    folium_static(mappaColori)

    progress1.empty()
    progress1_text.text("Mappa Italia con punti. Clicca sulla mappa per info.")

