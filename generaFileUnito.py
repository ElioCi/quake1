import streamlit as st
import pandas as pd
from datetime import datetime

def SalvaDati():
    # Carica i file CSV
    coordinate = pd.read_csv("files/Coordinate.csv")
    dati_generali = pd.read_csv("files/DatiGenerali.csv")
    dati_spettri = pd.read_csv("files/DatiSpettri.csv")
    dati_SL = pd.read_csv("files/DatiStatiLimite.csv")
    punto_scelto = pd.read_csv("files/punto_scelto.csv")
    risposta_locale = pd.read_csv("files/RispostaLocale.csv")



    # Crea una colonna vuota
    #colonna_vuota = pd.DataFrame(['' for _ in range(max(len(dati_generali), len(dati_piping)))], columns=[''])
    colonna_vuota = pd.DataFrame({'': [None] * max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))})
    # Inserisci l'intestazione personalizzata nella colonna vuota
    colonna_vuota.columns = [f"SismaNTC1 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"]

    colDG =pd.DataFrame({'Dati_Generali': [None] * max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))})
    colDS =pd.DataFrame({'Dati_Spettri': [None] * max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))})
    colSL =pd.DataFrame({'Dati_Stati_Limite': [None] * max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))})
    colPS =pd.DataFrame({'Punto_Scelto': [None] * max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))})
    colRL =pd.DataFrame({'Risposta_Locale': [None] * max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))})


    # Allinea le righe dei files in modo che abbiano la stessa lunghezza
    coordinate = coordinate.reindex(range(max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))))
    dati_generali = dati_generali.reindex(range(max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))))
    dati_spettri = dati_spettri.reindex(range(max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))))
    dati_SL = dati_SL.reindex(range(max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))))
    punto_scelto = punto_scelto.reindex(range(max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))))
    risposta_locale = risposta_locale.reindex(range(max(len(coordinate),len(dati_generali), len(dati_spettri), len(dati_SL), len(punto_scelto), len(risposta_locale))))

    # Unisci i due DataFrame con la colonna vuota tra di loro
    dati_uniti = pd.concat([colonna_vuota, coordinate, colDG, dati_generali, colDS, dati_spettri, colSL, dati_SL, colPS, punto_scelto, colRL, risposta_locale ], axis=1)

    # Forzare il formato decimale con il punto per tutte le colonne numeriche
    dati_uniti = dati_uniti.map(lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else x)
    
    # Permetti all'utente di scaricare il file
    csv = dati_uniti.to_csv(index=False)
    st.download_button(label="💾 Download file sismaNTC_dati.CSV", data=csv, file_name="sismaNTC_dati.csv", mime="text/csv", help= '***click here to save data in your personal drive***')

