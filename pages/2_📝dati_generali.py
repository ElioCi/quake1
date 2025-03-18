import streamlit as st

import pandas as pd
from math import log
import numpy as np
import csv
import os

# variabile per memorizzare i dati di input
if "input_data" not in st.session_state:
    st.session_state.input_data = {}

# inizializza session_state
if 'newFlag' not in st.session_state:
    st.session_state.newFlag = 'none'
if 'dataGen' not in st.session_state:
    st.session_state['dataGen'] = []
if 'JAccount' not in st.session_state:
    st.session_state.JAccount = ""
if 'Project' not in st.session_state:
    st.session_state.Project = ""
if 'Location' not in st.session_state:
    st.session_state.Location = ""

if 'VR' not in st.session_state:
    st.session_state.VR = 0.0 

if 'datiRispostaLocale' not in st.session_state:
    st.session_state['datiRispostaLocale'] = []
if 'CatSuolo' not in st.session_state:
    st.session_state.CatSuolo = ""     
if 'CatTopo' not in st.session_state:
    st.session_state.CatTopo = "" 


if 'dataConfirmed' not in st.session_state:
    st.session_state.dataConfirmed = False  

if 'flagChanges' not in st.session_state:
    st.session_state.flagChanges = False  

# functions
# Funzione per aggiornare lo stato quando cambia la selectbox

def ClasseUso(valoriCU):
    
    if st.session_state.CU != 0.0:
        valoreCU_da_cercare = st.session_state.CU
        opzione_CUtrovata = next((key for key, value in valoriCU.items() if value == valoreCU_da_cercare), None)
        #print('st.session_state.CU, opzione_trovata = ',st.session_state.CU, opzione_CUtrovata )
    # Ottieni l'indice della chiave se esiste
    if opzione_CUtrovata is not None:
        indiceCU = list(valoriCU.keys()).index(opzione_CUtrovata) if opzione_CUtrovata else None
        
    elif opzione_CUtrovata is None:
        indiceCU = 4
    
    return indiceCU

#print ('newFlag = ', st.session_state.newFlag)
#---in caso non hai fatto alcuna scelta torna alla main page ---
if st.session_state.newFlag == "none":
    pagina = 'pages/1_🗂️main.py'
    st.switch_page(pagina)
#---------------------------------------------


st.sidebar.info(st.session_state.newFlag)

if st.session_state.newFlag == "stored":
    # Titolo dell'applicazione
    st.title('📝 Dati generali - Stored project')
    st.session_state.flagChanges = False
    #st.subheader('Environmental data')

elif st.session_state.newFlag == "new":
    st.title('📝 Dati generali - New project')
    st.session_state.flagChanges = True


with st.expander("🆘 Help"):
    st.markdown("""
    - **Che cosa fare qui?**  
      Input or change general data as: codice progetto, titolo e localizzazione, vita nominale, classe d'uso, vita relativa.
      Questi ultimi tre valori saranno usati nelle analisi.                
    - **Prima di andare avanti ...**  
      Assicurati di avere introdotto i valori corretti e conferma spuntando la checkbox ***Conferma dati***. 
      Nota che fino a quando la casella non sarà spuntata, non sarà possibile eseguire le analisi successive.
    - **Ulteriori informazioni:**  
      clicca su ℹ️ info button menu
    """)

#leggi dati di input da DatiGenerali.csv
with open('files/DatiGenerali.csv') as file_input:
    dfgen = pd.read_csv(file_input)   # lettura file e creazione
    dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

st.session_state.JAccount = dfgen.loc[0,'JAccount']
st.session_state.Project = dfgen.loc[0,'Project']
st.session_state.Location = dfgen.loc[0,'Location']
st.session_state.VN_selected = dfgen.loc[0, 'VNSelected']
st.session_state.VN = dfgen.loc[0.0,'VN']
st.session_state.CU = dfgen.loc[0.0,'CU']
st.session_state.VR = dfgen.loc[0.0,'VR']

col1, col2 = st.columns([1,3])
JAccount = col1.text_input('Job Account', value = st.session_state.JAccount)
Project = col2.text_input('Project', value = st.session_state.Project)
Location = col2.text_input('Location', value = st.session_state.Location)

#col1, col2 = st.columns([3,1])

