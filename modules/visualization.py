import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def render():
    st.header("📈 Visualisations")
    st.divider()

    if "df" not in st.session_state:
        st.warning("⚠️ Importez d'abord des données dans l'onglet 📥 Import")
        return

    df = st.session_state["df"]
    colonnes_num = df.select_dtypes(include="number").columns.tolist()
    colonnes_cat = df.select_dtypes(include="object").columns.tolist()

    graphique = st.selectbox(
        "Type de graphique",
        ["Histogramme", "Boîte à moustaches (Boxplot)", "Nuage de points",
         "Barplot", "Camembert", "Matrice de corrélation"],
    )

    st.divider()

    if graphique == "Histogramme" and colonnes_num:
        var = st.selectbox("Variable", colonnes_num)
        nb_bins = st.slider("Nombre de classes", 5, 100, 30)
        fig = px.histogram(df, x=var, nbins=nb_bins, title=f"Histogramme de {var}")
        st.plotly_chart(fig, use_container_width=True)

    elif graphique == "Boîte à moustaches (Boxplot)" and colonnes_num:
        c1, c2 = st.columns(2)
        var = c1.selectbox("Variable", colonnes_num)
        groupe = c2.selectbox("Grouper par (optionnel)", ["Aucun"] + colonnes_cat)
        if groupe == "Aucun":
            fig = px.box(df, y=var, title=f"Boxplot de {var}")
        else:
            fig = px.box(df, x=groupe, y=var, title=f"Boxplot de {var} par {groupe}")
        st.plotly_chart(fig, use_container_width=True)

    elif graphique == "Nuage de points" and len(colonnes_num) >= 2:
        c1, c2 = st.columns(2)
        var_x = c1.selectbox("Axe X", colonnes_num)
        var_y = c2.selectbox("Axe Y", colonnes_num, index=min(1, len(colonnes_num)-1))
        couleur = st.selectbox("Couleur par (optionnel)", ["Aucun"] + colonnes_cat)
        if couleur == "Aucun":
            fig = px.scatter(df, x=var_x, y=var_y, title=f"{var_y} vs {var_x}")
        else:
            fig = px.scatter(df, x=var_x, y=var_y, color=couleur, title=f"{var_y} vs {var_x}")
        st.plotly_chart(fig, use_container_width=True)

    elif graphique == "Barplot" and colonnes_cat:
        c1, c2 = st.columns(2)
        var_cat = c1.selectbox("Variable qualitative", colonnes_cat)
        var_num = c2.selectbox("Variable à moyenner", colonnes_num) if colonnes_num else None
        if var_num:
            data = df.groupby(var_cat)[var_num].mean().reset_index()
            fig = px.bar(data, x=var_cat, y=var_num, title=f"Moyenne de {var_num} par {var_cat}")
        else:
            data = df[var_cat].value_counts().reset_index()
            data.columns = [var_cat, "Effectif"]
            fig = px.bar(data, x=var_cat, y="Effectif", title=f"Effectifs par {var_cat}")
        st.plotly_chart(fig, use_container_width=True)

    elif graphique == "Camembert" and colonnes_cat:
        var_cat = st.selectbox("Variable qualitative", colonnes_cat)
        data = df[var_cat].value_counts().reset_index()
        data.columns = [var_cat, "Effectif"]
        fig = px.pie(data, names=var_cat, values="Effectif", title=f"Répartition de {var_cat}")
        st.plotly_chart(fig, use_container_width=True)

    elif graphique == "Matrice de corrélation" and len(colonnes_num) >= 2:
        corr = df[colonnes_num].corr().round(2)
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r",
                        title="Matrice de corrélation")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Pas assez de colonnes adaptées pour ce graphique.")
