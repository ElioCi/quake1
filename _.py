import streamlit as st
import json
    
from urllib.parse import urlparse, parse_qs
import requests
import jwt
from jwt import PyJWTError
import time
    
if 'prot' not in st.session_state or not st.session_state.prot:
    st.session_state.prot = False

# Chiave segreta utilizzata per firmare il token
SECRET_KEY = 'EC1'

# Funzione per verificare il token
def verify_token(token):
    try:
        # Decodifica e verifica il token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token
    except PyJWTError as e:
        # Token non valido o scaduto
        st.error("Token invalid or expired: " + str(e))
        return None

# Acquisisci il token dai parametri dell'URL
# query_params = st.experimental_get_query_params()
query_params = st.query_params

#token = query_params.get("token", [None])[0]
token = query_params.get("token", [None])


if token:
    # Verifica il token
    decoded_token = verify_token(token)
    if decoded_token:
        st.success("Authorized access!")
        st.write("Token decoded:", decoded_token)
        st.session_state.prot = True
        with open("prot_status.json", "w") as file:
            json.dump({"prot": st.session_state.prot}, file)
            
        # Inserisci qui il codice dell'applicazione Streamlit
    else:
        st.error("Access denied: token invalid or expired.")
        st.session_state.prot = False
        with open("prot_status.json", "w") as file:
            json.dump({"prot": st.session_state.prot}, file)
        st.stop()
else:
    st.error("No token provided, access denied.")
    with open("prot_status.json", "w") as file:
            json.dump({"prot": st.session_state.prot}, file)
    st.stop()


 
st.markdown("---")
st.markdown("<h1 style='text-align: center;'>👷 Azioni sismiche secondo NTC2018</h1>", unsafe_allow_html=True)
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.page_link("https://enginapps.it", label="www.enginapps.it", icon="🏠")
#st.write("Application Start")

# Salva in un file temporaneo
st.session_state.prot = True
with open("prot_status.json", "w") as file:
    json.dump({"prot": st.session_state.prot}, file)

# Utilizza un link HTML per fare il redirect a "pages/main.py"
# Codice HTML e CSS per il pulsante con hover
button_html = """
    <style>
    .button-container {
        display: flex;
        justify-content: center; /* Centra il pulsante orizzontalmente */
        align-items: center; /* Centra il pulsante verticalmente, se necessario */
        height: 20vh; /* Imposta l'altezza del contenitore al 30% dell'altezza della vista */
    }
    .hover-button {
        padding: 10px 30px;
        font-size: 16px;
        cursor: pointer;
        color: #000000;
        background-color: #4CAF49; /* Colore iniziale del pulsante */
        border: none;
        border-radius: 5px;
        transition: background-color 0.3s ease, transform 0.3s ease; /* Transizioni per un effetto fluido */
    }

    /* Effetto hover */
    .hover-button:hover {
        background-color: #5CD458; /* Colore al passaggio del mouse */
        color: white; 
        transform: scale(1.05); /* Leggero ingrandimento */
    }
    </style>
    <div class="button-container">
    <a href="main" target="_self">
        <button class="hover-button">GoTo main page</button>
    </a>
"""

#st.session_state.update({'prot': True})
#st.rerun()

# Inserisci il bottone nella pagina
st.markdown(button_html, unsafe_allow_html=True)
 
print ('prot', st.session_state.prot)
