import streamlit as st
import pandas as pd
import csv

# **Titolo**
st.title("Risposta sismica locale")

# inizializza session_state
if "input_data" not in st.session_state:
    st.session_state.input_data = []

if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'none'

if 'datiRispostaLocale' not in st.session_state:
    st.session_state['datiRispostaLocale'] = []
   
if 'CatTopo' not in st.session_state:
    st.session_state.CatTopo = "" 

if 'dataConfirmed' not in st.session_state:
    st.session_state.dataConfirmed = False  




optA = '''
A - Ammassi rocciosi affioranti o terreni molto rigidi caratterizzati da valori di velocità delle onde
di taglio superiori a 800 m/s, eventualmente comprendenti in superficie terreni di caratteristiche
meccaniche più scadenti con spessore massimo pari a 3 m.
'''
optB = '''
B - Rocce tenere e depositi di terreni a grana grossa molto addensati o terreni a grana fina molto consistenti,
caratterizzati da un miglioramento delle proprietà meccaniche con la profondità e da
valori di velocità equivalente compresi tra 360 m/s e 800 m/s.
'''
optC = '''
C - Depositi di terreni a grana grossa mediamente addensati o terreni a grana fina mediamente consistenti
con profondità del substrato superiori a 30 m, caratterizzati da un miglioramento delle
proprietà meccaniche con la profondità e da valori di velocità equivalente compresi tra
180 m/s e 360 m/s.
'''
optD = '''
D - Depositi di terreni a grana grossa scarsamente addensati o di terreni a grana fina scarsamente consistenti,
con profondità del substrato superiori a 30 m, caratterizzati da un miglioramento delle
proprietà meccaniche con la profondità e da valori di velocità equivalente compresi tra
100 e 180 m/s.
'''
optE = '''
E - Terreni con caratteristiche e valori di velocità equivalente riconducibili a quelle definite per le categorie
C o D, con profondità del substrato non superiore a 30 m.
'''

valori_catSuolo = {optA: 'A', optB: 'B', optC: 'C', optD: 'D', optE: 'E'}
opzioni_catSuolo = list(valori_catSuolo.keys())

#leggi dati di input da DatiGenerali.csv
with open('files/RispostaLocale.csv') as fileRL:
    dfRL = pd.read_csv(fileRL)   # lettura file e creazione
    #dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

st.session_state.catSuolo = dfRL.loc[0,'Catsuolo']
st.session_state.catTopo = dfRL.loc[0,'CatTopo']
st.session_state.temphH = dfRL.loc[0,'hH']

if 'catSuolo' not in st.session_state:
    st.session_state.catSuolo = 'A'  # Valore di default

if 'catSuolo_selected' not in st.session_state:
    # Trova la chiave corrispondente al valore numerico di VN
    st.session_state.catSuolo_selected = next(
        (key for key, value in valori_catSuolo.items() if value == st.session_state.catSuolo), opzioni_catSuolo[0]
    )

def update_catSuolo():
    #st.write("update_VN() eseguita!")  # Questo dovrebbe apparire in output
    st.session_state.catSuolo = valori_catSuolo[st.session_state.catSuolo_selected]

# Selectbox con on_change
st.selectbox(
    '(Rif. Tab. 3.2.II NTC 2018) - Categoria di sottosuolo',
    options=opzioni_catSuolo,
    key="catSuolo_selected",
    on_change= update_catSuolo()
)

st.markdown(f"Cat. Sottosuolo selezionata = **{st.session_state.catSuolo}**")

optT1 = 'T1 - Superficie pianeggiante, pendii e rilievi isolati con inclinazione media i ≤ 15°'
optT2 = 'T2 - Pendii con inclinazione media i > 15°'
optT3 = 'T3 - Rilievi con larghezza in cresta molto minore che alla base e inclinazione media 15° ≤ i ≤ 30°'
optT4 = 'T4 - Rilievi con larghezza in cresta molto minore che alla base e inclinazione media i > 30°'

