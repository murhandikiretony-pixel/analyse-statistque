import streamlit as st
import pandas as pd

def render():
    st.header("📄 Rapport")
    st.divider()

    if "df" not in st.session_state:
        st.warning("⚠️ Importez d'abord des données dans l'onglet 📥 Import")
        return

    df = st.session_state["df"]

    st.subheader("🧾 Synthèse de vos données")

    n_lignes, n_colonnes = df.shape
    n_manquantes = int(df.isna().sum().sum())
    n_doublons = int(df.duplicated().sum())
    n_num = len(df.select_dtypes(include="number").columns)
    n_cat = len(df.select_dtypes(include="object").columns)

    c1, c2, c3 = st.columns(3)
    c1.metric("Lignes", n_lignes)
    c2.metric("Colonnes", n_colonnes)
    c3.metric("Valeurs manquantes", n_manquantes)
    c1, c2, c3 = st.columns(3)
    c1.metric("Doublons", n_doublons)
    c2.metric("Colonnes numériques", n_num)
    c3.metric("Colonnes qualitatives", n_cat)

    st.divider()

    st.subheader("📋 Résumé statistique complet")
    st.dataframe(df.describe().round(2))

    st.divider()

    st.subheader("💾 Téléchargements")
    c1, c2, c3 = st.columns(3)

    csv = df.to_csv(index=False).encode("utf-8")
    c1.download_button("📥 Données (CSV)", csv, "donnees.csv", "text/csv")

    resume = df.describe().round(2).to_csv().encode("utf-8")
    c2.download_button("📊 Statistiques (CSV)", resume, "statistiques.csv", "text/csv")

    # Rapport TXT complet
    lignes = []
    lignes.append("=" * 50)
    lignes.append("RAPPORT D'ANALYSE STATISTIQUE")
    lignes.append("=" * 50)
    lignes.append(f"\nDimensions : {n_lignes} lignes x {n_colonnes} colonnes")
    lignes.append(f"Valeurs manquantes : {n_manquantes}")
    lignes.append(f"Doublons : {n_doublons}")
    lignes.append(f"Colonnes numériques : {n_num} | Colonnes qualitatives : {n_cat}")
    lignes.append("\n--- RÉSUMÉ STATISTIQUE ---")
    lignes.append(df.describe().round(2).to_string())
    lignes.append("\n--- COLONNES ---")
    for col in df.columns:
        lignes.append(f"  • {col} ({df[col].dtype})")
    rapport = "\n".join(lignes).encode("utf-8")
    c3.download_button("📄 Rapport (TXT)", rapport, "rapport_analyse.txt", "text/plain")

    st.divider()

    # Export Excel
    st.subheader("📗 Export Excel complet")
    buffer = __import__("io").BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Données", index=False)
        df.describe().round(2).to_excel(writer, sheet_name="Statistiques")
    st.download_button("📥 Télécharger tout (Excel)", buffer.getvalue(), "analyse_complete.xlsx",
                       "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