#VN = col1.number_input('Vita nominale della costruzione (anni)', min_value=0.0, step=0.1, value= st.session_state.VN )
# Definizione delle opzioni e mappatura dei valori numerici
valoriVN = {
    '1- Costruzioni temporanee e provvisorie': 10.0,
    '2- Costruzioni con livelli di prestazione ordinari': 50.0,
    '3- Costruzioni con livelli di prestazioni elevati': 100.0
}


opzioniVN = list(valoriVN.keys())
if 'VN' not in st.session_state:
    st.session_state.VN = 10.0  # Valore di default
if 'VN_selected' not in st.session_state:
    # Trova la chiave corrispondente al valore numerico di VN
    st.session_state.VN_selected = next(
        (key for key, value in valoriVN.items() if value == st.session_state.VN), opzioniVN[0]
    )

def update_VN():
    #st.write("update_VN() eseguita!")  # Questo dovrebbe apparire in output
    st.session_state.VN = valoriVN[st.session_state.VN_selected]
    
# Selectbox con on_change
st.selectbox(
    '(Rif. Tab. 2.4.I NTC 2018) - Tipo di costruzione per valutazione Vita nominale "VN"',
    options=opzioniVN,
    key="VN_selected",
    on_change= update_VN()
)

VN_selected = st.session_state.VN_selected
# Mostra il valore aggiornato
#st.write(f"VN selezionato: {st.session_state.VN_selected}")
#st.write(f"Valore selezionato: {st.session_state.VN}")

VN = st.session_state.VN
   

optCU1 = 'Classe I - Costruzioni con presenza solo occasionale di persone, edifici agricoli.'
optCU2 = 'Classe II - Costruzioni il cui uso preveda normali affollamenti, senza contenuti pericolosi per l’ambiente e senza funzioni pubbliche e sociali essenziali. Industrie con attività non pericolose per l’ambiente. Ponti, opere infrastrutturali, reti viarie non ricadenti in Classe d’uso III o in Classe d’uso IV, reti ferroviarie la cui interruzione non provochi situazioni di emergenza. Dighe il cui collasso non provochi conseguenze rilevanti.'
optCU3 = 'Classe III - Costruzioni il cui uso preveda affollamenti significativi. Industrie con attività pericolose per l’ambiente. Reti viarie extraurbane non ricadenti in Classe d’uso IV. Ponti e reti ferroviarie la cui interruzione provochi situazioni di emergenza. Dighe rilevanti per le conseguenze di un loro eventuale collasso.'
optCU4 = 'Classe IV - Costruzioni con funzioni pubbliche o strategiche importanti, anche con riferimento alla gestione della protezione civile in caso di calamità. Industrie con attività particolarmente pericolose per l’ambiente. Reti viarie di tipo A o B, di cui al D.M. 5 novembre 2001, n. 6792, “Norme funzionali e geometriche per la costruzione delle strade”, e di tipo C quando appartenenti ad itinerari di collegamento tra capoluoghi di provincia non altresì serviti da strade di tipo A o B. Ponti e reti ferroviarie di importanza critica per il mantenimento delle vie di comunicazione, particolarmente dopo un evento sismico. Dighe connesse al funzionamento di acquedotti e a impianti di produzione di energia elettrica.'
optCU5 = 'Classe Personalizzata - Valore di Cu personalizzato impostato manualmente'

if st.session_state.CU != (0.7 or 1.0 or 1.5 or 2.0 or 2.2):
    valoriCU = {optCU1: 0.7, optCU2: 1.0, optCU3: 1.50, optCU4: 2.0, optCU5: st.session_state.CU}
else:
    valoriCU = {optCU1: 0.7, optCU2: 1.0, optCU3: 1.50, optCU4: 2.0, optCU5: 2.2}

#print ('valoriCU 5 =', valoriCU[optCU5])
#if st.session_state.CU != 0.0:
#    valoreCU_da_cercare = st.session_state.CU
#    opzione_CUtrovata = next((key for key, value in valoriCU.items() if value == valoreCU_da_cercare), None)
#    #print('st.session_state.CU, opzione_trovata = ',st.session_state.CU, opzione_CUtrovata )
#    # Ottieni l'indice della chiave se esiste
#    if opzione_CUtrovata is not None:
#        indiceCU = list(valoriCU.keys()).index(opzione_CUtrovata) if opzione_CUtrovata else None
#    elif opzione_CUtrovata is None:
#        indiceCU = 4
#else:
#    indiceCU = 0