valori_catTopo = {optT1: 'T1', optT2: 'T2', optT3: 'T3', optT4: 'T4'}
opzioni_catTopo = list(valori_catTopo.keys())

if 'catTopo' not in st.session_state:
    st.session_state.catTopo = 'T1'  # Valore di default

if 'catTopo_selected' not in st.session_state:
    # Trova la chiave corrispondente al valore numerico di VN
    st.session_state.catTopo_selected = next(
        (key for key, value in valori_catTopo.items() if value == st.session_state.catTopo), opzioni_catTopo[0]
    )

if 'hH' not in st.session_state:
    st.session_state.hH = 0.00

if 'temphH' not in st.session_state:
    st.session_state.temphH = 0.00

def update_catTopo():
    #st.write("update_VN() eseguita!")  # Questo dovrebbe apparire in output
    st.session_state.catTopo = valori_catTopo[st.session_state.catTopo_selected]
    

# Selectbox con on_change
st.selectbox(
    '(Rif. Tab. 3.2.III NTC 2018) - Categoria topografica',
    options=opzioni_catTopo,
    key="catTopo_selected",
    on_change= update_catTopo()
)

st.markdown(f"Cat. Topografica selezionata = **{st.session_state.catTopo}**")

# Calcolo SS e CC
catS = st.session_state.catSuolo
catT = st.session_state.catTopo

# Valutazione e calcolo ST (coeff. topografico)
hH = st.slider('h/H', min_value= 0.0, max_value= 1.0, value = st.session_state.temphH)

st.session_state.temphH = hH

match catT:
    case "T1":
        ST = 1.0

    case "T2":
        ST = 1.0 + (1.2 - 1) * hH

    case "T3":
        ST = 1.0 + (1.2 - 1) * hH

    case "T4":
        ST = 1.0 + (1.4 - 1) * hH

st.markdown(f'**ST = {round(ST, 3)}**')

# memorizza risultati nel file RispostaLocale.csv
fileRispostaLocale = "files/RispostaLocale.csv"
st.session_state['datiRispostaLocale'] = [{
    'Catsuolo': catS,
    'CatTopo': catT,
    'hH': hH,
    'ST': ST,
}]

dfRL = pd.DataFrame(st.session_state['datiRispostaLocale'])
dfRL.to_csv(fileRispostaLocale, index= False)   # salva dati risposta locale


# Caricamento del file CSV
file_path = "files/DatiStatiLimite.csv"  # leggi file
dfSL = pd.read_csv(file_path)

# Estrazione dei dati per ogni Stato Limite
SLO_TR, SLO_ag, SLO_F0, SLO_Tc = dfSL[dfSL["StatoLimite"] == "SLO"].values[0][1:5]
SLD_TR, SLD_ag, SLD_F0, SLD_Tc = dfSL[dfSL["StatoLimite"] == "SLD"].values[0][1:5]
SLV_TR, SLV_ag, SLV_F0, SLV_Tc = dfSL[dfSL["StatoLimite"] == "SLV"].values[0][1:5]
SLC_TR, SLC_ag, SLC_F0, SLC_Tc = dfSL[dfSL["StatoLimite"] == "SLC"].values[0][1:5]

# Visualizzazione delle variabili in Streamlit
#st.write("### Dati per ogni Stato Limite:")

#st.write(f"**SLO** - TR= {SLO_TR}, ag= {SLO_ag}, F0= {SLO_F0}, Tc= {SLO_Tc}")
#st.write(f"**SLD** - TR= {SLD_TR}, ag= {SLD_ag}, F0= {SLD_F0}, Tc= {SLD_Tc}")
#st.write(f"**SLV** - TR= {SLV_TR}, ag= {SLV_ag}, F0= {SLV_F0}, Tc= {SLV_Tc}")
#st.write(f"**SLC** - TR= {SLC_TR}, ag= {SLC_ag}, F0= {SLC_F0}, Tc= {SLC_Tc}")

