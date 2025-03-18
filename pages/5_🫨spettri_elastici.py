import streamlit as st
import pandas as pd

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

st.title("Spettri di risposta elastici")

if 'prot' not in st.session_state:
    st.session_state.prot = False

print ('prot analysis', st.session_state.prot)
if st.session_state.prot == False:
    st.info('unauthorized access')
    st.stop()
    

# Definiamo la funzione f(T)
def f(T, TB, TC, TD, ag, S, eta, F0):
    if T >= 0 and T < TB:
        return ag*S*eta*F0*(T/TB + 1/(eta*F0)*(1-T/TB))     # spettro per 0<=T<TB
    if T >= TB and T < TC:
        return ag*S*eta*F0                                  # spettro per TB<=T<TC
    if T >= TC and T < TD:
        return ag*S*eta*F0*(TC/T)                           # spettro per TC<=T<TD
    if T >= TD:
        return ag*S*eta*F0*(TC*TD/(T**2))                   # spettro per T>=TD

def fvert(T, TB, TC, TD, ag, S, eta, F0, Fv):
    if T >= 0 and T < TB:
        return ag*S*eta*Fv*(T/TB + 1/(eta*F0)*(1-T/TB))     # spettro per 0<=T<TBv
    if T >= TB and T < TC:
        return ag*S*eta*Fv                                  # spettro per TBv<=T<TCv
    if T >= TC and T < TD:
        return ag*S*eta*Fv*(TC/T)                           # spettro per TCv<=T<TDv
    if T >= TD:
        return ag*S*eta*Fv*(TC*TD/(T**2))                   # spettro per T>=TDv    

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

col1, col2, col3 = st.columns([2,1,1])
opzioniStatiLimite = ["SLO", "SLD", "SLV", "SLC"]
slSelected = col1.radio("Stato limite considerato", options=opzioniStatiLimite)

match slSelected:
    case "SLO":
        testoSL = "Stato Limite di Operatività"

    case "SLD":
        testoSL = "Stato Limite di Danno"

    case "SLV":
        testoSL = "Stato Limite di salvaguardia della Vita"

    case "SLC":
        testoSL = "Stato Limite di prevenzione del Collasso"

csi = col2.number_input("Smorzamento ξ(%)", min_value= 0.0, value= 5.0)  
eta = sqrt(10/(5+csi))
if eta < 0.55:
    eta = 0.55

#col3.write(f"η = {eta}")
col3.markdown(f"<p style='margin-top:35px; color: white; background-color:green; text-align: center'> ➩ &nbsp &nbsp  η = {eta: .4f}</p>", unsafe_allow_html=True)
st.write(f"(**{slSelected}**) - {testoSL}")

# Caricamento del file CSV
file_path = "files/DatiStatiLimite.csv"  # leggi file
dfSL = pd.read_csv(file_path)

# verifica se le colonne SS e CC esistono e se contengono valori non nulli
# Controllo se le colonne esistono

def dati_non_validi():
    
    if st.button("Input dati mancanti"):
        st.switch_page('pages/4_®️risposta_locale.py')
    
    st.stop()


if "SS" in dfSL.columns and "CC" in dfSL.columns:
    #st.success("Dati presenti e validi.")
    # Controllo se ci sono valori diversi da 0
    ss_valid = (dfSL["SS"] != 0).any()
    cc_valid = (dfSL["CC"] != 0).any()
    ss_has_zero = (dfSL["SS"] == 0).any()
    cc_has_zero = (dfSL["CC"] == 0).any()
    
    if ss_has_zero or cc_has_zero:
        flag_dati_validi = False
        st.warning("Sono presenti valori di SS o CC nulli. Premi il pulsante seguente per inserli")
        dati_non_validi()
        #st.success("Entrambe le colonne contengono valori diversi da 0.")
       
    else:
        flag_dati_validi = True
        st.success("Dati presenti e validi.")
        
else:
    st.error("Mancano dati fondamentali per definire gli spettri di risposta. Premi il pulsante seguente per inserirli." )
    dati_non_validi()




# Estrazione dati Stato Limite selezionato
TR_sl, ag_sl, F0_sl, Tc_sl, SS_sl, CC_sl = dfSL[dfSL["StatoLimite"] == slSelected].values[0][1:7]