opzioniCU = list(valoriCU.keys())

if 'CU' not in st.session_state:
    st.session_state.CU = 0.7  # Valore di default

   
if 'CU_selected' not in st.session_state:
    # Trova la chiave corrispondente al valore numerico di CU
    st.session_state.CU_selected = next(
        (key for key, value in valoriCU.items() if value == st.session_state.CU), opzioniCU[4]
    )
   
def update_CU():
    #st.write("update_CU() eseguita!")  # Questo dovrebbe apparire in output
    st.session_state.CU = valoriCU[st.session_state.CU_selected]

# Selectbox con on_change
st.selectbox(
    '(rif. Tab. 2.4.II NTC 2018) - Classe Uso',
    options=opzioniCU,
    key="CU_selected",
    on_change= update_CU()

)
# Mostra il valore aggiornato
#st.write(f"CU selezionato: {st.session_state.CU_selected}")
#st.write(f"Valore selezionato da CU: {st.session_state.CU}")

CU = st.session_state.CU

st.markdown("")
col1, col2, col3, col4 = st.columns([0.8,1,1,1])
col1.markdown("<p style='margin-top:35px;'>Cu = </p>", unsafe_allow_html=True)

CU = col2.number_input("-", value=CU, max_value=3.0, step=0.1)

if CU != st.session_state.CU:
    
    st.session_state.CU = CU
    valoriCU[optCU5] = st.session_state.CU  # Cambia il valore associato a optCU5
    col3.markdown("<p style='margin-top:35px; color: white; background-color:red;'>&nbsp Valore Cu personalizzato</p>", unsafe_allow_html=True)


#st.session_state.indiceCU = ClasseUso(valoriCU)

#st.write('indiceCU = ', st.session_state.indiceCU)
#col2.markdown(f"Cu = {CU}")
col1, col2, col3, col4 = st.columns([1,1,1,1])
VR = VN * CU
if VR <= 35:
    VR= 35

#VN = "{:.1f}".format(VN)
#VR = "{:.1f}".format(VR)

col1.markdown(f"VN = {VN: .1f} anni")
col2.markdown(f"**VR =  {VR: .1f} anni**")

st.session_state['dataGen'] = [{
    'JAccount': JAccount,
    'Project': Project,
    'Location': Location,
    'VNSelected': VN_selected,
    'VN': VN,
    'CU': CU,
    'VR': VR,
}]

df = pd.DataFrame(st.session_state['dataGen'])
st.subheader('Sommario dati generali')
st.dataframe(df, hide_index= True)
df.to_csv("files/DatiGenerali.csv", index= False)   # salva dati generali


st.write("")
st.markdown("Periodo di ritorno azione sismica (anni) - TR")
PVR81 = -VR/log(1-0.81)
PVR63 = -VR/log(1-0.63)
PVR10 = -VR/log(1-0.10)
PVR5 = -VR/log(1-0.05)

if PVR81 < 30:
    PVR81 = 30
elif PVR81 > 2475:
    PVR81 = 2475
if PVR63 < 30:
    PVR63 = 30
elif PVR63 > 2475:
    PVR63 = 2475
if PVR10 < 30:
    PVR10 = 30
elif PVR10 > 2475:
    PVR10 = 2475
if PVR5 < 30:
    PVR5 = 30
elif PVR5 > 2475:
    PVR5 = 2475
st.markdown ("<u>Stati limite di esercizio:</u>", unsafe_allow_html=True)
st.markdown(f'SLO - PVR = 81% -->  &nbsp; &nbsp; {PVR81: .0f}')
st.markdown(f'SLD - PVR = 63% -->  &nbsp; &nbsp; {PVR63: .0f}')
st.markdown ("<u>Stati limite ultimi:</u>", unsafe_allow_html=True)
st.markdown(f'SLV - PVR = 10% --->  &nbsp; &nbsp; {PVR10: .0f}')
st.markdown(f'SLC - PVR = 5% ---> &nbsp; &nbsp; {PVR5: .0f}', unsafe_allow_html=True)
st.markdown("---")

#CU = col2.number_input("Classe d'uso della costruzione (Cu)", min_value=-273.0, step=0.1,  value= st.session_state.CU)

