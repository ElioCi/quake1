import streamlit as st
import pandas as pd
from generaFileUnito import SalvaDati


st.title("Salva progetto in archivio locale")


# leggi dagli archivi i dati presenti per vedere se c'è qualche modifica
#leggi dati di input da DatiGenerali.csv
with open('files/DatiGenerali.csv') as file_input:
    dfgen = pd.read_csv(file_input)   # lettura file e creazione
    dfgen.drop(dfgen.columns[dfgen.columns.str.contains('unnamed', case= False)], axis=1, inplace= True)

JA = dfgen.loc[0,'JAccount']
prj = dfgen.loc[0,'Project']
loc = dfgen.loc[0,'Location']
VN = dfgen.loc[0.0,'VN']
CU = dfgen.loc[0.0,'CU']
VR = dfgen.loc[0.0,'VR']

#leggi coordinate
with open('files/Coordinate.csv') as file_coord:
    dfcoord = pd.read_csv(file_coord)   # lettura file

lat = dfcoord.loc[0,'Latitudine']
lon = dfcoord.loc[0,'Longitudine']

#leggi risposta locale
with open('files/RispostaLocale.csv') as file_RL:
    dfRL = pd.read_csv(file_RL)   # lettura file

catS = dfRL.loc[0,'Catsuolo']
catT = dfRL.loc[0,'CatTopo']
hH = dfRL.loc[0,'hH']
ST = dfRL.loc[0,'ST']

#leggi dati x spettri
with open('files/DatiSpettri.csv') as file_datiSpettri:
    dfDS = pd.read_csv(file_datiSpettri)   # lettura file
   
eta = dfDS.loc[0,'eta']

if 'q' in dfDS.columns:
    q = dfDS.loc[0, 'q']
else:
    q = 0.0

if 'etav' in dfDS.columns:
    etav = dfDS.loc[0, 'etav']
else:
    etav = 0.0

if "input_data" not in st.session_state:
    st.session_state["input_data"] = {}  # Inizializza come dizionario

# memorizzo dati in st_session_state.input_backup
st.session_state['input_data'] = {
    'PH': 1,
    'JA': JA,
    'Prj': prj,
    'Loc': loc,
    'VN': VN,
    'CU': CU,
    'VR': VR,
    'lat': lat,
    'lon': lon,
    'catSuolo': catS,
    'catTopo': catT,
    'hH': hH,
    'ST': ST,
    'eta': eta,
    'q': 0.0,
    'etav': 0.0,
}
# crea dataframe
df1_1riga = pd.DataFrame(st.session_state['input_data'], index = [0])
# Crea una seconda riga con valori diversi per 'q' ed 'etav'
second_row = st.session_state['input_data'].copy()
second_row['PH'] = 2  # Nuovo valore per 'PH'
second_row['q'] = q  # Nuovo valore per 'q'
second_row['etav'] = etav  # Nuovo valore per 'etav'

# Aggiungi la seconda riga al DataFrame
df1 = pd.concat([df1_1riga, pd.DataFrame([second_row])], ignore_index=True)



# leggi dati da inputBackup
with open('files/inputBackup.csv') as file_inputBackup:
    df2 = pd.read_csv(file_inputBackup)   # lettura file



# Funzione per evidenziare le differenze tra le righe
def highlight_differences(row1, row2):
    # Crea una maschera booleana per le differenze
    mask = row1 != row2
    return ['background-color: yellow' if val else '' for val in mask]


# Verifica se i DataFrame sono uguali
if df1.equals(df2):
    # Se i DataFrame sono uguali
    st.success("Valori di calcolo aggiornati e congruenti! Pertanto procedo la generazione del file dati...")
    SalvaDati()
else:
    # Se ci sono differenze, evidenzia le differenze
    st.warning("Calcoli non aggiornati. Rieseguire il calcolo di degli spettri di risposta.")
    
    # Creiamo una nuova tabella per i valori diversi
    differences = []
    for col in df1.columns:
        for i, (val1, val2) in enumerate(zip(df1[col], df2[col])):
            if val1 != val2:
                #ph_value = df2.loc[i, 'PH']   #'PH'  colonna in df2
                differences.append({
                    'PH': i+1,
                    #'PH': ph_value,  # Aggiungi il valore di PH
                    'Colonna': col,
                    'Valore aggiornato': val1,
                    'Valore precedente': val2
                })
    
    # Mostra le differenze in una tabella separata
    if differences:
        diff_df = pd.DataFrame(differences)
        st.write("Tabella dati modificati:")
        st.dataframe(diff_df, hide_index= True)
    
        # Analizza i valori unici nella colonna 'PH' e mostra il risultato
        unique_ph_values = diff_df['PH'].unique()  # Valori unici nella colonna PH
        
        if len(unique_ph_values) == 1:
            if 1 in unique_ph_values:
                st.write("E' necessario ricalcolare gli spettri elastici.") #La colonna 'PH' contiene solo il valore 1
            elif 2 in unique_ph_values:
                st.write("E' necessario ricalcolare gli spettri di progetto.") # La colonna 'PH' contiene solo il valore 2
        elif len(unique_ph_values) == 2:
            st.write("E' necessario ricalcolare sia gli spettri elastici che quelli di progetto.") #La colonna 'PH' contiene sia il valore 1 che il valore 2.
        else:
            st.write("La colonna 'PH' contiene valori diversi da 1 e 2.")


    # Evidenziamo le differenze nei DataFrame
    df_comparison = df1.style.apply(lambda x: highlight_differences(x, df2.loc[x.name]), axis=1)

    st.write("Parametri di calcolo per PH=1 (spettri elastici) e PH=2 (spettri di progetto) - **In giallo i dati obsoleti**:")
    st.dataframe(df_comparison, hide_index= True)