#st.write(f"TR = {TR_sl} ")
#st.write(f"ag = {ag_sl: .3f} g")
#st.write(f"F0 = {F0_sl: .3f} ")
#st.write(f"Tc = {Tc_sl: .3f} s")
#st.write(f"Ss = {SS_sl: .3f} ")
#st.write(f"Cc = {CC_sl: .3f} ")

filtered_df = dfSL[dfSL["StatoLimite"] == slSelected]
st.dataframe(filtered_df, hide_index= True )

fileRL = "files/RispostaLocale.csv"  # leggi file
dfRispostaLocale = pd.read_csv(fileRL)

# calcolo S = SS*ST
ST = dfRispostaLocale.loc[0,'ST']
S = SS_sl * ST
st.write(f"S = SS * ST = {SS_sl}*{ST} = {S} ")

# calcolo TB, TC, TD
TC = Tc_sl * CC_sl          # 3.2.5
TB = TC/3                   # 3.2.6
TD = 4.0 * ag_sl + 1.6      # 3.2.7

#st.write(f"TB = {TB: .3f} s")
#st.write(f"TC = {TC: .3f} s")
#st.write(f"TD = {TD: .3f} s")

# Definizione dell'intervallo di T
T_min, T_max = 0, 4     # Estremi dell'intervallo
num_points = 50         # Numero di punti desiderati

# Punti caratteristici da includere TB, TC, TD

# Creiamo l'array di T
T_values = np.linspace(T_min, T_max, num_points)  # Genera punti equidistanti
T_values = np.append(T_values, [TB, TC, TD])  # Aggiunge i punti caratteristici
T_values = np.unique(np.sort(T_values))  # Ordina ed elimina duplicati

# Calcoliamo a = f(T) per tutti i valori
a_values = [f(T, TB, TC, TD, ag_sl, S, eta, F0_sl) for T in T_values]

# Creiamo un DataFrame per Plotly
df = pd.DataFrame({"T": T_values, "Sd": a_values})

# Calcoliamo il massimo valore di "a" e impostiamo un margine superiore del 15%
a_max = max(a_values) * 1.15

# Creazione del grafico con Plotly
fig = go.Figure()

# Linea principale
fig.add_trace(go.Scatter(
    x=df["T"], 
    y=df["Sd"], 
    mode="lines+markers", 
    name="Sd = f(T)",
    marker=dict(size=6),
    line=dict(width=2)
))

# Punti caratteristici
fig.add_trace(go.Scatter(
    x=[TB, TC, TD], 
    y=[f(TB, TB, TC, TD, ag_sl, S, eta, F0_sl), 
       f(TC, TB, TC, TD, ag_sl, S, eta, F0_sl), 
       f(TD, TB, TC, TD, ag_sl, S, eta, F0_sl)], 
    mode="markers", 
    marker=dict(color="red", size=10), 
    name="Punti caratteristici"
))

# Aggiunta delle linee verticali in corrispondenza di TB, TC e TD
for T_char in [TB, TC, TD]:
    fig.add_trace(go.Scatter(
        x=[T_char, T_char], 
        y=[0, a_max/1.15],  
        mode="lines",
        line=dict(color="gray", width=1.5, dash="dash"),
        name=f"T = {T_char:.2f}"
    ))


# Aggiunta di etichette accanto a TB, TC, TD
etichetta_offset = {"TB": -20, "TC": 20, "TD": -20}  # Offset per spostare le etichette (negativo = sinistra, positivo = destra)
for nome, valore in zip(["TB", "TC", "TD"], [TB, TC, TD]):
    fig.add_annotation(
        x=valore, 
        y=f(valore, TB, TC, TD, ag_sl, S, eta, F0_sl),  
        text=nome,  
        showarrow=True,  
        arrowhead=2,  
        ax=etichetta_offset[nome],  # Sposta l'etichetta a sinistra (-) o destra (+)
        ay=-30,  # Sposta l'etichetta verticalmente
        font=dict(size=12, color="black"),
        arrowcolor="black"
    )

# **Aggiungere le etichette numeriche ogni 0.5 secondi sull'asse delle ascisse (X)**
tick_vals = np.arange(0, T_max+0.5, 0.5)  # Etichette numeriche ogni 0.5 secondi

# Personalizzazione asse x con etichette numeriche
fig.update_xaxes(
    tickmode="array",
    tickvals=tick_vals,  
    ticktext=[str(i) for i in tick_vals],  # Etichette numeriche come stringhe
    showgrid=True,  
    zeroline=True,  
    zerolinewidth=2,
    zerolinecolor="black"
)