with open('files/Coordinate.csv') as file_coordinate:
    dfcoord = pd.read_csv(file_coordinate)   # lettura file e creazione

    #dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

#btnSito = st.empty()
col1, col2, col3 = st.columns([1,1,2])
col1.markdown("**Coordinate Sito**")

st.dataframe(dfcoord, hide_index=True)

if col2.button("📍Cambia Sito"):
    st.switch_page('pages/3_📍sito.py')

# Definisci il layout della colonna
#col1 = st.columns(1)[0]
# Pulsante per acquisire i dati

#col1, col2, col3 = st.columns([1,1,1])
#checkbox_state = col1.checkbox('Data confirmed', value=st.session_state.dataConfirmed)
#checkbox_state = col1.checkbox('Data confirmed')
# Pulsante per acquisire i dati
#if checkbox_state:

# dati Stati limite Probabilistici
st.session_state['datiSL'] = {
    'StatoLimite': ['SLO', 'SLD', 'SLV', 'SLC'],
    'TR': [round(PVR81), round(PVR63), round(PVR10), round(PVR5)]
}
st.session_state.dataConfirmed = True
#st.success('Data confirmed and stored successfully! Double click to untick checkbox.')
df_SL = pd.DataFrame(st.session_state['datiSL'])
st.subheader('Parametri di Normativa')
#st.write(f'Coordinate: Lat.={dfcoord.loc[0, "Latitudine"]} Lon.={dfcoord.loc[0,"Longitudine"]}')
#st.dataframe(df_SL, hide_index= True)
df_SL.to_csv("files/DatiStatiLimite.csv", index=False)  
# Carica i dati dai file CSV
punto_scelto = pd.read_csv("files/punto_scelto.csv")
dati_stati_limite = pd.read_csv("files/DatiStatiLimite.csv")
# Esegui l'interpolazione per ogni colonna (ag, F0, Tc)
for col in ["ag", "F0", "Tc"]:
    dati_stati_limite[col] = np.interp(
        dati_stati_limite["TR"],  # Valori da interpolare
        punto_scelto["T"],        # Ascisse note
        punto_scelto[col]         # Valori noti
    )
# Salva il file aggiornato
dati_stati_limite.to_csv("files/DatiStatiLimite.csv", index=False)
st.dataframe(dati_stati_limite, hide_index= True)

# else:
    
    #st.session_state.dataConfirmed = False
    #st.warning('Data not confirmed! Double click to tick checkbox and confirm input data.')
    
    #df = pd.DataFrame(st.session_state['dataGen'])
    #st.subheader('Summary of general data')
    #st.dataframe(df, hide_index= True)
    #df.to_csv("files/DatiGenerali.csv")   # salva dati su DatiPiping      

# memorizzo dati in st_session_state.input_backup
#st.session_state['input_data'] = ({
#    'JA': JAccount,
#    'Prj': Project,
#    'Loc': Location,
#    'VN': VN,
#    'CU': CU,
#    'VR': VR,
#    'lat': dfcoord.loc[0,'Latitudine'],
#    'lon': dfcoord.loc[0,'Longitudine'],

#})

catS = ""
catT = ""
hH = 0.0
ST = 0.0
eta = 0.0
q = 0.0
etav = 0.0

if "input_backup" not in st.session_state:
    st.session_state["input_backup"] = {}  # Inizializza come dizionario

fase = 0
# memorizzo dati in st_session_state.input_backup
st.session_state['input_backup'] = {
    'PH': fase,
    'JA': JAccount,
    'Prj': Project,
    'Loc': Location,
    'VN': VN,
    'CU': CU,
    'VR': VR,
    'lat': dfcoord.loc[0,'Latitudine'],
    'lon': dfcoord.loc[0,'Longitudine'],
    'catSuolo': catS,
    'catTopo': catT,
    'hH': hH,
    'ST': ST,
    'eta': eta,
    'q': q,
    'etav': etav,
}



col1, col2, col3, col4 = st.columns([1,1,1,1])

if col1.button("®️Risposta locale"):
    st.switch_page('pages/4_®️risposta_locale.py')
# Ritorno a Main
if col2.button('🔙 Main'):
    st.switch_page('pages/1_🗂️main.py')





