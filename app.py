import streamlit as st
import pandas as pd
import numpy as np
import random
from streamlit_gsheets import GSheetsConnection

st.set_page_config(initial_sidebar_state="expanded")


@st.cache_data
def load_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(
        ttl="60min"
    )
    return df


df = load_data()


def display_module_infos(parcours, semestre, module):
    data = df.query(
        'Parcours == @parcours and Semestre == @semestre and Module == @module')
    data = data.iloc[0]

    title = ''.join(data.Module)
    st.title(title)
    st.header(' - '.join([data.Semestre, data.Parcours]))
    cols = ['Competence Ciblee', 'Descriptif',
            'Apprentissages Critiques', 'Mots Cles', 'Objectifs pédagogiques (prédiction IA)']

    for col in cols:
        st.subheader(f':blue[{col}]')
        if col == 'Objectifs pédagogiques (prédiction IA)':
            st.warning('''Experimental : Do not trust !''', icon="⚠️")
        st.write(data[col])


def display_modules_main_panel(parcours):
    st.title(parcours)
    for semestre in data.Semestre.unique():
        with st.expander(semestre):
            parcours_semestre = data.query('Semestre == @semestre')
            for module in parcours_semestre.Module:
                st.button(
                    label=module,
                    key=str(random.randrange(10**6)),
                    on_click=display_module_infos,
                    args=(parcours, semestre, module)
                )


st.sidebar.title('Parcours')
for parcours in df.Parcours.unique():
    if st.sidebar.button(parcours, type="primary"):
        data = df.query('Parcours == @parcours')
        display_modules_main_panel(parcours)


if st.sidebar.button('synchroniser', type="secondary"):
    st.cache_data.clear()