# Assicura che l'asse verticale sia visibile
fig.update_yaxes(
    showgrid=True,  
    zeroline=True,  # Mostra l'asse x principale
    zerolinewidth=2,
    zerolinecolor="black"
)

# Layout del grafico
fig.update_layout(
    title=f"{slSelected} - Diagramma  Sd (g) - T (s) - Componente orizzontale",
    xaxis_title="T (s)",
    yaxis_title="Sd (g)",
    yaxis=dict(range=[0, a_max]),  
    showlegend=True,
    hovermode="x unified",  
    template="plotly_white"
)

# Mostrare il grafico interattivo in Streamlit
st.plotly_chart(fig)

# Aggiungiamo una colonna 'Etichetta' che contiene 'TB', 'TC', 'TD' quando T è uguale a uno di questi
df[''] = df['T'].apply(lambda x: 'TB' if x == TB else ('TC' if x == TC else ('TD' if x == TD else '')))

# Evidenziare le righe corrispondenti a TB, TC e TD
def highlight_special_rows(row):
    if row["T"] in [TB, TC, TD]:
        return ["background-color: yellow"] * len(row)  # Evidenzia tutta la riga
    return [""] * len(row)

# Mostriamo la tabella in Streamlit con evidenziazione
st.write("**Tabella punti spettro di risposta elastico - componente orizzontale**")
st.dataframe(df.style.apply(highlight_special_rows, axis=1), hide_index= True)

# -------------------------------------------------------------------------------------
# Spettro di risposta elastico - Componente verticale
# -------------------------------------------------------------------------------------

Fv = 1.35*F0_sl*ag_sl**(0.5) 
SSv = 1.0
TBv = 0.05
TCv = 0.15
TDv = 1.0
Sv = SSv*ST

st.write(f"Sv = SSv * ST = {SSv}*{ST} = {Sv} ")

# costruzione spettro
# Definizione dell'intervallo di T
Tv_min, Tv_max = 0, 4     # Estremi dell'intervallo
num_points = 50         # Numero di punti desiderati

# Punti caratteristici da includere TB, TC, TD

# Creiamo l'array di Tv
Tv_values = np.linspace(Tv_min, Tv_max, num_points)  # Genera punti equidistanti
Tv_values = np.append(Tv_values, [TBv, TCv, TDv])  # Aggiunge i punti caratteristici
Tv_values = np.unique(np.sort(Tv_values))  # Ordina ed elimina duplicati

# Calcoliamo a = f(Tv) per tutti i valori
av_values = [fvert(Tv, TBv, TCv, TDv, ag_sl, Sv, eta, F0_sl, Fv) for Tv in Tv_values]

# Creiamo un DataFrame per Plotly
dfv = pd.DataFrame({"Tv": Tv_values, "Sdv": av_values})

# Calcoliamo il massimo valore di "a" e impostiamo un margine superiore del 15%
av_max = max(av_values) * 1.15

# Creazione del grafico con Plotly
figv = go.Figure()

# Linea principale
figv.add_trace(go.Scatter(
    x=dfv["Tv"], 
    y=dfv["Sdv"], 
    mode="lines+markers", 
    name="Sdv = f(Tv)",
    marker=dict(size=6),
    line=dict(width=2)
))

# Punti caratteristici
figv.add_trace(go.Scatter(
    x=[TBv, TCv, TDv], 
    y=[fvert(TBv, TBv, TCv, TDv, ag_sl, Sv, eta, F0_sl, Fv), 
       fvert(TCv, TBv, TCv, TDv, ag_sl, Sv, eta, F0_sl, Fv), 
       fvert(TDv, TBv, TCv, TDv, ag_sl, Sv, eta, F0_sl, Fv)], 
    mode="markers", 
    marker=dict(color="red", size=10), 
    name="Punti caratteristici"
))

# Aggiunta delle linee verticali in corrispondenza di TBv, TCv e TDv
for Tv_char in [TBv, TCv, TDv]:
    figv.add_trace(go.Scatter(
        x=[Tv_char, Tv_char], 
        y=[0, av_max/1.15],  
        mode="lines",
        line=dict(color="gray", width=1.5, dash="dash"),
        name=f"T = {Tv_char:.2f}"
    ))


