
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import streamlit as st
import os
import time
from tensorflow import keras
from bokeh.plotting import figure


from helper import *


st.set_page_config(
    page_title='Predictions', 
    page_icon="chart_with_downwards_trend", 
    layout="wide", 
    initial_sidebar_state="expanded", 
    menu_items=None
    )


st.header("▶️""Predict your time series data by Deep Learning Approach.")

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

st.subheader('Upload your trained model for prediction')

st.markdown("Please enter number of samples and number of timesteps and features trained in your model")


col1, col2 = st.columns(2)

with col1:  
    if ['hours'] not in st.session_state:
        st.session_state['hours'] = st.number_input("Number of timestep", min_value=1, help="timestep trained in your model")

with col2:
    if ['features'] not in st.session_state:
        st.session_state['features'] = st.number_input("Number of features", min_value=1, help="Features trained in your model")


if ['uploaded_model'] not in st.session_state:
    st.session_state['uploaded_model'] = st.file_uploader('Upload your trained model here.', type=['h5', 'sav'])

uploaded_model = st.session_state['uploaded_model']

if uploaded_model is not None:
    file_details = {'FileName': uploaded_model.name, 'FileType': uploaded_model.type}
    st.write(file_details)
    with open(os.path.join("tempDir", uploaded_model.name), "wb") as f:
        f.write(uploaded_model.getbuffer())
    st.success("Successfully Saved File: {} to tempDir".format(uploaded_model.name))

st.markdown('---')

if 'output' not in st.session_state:
    st.session_state['output'] = []

if st.button("Predict"):
    if uploaded_model is not None:
        with st.spinner("Predicting....Wait for it..."):
            time.sleep(5)
            output = dl_prediction()
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
                
            st.subheader("Time Series Graph")
            
            x = output.index.values
            y1 = output['Actual'].values
            y2 = output['Predicted'].values

            p = figure(
            title='Time Series Graph',
            x_axis_label='Time Index',
            y_axis_label='Actual-Predicted Value',
            )

            p.line(x, y1, legend_label='Actual', line_width=2, color='red')
            p.line(x, y2, legend_label='Predicted', line_width=2, color='blue')

            p.legend.location = "top_left"
            p.legend.click_policy="mute"

            st.bokeh_chart(p, use_container_width=True)

    else:
        try:
            output = dl_prediction()
        except ValueError:
            st.error("Invalid Input!!")
    
    if uploaded_model is None:
        st.error("Can't Predict. Upload your model first!")
    
else:
    st.info("Waiting for user input. Click 'Predict' button to predict")


