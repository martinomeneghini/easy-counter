import streamlit as st
import zipfile
import json

# CSS personalizzato
st.markdown("""
    <style>
    .stApp {
        background-color: #0a0a0a;
    }
    .stApp, .stMarkdown, p, label {
        color: #ffffff !important;
    }
    h1 {
        color: #ffffff !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    h2, h3 {
        color: #FF6B00 !important;
    }
    .stFileUploader {
        background-color: #1a1a1a !important;
        border: 2px dashed #FF6B00 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    .stSuccess {
        background-color: #1a1a1a !important;
        border-left: 4px solid #FF6B00 !important;
        color: #FF6B00 !important;
    }
    .stWarning {
        background-color: #1a1a1a !important;
        border-left: 4px solid #FF6B00 !important;
    }
    .stCheckbox label {
        color: #FF6B00 !important;
        font-weight: 600 !important;
    }
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

# Database utenti salvato in sessione
if "utenti" not in st.session_state:
    st.session_state.utenti = {
        "martino": {"password": "1234", "premium": False},
        "utente_premium": {"password": "1234", "premium": True},
    }
utenti = st.session_state.utenti

# Inizializza sessione
if "loggato" not in st.session_state:
    st.session_state.loggato = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Schermata di login e registrazione
if not st.session_state.loggato:
    st.markdown("<h1>Easy <span style='background-color:#FF6B00; color:#000000; padding:2px 14px; border-radius:8px;'>Counter</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaaaaa;'>Scopri chi non ti segue su Instagram</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_sinistra, col_destra = st.columns(2)

    with col_sinistra:
        st.markdown("<h3>Accedi</h3>", unsafe_allow_html=True)
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Accedi"):
            if username in utenti and utenti[username]["password"] == password:
                st.session_state.loggato = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Username o password errati")

    with col_destra:
        st.markdown("<h3>Registrati</h3>", unsafe_allow_html=True)
        nuovo_username = st.text_input("Scegli uno username", key="reg_user")
        nuova_password = st.text_input("Scegli una password", type="password", key="reg_pass")
        conferma_password = st.text_input("Conferma password", type="password", key="reg_conf")

        if st.button("Crea account"):
            if nuovo_username == "":
                st.error("❌ Inserisci uno username")
            elif nuovo_username in utenti:
                st.error("❌ Username già esistente")
            elif nuova_password != conferma_password:
                st.error("❌ Le password non coincidono")
            elif len(nuova_password) < 4:
                st.error("❌ La password deve avere almeno 4 caratteri")
            else:
                utenti[nuovo_username] = {"password": nuova_password, "premium": False}
                st.success("✅ Account creato! Ora accedi")

    st.stop()

# App principale — visibile solo se loggato
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
st.markdown("<p style='color:#aaaaaa; font-size:1.1rem;'>Scopri chi non ti segue su Instagram</p>", unsafe_allow_html=True)
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

        st.success("✅ Analisi completata!")
        col1, col2, col3 = st.columns(3)
        col1.metric("Followers", len(followers))
        col2.metric("Following", len(following))
        col3.metric("Non ti seguono", len(non_ti_seguono))

        st.markdown("---")

        # Controlla se utente è premium
        is_premium = utenti[st.session_state.username]["premium"]

        if is_premium:
            lista_da_mostrare = non_ti_seguono
        else:
            lista_da_mostrare = non_ti_seguono[0:2]

        st.markdown("<h3>Lista:</h3>", unsafe_allow_html=True)
        for persona in lista_da_mostrare:
            st.markdown(f"<div class='profilo-card'>@{persona}</div>", unsafe_allow_html=True)

        if not is_premium and len(non_ti_seguono) > 2:
            st.warning(f"🔒 E altri **{len(non_ti_seguono) - 2}** profili nascosti — passa al Premium per vedere tutti")