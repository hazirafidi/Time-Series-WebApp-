import streamlit as st
import os
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
# from st_aggrid.shared import DataReturnMode
# import pickle
# import numpy as np
import time

from helper import *


st.set_page_config(page_title='Predictions', page_icon="chart_with_downwards_trend", layout="wide", initial_sidebar_state="expanded", menu_items=None)

st.header("Predict your time series data by Machine Learning Approach.")

st.markdown("---")

st.subheader("Your Dataset")

file_upload = st.file_uploader(
                                "Upload your dataset", 
                                type=['csv'], 
                                help="IMPORTANT:Please ensure your target at the first column"
                                )

@st.cache(allow_output_mutation=True, persist=True)
def data_upload():
    if file_upload is not None:
        df_input = pd.read_csv(file_upload)
        return df_input

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


if ['df_input'] not in st.session_state:
    st.session_state['df_input'] = pd.DataFrame(data_upload())


with st.expander("Collapse to view", expanded=True):
    with st.form('dataset') as f:
        st.subheader('Your dataset')
        gd = GridOptionsBuilder.from_dataframe(st.session_state['df_input'])
        gd.configure_default_column(editable=True,groupable=True)
        # gd.configure_columns(column_names='date')
        gd.configure_pagination(enabled=True)
        gridoptions = gd.build()
        editable_df = AgGrid(st.session_state['df_input'], editable=True, gridOptions=gridoptions,
                            fit_columns_on_grid_load=True, 
                            update_mode=GridUpdateMode.GRID_CHANGED,
                            theme='fresh',
                            )
        if st.form_submit_button():
            st.session_state['df_input'] = editable_df['data']
            st.info("Successfully added! Displaying first 5 rows")
            st.write(editable_df['data'].head())
        else:
            st.write("Double-click interactive table to edit value. Click 'submit' button if you're satisfied with the data input")

    csv = convert_df(pd.DataFrame(editable_df['data']))
        
    st.download_button(
        label="Download CSV file",
        data=csv,
        file_name='file.csv',
        mime='text/csv'
        )

st.markdown('---')

st.header('Upload your trained model for prediction')

# uploaded_model = st.file_uploader('Upload your trained model here.', type=['h5', 'sav'])

if ['uploaded_model'] not in st.session_state:
    st.session_state['uploaded_model'] = st.file_uploader('Upload your trained model here.', type=['h5', 'sav'])

uploaded_model = st.session_state['uploaded_model']

if uploaded_model is not None:
    file_details = {'FileName': uploaded_model.name, 'FileType': uploaded_model.type}
    st.write(file_details)
    with open(os.path.join("tempDir", uploaded_model.name), "wb") as f:
        f.write(uploaded_model.getbuffer())
    st.success("Successfully Saved File: {} to tempDir".format(uploaded_model.name))



if 'output' not in st.session_state:
    st.session_state['output'] = []

if st.button("Predict"):
    if uploaded_model is not None:
        with st.spinner("Predicting....Wait for it..."):
            time.sleep(5)
            output = ml_prediction()
            st.success("Successfully predicted!")
            with st.expander("Collapse to view. Data display for first 5 rows"):
                output = st.session_state['output'] = pd.DataFrame(output)
                st.write(st.session_state['output'].head())
                csv = convert_df(output)
        
                st.download_button(
                    label="Download CSV file",
                    data=csv,
                    file_name='file.csv',
                    mime='text/csv'
                    )