match catS:    # match su Categoria Suolo 
    case "A":
        SLO_SS = 1.0
        SLO_CC = 1.0
        SLD_SS = 1.0
        SLD_CC = 1.0
        SLV_SS = 1.0
        SLV_CC = 1.0
        SLC_SS = 1.0
        SLC_CC = 1.0

    case "B":
        SLO_SS = 1.4 - 0.4*SLO_F0*SLO_ag
        if SLO_SS <= 1: SLO_SS = 1
        if SLO_SS >= 1.2: SLO_SS = 1.2
        SLO_CC = 1.1*(SLO_Tc)**(-0.20)

        SLD_SS = 1.4 - 0.4*SLD_F0*SLD_ag
        if SLD_SS <= 1: SLD_SS = 1
        if SLD_SS >= 1.2: SLD_SS = 1.2
        SLD_CC = 1.1*(SLD_Tc)**(-0.20)

        SLV_SS = 1.4 - 0.4*SLV_F0*SLV_ag
        if SLV_SS <= 1: SLV_SS = 1
        if SLV_SS >= 1.2: SLV_SS = 1.2
        SLV_CC = 1.1*(SLV_Tc)**(-0.20)

        SLC_SS = 1.4 - 0.4*SLC_F0*SLC_ag
        if SLC_SS <= 1: SLC_SS = 1
        if SLC_SS >= 1.2: SLC_SS = 1.2
        SLC_CC = 1.1*(SLC_Tc)**(-0.20)

    case "C":
        SLO_SS = 1.7 - 0.6*SLO_F0*SLO_ag
        if SLO_SS <= 1: SLO_SS = 1
        if SLO_SS >= 1.5: SLO_SS = 1.5
        SLO_CC = 1.05*(SLO_Tc)**(-0.33)
        #SLD
        SLD_SS = 1.7 - 0.6*SLD_F0*SLD_ag
        if SLD_SS <= 1: SLD_SS = 1
        if SLD_SS >= 1.5: SLD_SS = 1.5
        SLD_CC = 1.05*(SLD_Tc)**(-0.33)
        # segue SLV
        SLV_SS = 1.7 - 0.6*SLV_F0*SLV_ag
        if SLV_SS <= 1: SLV_SS = 1
        if SLV_SS >= 1.5: SLV_SS = 1.5
        SLV_CC = 1.05*(SLV_Tc)**(-0.33)
        # segue SLC
        SLC_SS = 1.7 - 0.6*SLC_F0*SLC_ag
        if SLC_SS <= 1: SLC_SS = 1
        if SLC_SS >= 1.5: SLC_SS = 1.5
        SLC_CC = 1.05*(SLC_Tc)**(-0.33)

    case "D":
        SLO_SS = 2.4 - 1.5*SLO_F0*SLO_ag
        if SLO_SS <= 0.9: SLO_SS = 0.9
        if SLO_SS >= 1.8: SLO_SS = 1.8
        SLO_CC = 1.25*(SLO_Tc)**(-0.50)
        # segue SLD
        SLD_SS = 2.4 - 1.5*SLD_F0*SLD_ag
        if SLD_SS <= 0.9: SLD_SS = 0.9
        if SLD_SS >= 1.8: SLD_SS = 1.8
        SLD_CC = 1.25*(SLD_Tc)**(-0.50)
        # segue SLV
        SLV_SS = 2.4 - 1.5*SLV_F0*SLV_ag
        if SLV_SS <= 0.9: SLV_SS = 0.9
        if SLV_SS >= 1.8: SLV_SS = 1.8
        SLV_CC = 1.25*(SLV_Tc)**(-0.50)
        # segue SLC
        SLC_SS = 2.4 - 1.5*SLC_F0*SLC_ag
        if SLC_SS <= 0.9: SLC_SS = 0.9
        if SLC_SS >= 1.8: SLC_SS = 1.8
        SLC_CC = 1.25*(SLC_Tc)**(-0.50)

    case "E":
        SLO_SS = 2.0 - 1.1*SLO_F0*SLO_ag
        if SLO_SS <= 1.0: SLO_SS = 1.0
        if SLO_SS >= 1.6: SLO_SS = 1.6
        SLO_CC = 1.15*(SLO_Tc)**(-0.40)
        # segue SLD
        SLD_SS = 2.0 - 1.1*SLD_F0*SLD_ag
        if SLD_SS <= 1.0: SLD_SS = 1.0
        if SLD_SS >= 1.6: SLD_SS = 1.6
        SLD_CC = 1.15*(SLD_Tc)**(-0.40)
        # segue SLV
        SLV_SS = 2.0 - 1.1*SLV_F0*SLV_ag
        if SLV_SS <= 1.0: SLV_SS = 1.0
        if SLV_SS >= 1.6: SLV_SS = 1.6
        SLV_CC = 1.15*(SLV_Tc)**(-0.40)
        # segue SLC
        SLC_SS = 2.0 - 1.1*SLC_F0*SLC_ag
        if SLC_SS <= 1.0: SLC_SS = 1.0
        if SLC_SS >= 1.6: SLC_SS = 1.6
        SLC_CC = 1.15*(SLC_Tc)**(-0.40)

