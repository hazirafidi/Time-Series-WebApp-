
import pandas as pd
import numpy as np
import streamlit as st
import os
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import pickle
# from bokeh.plotting import figure, show
# import plotly.express as px
# import plotly.graph_objects as go
# import altair as alt


### FUNCTION TO UPLOAD MODEL ###

def dl_model_upload():
    model = keras.models.load_model(os.path.join("tempDir", st.session_state['uploaded_model'].name))
    return model


def ml_model_upload():
    model = pickle.load(os.path.join("tempDir", st.session_state['uploaded_model'].name))
    return model


### FUNCTION TO TRANSFORM AND PREDICT USING DEEP LEARNING MODEL ###

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


def dl_prediction():
    df = st.session_state['df_input']
    values = df.values
    # normalize
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled = scaler.fit_transform(values)
    # specify the number of lag hours
    n_hours = int(st.session_state['hours'])
    n_features = int(st.session_state['features'])
    # frame as supervised learning
    reframed = series_to_supervised(scaled, n_hours, 1)
    # drop column not use for prediction
    reframed.drop(reframed.iloc[:, -n_features:], axis=1, inplace=True)
    # split into input and outputs
    values = reframed.values
    n_obs = n_hours * n_features
    test_X, test_y = values[:, :n_obs], values[:, -n_features]
    # reshape input to be 3D [samples, timesteps, features]
    test_X = test_X.reshape((test_X.shape[0], n_hours, n_features))
    # load model
    input_model = dl_model_upload()
    # make prediction
    pred = input_model.predict(test_X)
    test_X = test_X.reshape((test_X.shape[0], n_hours*n_features))
    #invert scaling forecast
    inv_pred = np.concatenate((pred, test_X[:, -n_features+1:]), axis=1)
    inv_pred = scaler.inverse_transform(inv_pred)
    inv_pred = inv_pred[:,0]
    #invert scaling actual
    test_y = test_y.reshape((len(test_y), 1))
    inv_actual = np.concatenate((test_y, test_X[:, -n_features+1:]), axis=1)
    inv_actual = scaler.inverse_transform(inv_actual)
    inv_actual = inv_actual[:,0]
    data = {
        'Predicted': inv_pred,
        'Actual': inv_actual
    }
    return data

### FUNCTION TO TRANSFORM AND PREDICT USING DEEP LEARNING MODEL ###

def ml_prediction():
    df = st.session_state['df_input']
    values = df.values
    return st.write(values)


    # #normalize
    # scaler = MinMaxScaler(feature_range=(0,1))
    # scaled = scaler.fit_transform(values)
    # input_model = ml_model_upload()
    # pred = input_model.predict(X_test)





# def plot_chart_1():
#     fig = px.line(
#         pd.DataFrame(st.session_state['output']),
#         x = 'Time Index',
#         y = 'Actual/Predicted Target Values',
#         title = 'Time Series Graph'
#         )
#     fig.update_xaxes(rangeslider_visible=True)
#     fig.update_layout(height=600, width=900)
#     return fig.show()






# 

    # source = pd.DataFrame(st.session_state['output'])
    # chart = alt.Chart(source).mark_line().encode(
    #             x = 'Time Index',
    #             y = 'Actual-Predicted Value',
    #             color = 'symbol',
    #             strokeDash = 'symbol',
    #             )
    # return chart