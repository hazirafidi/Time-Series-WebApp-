import streamlit as st
from PIL import Image



st.set_page_config(
    page_title='Time Series Prediction‍', 
    page_icon='🏚️', 
    layout="wide", 
    initial_sidebar_state="expanded", 
    menu_items=None)

st.title("Time Series WebApp for Analysis and Prediction")

st.markdown(
    """ 
    Developed by [![Repo](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/hazirafidi)    
    """
)


st.markdown("---")

st.markdown(""

"Time series is a sequence of data points that occur in successive order over some period of time. In time series analysis, time is a significant variable of the data. Times series analysis helps us study our world and learn how we progress within it. This webapp is designed for time series analysis and prediction. All the training will be done using KNIME Analytics Platform and this WebApp is specifically design for the Model Deployment."

"")

image = Image.open('images\image.jpeg')

st.image(image, caption='Time Series Analysis')