# Aggiunta di etichette accanto a TBv, TCv, TDv
etichettav_offset = {"TBv": -20, "TCv": 20, "TDv": -20}  # Offset per spostare le etichette (negativo = sinistra, positivo = destra)
for nomev, valorev in zip(["TBv", "TCv", "TDv"], [TBv, TCv, TDv]):
    figv.add_annotation(
        x=valorev, 
        y=fvert(valorev, TBv, TCv, TDv, ag_sl, Sv, eta, F0_sl, Fv),  
        text=nomev,  
        showarrow=True,  
        arrowhead=2,  
        ax=etichettav_offset[nomev],  # Sposta l'etichetta a sinistra (-) o destra (+)
        ay=-30,  # Sposta l'etichetta verticalmente
        font=dict(size=12, color="black"),
        arrowcolor="black"
    )

# **Aggiungere le etichette numeriche ogni 0.5 secondi sull'asse delle ascisse (X)**
tickv_vals = np.arange(0, Tv_max+0.5, 0.5)  # Etichette numeriche ogni 0.5 secondi

# Personalizzazione asse x con etichette numeriche
figv.update_xaxes(
    tickmode="array",
    tickvals=tickv_vals,  
    ticktext=[str(iv) for iv in tickv_vals],  # Etichette numeriche come stringhe
    showgrid=True,  
    zeroline=True,  
    zerolinewidth=2,
    zerolinecolor="black"
)



# Assicura che l'asse verticale sia visibile
figv.update_yaxes(
    showgrid=True,  
    zeroline=True,  # Mostra l'asse x principale
    zerolinewidth=2,
    zerolinecolor="black"
)

# Layout del grafico
figv.update_layout(
    title=f"{slSelected} - Diagramma  Sdv (g) - Tv (s) - Componente verticale",
    xaxis_title="Tv (s)",
    yaxis_title="Sdv (g)",
    yaxis=dict(range=[0, av_max]),  
    showlegend=True,
    hovermode="x unified",  
    template="plotly_white"
)

# Mostrare il grafico interattivo in Streamlit
st.plotly_chart(figv)

# Aggiungiamo una colonna 'Etichetta' che contiene 'TB', 'TC', 'TD' quando T è uguale a uno di questi
dfv[''] = dfv['Tv'].apply(lambda x: 'TBv' if x == TBv else ('TCv' if x == TCv else ('TDv' if x == TDv else '')))

# Evidenziare le righe corrispondenti a TBv, TCv e TDv
def highlight_SpettroVert(rowv):
    if rowv["Tv"] in [TBv, TCv, TDv]:
        return ["background-color: yellow"] * len(rowv)  # Evidenzia tutta la riga
    return [""] * len(rowv)

# Mostriamo la tabella in Streamlit con evidenziazione
st.write("**Tabella punti spettro di risposta elastico - componente verticale**")
st.dataframe(dfv.style.apply(highlight_SpettroVert, axis=1), hide_index= True)


# Percorso del file
file_spettri = "files/DatiSpettri.csv"

# Carica il file CSV esistente
df_existing = pd.read_csv(file_spettri)

# Aggiorna solo la colonna 'eta' mantenendo inalterate le altre colonne
df_existing['eta'] = eta  # Assumendo che 'eta' sia un valore o una lista con la stessa lunghezza

# Salva di nuovo il file senza modificare le altre colonne
df_existing.to_csv(file_spettri, index=False)


col1, col2, col3, col4 = st.columns([1.2,1,1,1])

if col1.button("🫨Spettri di progetto"):
    st.switch_page('pages/6_🫣spettri_di_progetto.py')
if col2.button("🔙Risposta locale"):
    st.switch_page('pages/4_®️risposta_locale.py')


# backup dati di input fino a questo punto
# richiamo archivi
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

if "input_backup" not in st.session_state:
    st.session_state["input_backup"] = {}  # Inizializza come dizionario

# Nuovi valori da aggiornare
new_data = {"PH": 1, "JA": str(JA), "eta": eta, "q": 0.0, "etav": 0.0}
# Aggiornamento delle sole chiavi presenti in new_data
st.session_state.input_backup.update(new_data)

df_inputBackup = pd.read_csv("files/inputBackup.csv")   # lettura file

df_inputBackup['JA'] = df_inputBackup['JA'].astype(str)
df_inputBackup['catTopo'] = df_inputBackup['catTopo'].astype(str)
df_inputBackup.loc[0] = st.session_state['input_backup']
df_inputBackup.to_csv("files/inputBackup.csv", index=False)
#st.dataframe(df_inputBackup, hide_index= True)