valori_calcolati = {
    "SLO": {"SS": SLO_SS, "CC": SLO_CC},
    "SLD": {"SS": SLD_SS, "CC": SLD_CC},
    "SLV": {"SS": SLV_SS, "CC": SLV_CC},
    "SLC": {"SS": SLC_SS, "CC": SLC_CC}
}
 # Aggiunta delle colonne SS e CC con i valori pre-calcolati
dfSL["SS"] = dfSL["StatoLimite"].map(lambda x: valori_calcolati.get(x, {}).get("SS", ""))
dfSL["CC"] = dfSL["StatoLimite"].map(lambda x: valori_calcolati.get(x, {}).get("CC", ""))

dfSL.to_csv(file_path, index=False)    
# Visualizzazione del dataframe aggiornato
st.write("### Parametri per ogni stato limite")
st.dataframe(dfSL)

if st.toggle("ℹ️ Vis. Tab 3.2.IV NTC 2018"):
    st.image("images/imgSS_CC.png", caption="Dettagli immagine", use_container_width=True)


# aggiunta coppie a datiInput
# Controlla se 'datiInput' esiste già e non è vuoto
#if 'input_data' in st.session_state and st.session_state['input_data']:
#    # Aggiungi nuove chiavi al primo (e unico) dizionario della lista
#    st.session_state['input_data'].update({
#        'catSuolo': catS,
#        'catTopo': catT,
#        'hH': hH,
#        'ST': ST
#    })
#else:
#    st.warning("Attenzione: 'datiInput' non è stato inizializzato correttamente.")

eta = 0.0
q = 0.0
etav = 0.0

if "input_backup" not in st.session_state:
    st.session_state["input_backup"] = {}  # Inizializza come dizionario

# Nuovi valori da aggiornare
new_data = {"catSuolo": catS, "catTopo": catT, "hH": hH, "ST": ST}
# Aggiornamento delle sole chiavi presenti in new_data
st.session_state.input_backup.update(new_data)


col1, col2, col3, col4 = st.columns([1,1.2,1,1])

if col1.button("🫨Spettri elastici"):
    st.switch_page('pages/5_🫨spettri_elastici.py')
if col2.button("🫣Spettri di progetto"):
    st.switch_page('pages/6_🫣spettri_di_progetto.py')
if col3.button('📍 Coord. Sito'):
    st.switch_page('pages/3_📍sito.py')
if col4.button('🔙 Dati generali'):
    st.switch_page('pages/2_📝dati_generali.py')






