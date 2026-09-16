import streamlit as st
from modules import import_data, cleaning, descriptive, inferential, visualization, report

# --- Configuration ---
st.set_page_config(
    page_title="Analyse Statistique Pro",
    page_icon="📊",
    layout="wide",
)

# --- Barre latérale ---
st.sidebar.title("📊 Analyse Statistique Pro")
page = st.sidebar.radio(
    "Navigation",
    ["📥 Import", "🧹 Nettoyage", "📊 Descriptif", "🧪 Tests", "📈 Graphiques", "📄 Rapport"],
)

if "df" in st.session_state:
    st.sidebar.success(f"Données actives : {st.session_state['df'].shape[0]} lignes")
    if st.sidebar.button("♻️ Réinitialiser"):
        del st.session_state["df"]
        st.rerun()

# --- Routage ---
if page == "📥 Import":
    import_data.render()
elif page == "🧹 Nettoyage":
    cleaning.render()
elif page == "📊 Descriptif":
    descriptive.render()
elif page == "🧪 Tests":
    inferential.render()
elif page == "📈 Graphiques":
    visualization.render()
elif page == "📄 Rapport":
    report.render()
