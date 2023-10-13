import pandas as pd
import streamlit as st

df = pd.read_csv("StudentsPerformance.csv")

df = df.replace({"test preparation course":{"none":False, "completed":True}})

st.data_editor(
    df,
    hide_index=True,
    column_config={
        "gender": "Gender",
        "race/ethnicity":"Ethnicity Group",
        "parental level of education":"Parental level of education",
        "launch":"Launch",
        "test preparation course":st.column_config.CheckboxColumn(
            "Test preparation course",
            help="Indication if the student completed the preparation course or not",
            
        ),
        "math score": st.column_config.ProgressColumn(
            "Math Score",
            help="The score in the math part",
            format="%f",
            min_value=0,
            max_value=100,
        ),
        "reading score": st.column_config.ProgressColumn(
            "Reading Score",
            help="The score in the reading part",
            format="%f",
            min_value=0,
            max_value=100,
        ),
        "writing score": st.column_config.ProgressColumn(
            "Writing Score",
            help="The score in the writing part",
            format="%f",
            min_value=0,
            max_value=100,
        ),
        
    },
    disabled=True,
)
