# Time Series WebApp

This webapp is developed to deploy trained ML and DL model for Time Series Data. The Model is trained using KNIME Analytics Platform and the model is saved for deployment here.

# 1. Project Summary

This webapp is developed to deploy trained ML and DL model for Time Series Data. The Model is trained using KNIME Analytics Platform and the model is saved for deployment here.

# 2. IDE and Framework

This Webapp is built using Python Programming Language as the main IDE. The main framework use including Keras, Scikit-Learn, Streamlit, pandas and numpy.

# 3. Methodolgy

The Methodolgy for ML and DL Model Training using KNIME Analytic Platforms

# 3.1 Input Pipeline

The dataset is in the format of csv file and contains information of the Features and Target.


## 3.2 Univariate and Mutivariate Time Series (Deep Learning)

1. Data loading and preprocessing. Data preprocerssing involve data cleaning i.e filter out unnecessary columns, fill in null values, convert categorical data to numerical data, normalize the data, data splitting (train, validation and test data) and transform the data for to 3-D array as the keras input vector.

2. Construct the Model Architecture (LSTM Model)

3. Model Training and prediction with test data

4. Model Evaluation using Metric Measure 

## 3.3 Univariate and Mutivariate Time Series (Machine Learning)

1. Data loading and preprocessing. Data preprocerssing involve data cleaning i.e filter out unnecessary columns, fill in null values, convert categorical data to numerical data, normalize the data, data splitting (train and test data).

3. Model Training and prediction with test data (using Gradient Boosting and Linear Regression Model)

4. Model Evaluation using Metric Measure

# Demo

git clone this repo

Then, run yaml file to create and install dependencies

conda env create -f <name_of_your_env>.yml

Then, activate created environment using 

conda activate <name_of_your_env>

and run following command to install kerasa-gpu dependencies

conda install -c anaconda keras-gpu

https://user-images.githubusercontent.com/100177902/187399449-49223eee-971d-453d-85d2-1bc6f38c69eb.mp4



