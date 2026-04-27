import streamlit as st
import zipfile
import json

st.title("Easy Counter")
st.subheader("Scopri chi non ti segue back su Instagram")

file_caricato = st.file_uploader("Carica il tuo file ZIP di Instagram", type="zip")

if file_caricato:
    with zipfile.ZipFile(file_caricato) as z:
        
        # Leggi followers
        with z.open("connections/followers_and_following/followers_1.json") as f:
            dati_followers = json.load(f)
        
        # Leggi following
        with z.open("connections/followers_and_following/following.json") as f:
            dati_following = json.load(f)

        # Estrai lista username followers
        followers = []
        for persona in dati_followers:
            username = persona["string_list_data"][0]["value"]
            followers.append(username)

        # Estrai lista username following
        following = []
        for persona in dati_following["relationships_following"]:
            username = persona["title"]
            following.append(username)

        # Trova chi non ti segue back
        non_ti_seguono = []
        for persona in following:
            if persona not in followers:
                non_ti_seguono.append(persona)

        # Mostra risultati
        st.success("Analisi completata!")
        st.write(f"Followers: {len(followers)}")
        st.write(f"Following: {len(following)}")
        st.write(f"Chi non ti segue back: {len(non_ti_seguono)}")

        # Meccanismo freemium
        premium = st.checkbox("Modalità Premium (sblocca tutti i risultati)")

        if premium:
            lista_da_mostrare = non_ti_seguono
        else:
            lista_da_mostrare = non_ti_seguono[0:2]

        st.subheader("Lista:")
        for persona in lista_da_mostrare:
            st.write(f"@{persona}")

        if not premium and len(non_ti_seguono) > 2:
            st.warning(f"E altri {len(non_ti_seguono) - 2} profili nascosti — sblocca per vedere tutti")
