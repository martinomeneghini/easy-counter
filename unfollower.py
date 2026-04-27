import streamlit as st
import zipfile
import json

# CSS personalizzato
st.markdown("""
    <style>
    /* Sfondo nero */
    .stApp {
        background-color: #0a0a0a;
    }
    
    /* Testo bianco */
    .stApp, .stMarkdown, p, label {
        color: #ffffff !important;
    }
    
    /* Titolo arancione */
    h1 {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    
    /* Sottotitolo */
    h2, h3 {
        color: #FF6B00 !important;
    }
    
    /* Bottone upload */
    .stFileUploader {
        background-color: #1a1a1a !important;
        border: 2px dashed #FF6B00 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    /* Box successo */
    .stSuccess {
        background-color: #1a1a1a !important;
        border-left: 4px solid #FF6B00 !important;
        color: #FF6B00 !important;
    }
    
    /* Box warning */
    .stWarning {
        background-color: #1a1a1a !important;
        border-left: 4px solid #FF6B00 !important;
    }

    /* Checkbox */
    .stCheckbox label {
        color: #FF6B00 !important;
        font-weight: 600 !important;
    }

    /* Card per ogni profilo */
    .profilo-card {
        background-color: #1a1a1a;
        border-left: 3px solid #FF6B00;
        border-radius: 8px;
        padding: 10px 16px;
        margin: 6px 0;
        color: white;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Intestazione
st.markdown("""
    <h1>
        Easy 
        <span style='
            background-color: #FF6B00;
            color: #000000;
            padding: 2px 14px;
            border-radius: 8px;
        '>Counter</span>
    </h1>
""", unsafe_allow_html=True)
st.markdown("<p style='color:#aaaaaa; font-size:1.1rem;'>Scopri chi non ti segue  su Instagram</p>", unsafe_allow_html=True)
st.markdown("---")

file_caricato = st.file_uploader("📂 Carica il tuo file ZIP di Instagram", type="zip")

if file_caricato:
    with zipfile.ZipFile(file_caricato) as z:

        with z.open("connections/followers_and_following/followers_1.json") as f:
            dati_followers = json.load(f)

        with z.open("connections/followers_and_following/following.json") as f:
            dati_following = json.load(f)

        followers = []
        for persona in dati_followers:
            username = persona["string_list_data"][0]["value"]
            followers.append(username)

        following = []
        for persona in dati_following["relationships_following"]:
            username = persona["title"]
            following.append(username)

        non_ti_seguono = []
        for persona in following:
            if persona not in followers:
                non_ti_seguono.append(persona)

        # Statistiche
        st.success("✅ Analisi completata!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", len(followers))
        col2.metric("Following", len(following))
        col3.metric("Non ti seguono ", len(non_ti_seguono))

        st.markdown("---")

        # Freemium
        premium = st.checkbox("🔓 Modalità Premium — sblocca tutti i risultati")

        if premium:
            lista_da_mostrare = non_ti_seguono
        else:
            lista_da_mostrare = non_ti_seguono[0:2]

        st.markdown("<h3>Lista:</h3>", unsafe_allow_html=True)
        for persona in lista_da_mostrare:
            st.markdown(f"<div class='profilo-card'>@{persona}</div>", unsafe_allow_html=True)

        if not premium and len(non_ti_seguono) > 2:
            st.warning(f"🔒 E altri **{len(non_ti_seguono) - 2}** profili nascosti — attiva il Premium per vedere tutti")
