import streamlit as st
import pandas as pd
import numpy as np

df = pd.read_excel('./referentiel.xlsx')


def display_module_infos(parcours, semestre, module):
    data = df.query(
        'Parcours == @parcours and Semestre == @semestre and Module == @module')
    data = data.iloc[0]
    for col in data.index:
        st.subheader(col)
        st.write(data[col])


def set_stage():
    st.write('test')


def display_modules_main_panel(parcours):
    st.title(parcours)
    for semestre in data.Semestre.unique():
        st.subheader(semestre)
        parcours_semestre = data.query('Semestre == @semestre')
        for module in parcours_semestre.Module:
            label = ' '.join(module.split(':')[1:])
            st.button(
                label=label,
                key=semestre + label,
                on_click=display_module_infos,
                args=(parcours, semestre, module)
            )


for parcours in df.Parcours.unique():
    if st.sidebar.button(parcours, type="primary"):
        data = df.query('Parcours == @parcours')
        display_modules_main_panel(parcours)
