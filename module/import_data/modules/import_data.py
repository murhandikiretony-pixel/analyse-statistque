import streamlit as st
import pandas as pd
import numpy as np

def render():
    st.header("📥 Import des données")
    st.divider()

    source = st.radio("Source des données", ["Fichier local", "URL", "Données d'exemple"], horizontal=True)

    if source == "Fichier local":
        fichier = st.file_uploader("Choisissez un fichier", type=["csv", "xlsx", "xls"])
        if fichier is not None:
            try:
                if fichier.name.endswith((".xlsx", ".xls")):
                    df = pd.read_excel(fichier)
                else:
                    c1, c2 = st.columns(2)
                    sep = c1.selectbox("Séparateur", [",", ";", "\\t", "|"], key="sep")
                    sep = "\\t" if sep == "\\t" else sep
                    encodage = c2.selectbox("Encodage", ["utf-8", "latin-1", "iso-8859-1"], key="enc")
                    df = pd.read_csv(fichier, sep=sep, encoding=encodage)
                st.session_state["df"] = df
                st.success(f"✅ {df.shape[0]} lignes et {df.shape[1]} colonnes chargées !")
                st.dataframe(df.head(10))
            except Exception as e:
                st.error(f"❌ Erreur de lecture : {e}")

    elif source == "URL":
        url = st.text_input("URL du fichier CSV")
        if st.button("Charger") and url:
            try:
                df = pd.read_csv(url)
                st.session_state["df"] = df
                st.success(f"✅ {df.shape[0]} lignes et {df.shape[1]} colonnes chargées !")
                st.dataframe(df.head(10))
            except Exception as e:
                st.error(f"❌ Erreur : {e}")

    else:
        if st.button("Générer des données d'exemple"):
            np.random.seed(42)
            n = 200
            df = pd.DataFrame({
                "Age": np.random.randint(18, 70, n),
                "Salaire": np.random.normal(35000, 8000, n).round(0),
                "Experience": np.random.randint(0, 40, n),
                "Satisfaction": np.random.randint(1, 11, n),
                "Departement": np.random.choice(["Ventes", "IT", "RH", "Marketing"], n),
                "Ville": np.random.choice(["Paris", "Lyon", "Marseille", "Toulouse"], n),
            })
            st.session_state["df"] = df
            st.success("✅ Données d'exemple générées !")
            st.dataframe(df.head(10))
