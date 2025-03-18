import streamlit as st
import pandas as pd

import shutil
import time

   
st.markdown("---")
#st.title(" Azioni sismiche")
st.markdown("<h1 style='text-align: center;'>🛠️ Ripristino database </h1>", unsafe_allow_html=True)
st.markdown("---")



if st.button('Ripristina'):

    bck_file1 = "backup/Coordinate_bck.csv"
    bck_file2 = "backup/DatiGenerali_bck.csv"
    bck_file3 = "backup/DatiSpettri_bck.csv"
    bck_file4 = "backup/DatiStatiLimite_bck.csv"
    bck_file5 = "backup/punto_scelto_bck.csv"
    bck_file6 = "backup/RispostaLocale_bck.csv"

    dest_file1 = "files/Coordinate.csv"
    dest_file2 = "files/DatiGenerali.csv"
    dest_file3 = "files/DatiSpettri.csv"
    dest_file4 = "files/DatiStatiLimite.csv"
    dest_file5 = "files/punto_scelto.csv"
    dest_file6 = "files/RispostaLocale.csv"

    # Sovrascrive il file originale con il backup
    shutil.copy(bck_file1, dest_file1)
    shutil.copy(bck_file2, dest_file2)
    shutil.copy(bck_file3, dest_file3)
    shutil.copy(bck_file4, dest_file4)
    shutil.copy(bck_file5, dest_file5)
    shutil.copy(bck_file6, dest_file6)

    st.success("Database ripristinato con successo !")
    
    time.sleep(3)
    
    pagina = 'pages/1_🗂️main.py'
    st.switch_page(pagina)

