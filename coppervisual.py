import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelBinarizer
import streamlit as st
from sklearn.preprocessing import LabelEncoder


import re

st.set_page_config(layout="wide")

st.write("""
<div style='text-align:center'>
    <h1 style='color:Red;'>Industrial Copper Modeling Application</h1>
</div>
""", unsafe_allow_html=True)
df=pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\cleancopperdata.csv")
x=df.iloc[:,[4,5,8,9,10,12]].values
y=df.iloc[:,[6]].values
x1=df.iloc[:,[4,5,8,9,10]].values
y1=df.iloc[:,[12]].values

tab1, tab2 = st.tabs(["PREDICT STATUS", "PREDICT SELLING PRICE"])
with tab1:
    # Define the possible values for the dropdown menus
    status_options = ['Won', 'Lost']
    item_type_options = df['item type'].unique()
    country_options = df['country'].unique()
    application_options =df['application'].unique()

    # Define the widgets for user input
    with st.form("my_form"):
        col1, col2, col3 = st.columns([5, 2, 5])
        with col1:
            st.write(' ')
            selling_price = st.slider("Enter Selling Price",min_value=df['selling_price'].min() , max_value=df["selling_price"].max())
            item_type = st.selectbox("Item Type", item_type_options, key=2)
            country = st.selectbox("Country", sorted(country_options), key=3)
            application = st.selectbox("Application", sorted(application_options), key=4)
        with col3:
            st.write(
                f'<h5 style="color:blue;">NOTE: Min & Max given for reference, you can enter any value</h5>',
                unsafe_allow_html=True)
            quantity_tons = st.slider("Enter Quantity Tons",min_value=611728 , max_value=1722207579)
            thickness = st.slider("Enter thickness",min_value=1,max_value=400)
            width = st.slider("Enter width",min_value=1, max_value=2990)
            customer = st.slider("customer ID" ,min_value=12458,max_value=30408185)
            submit_button = st.form_submit_button(label="PREDICT STATUS")
            st.markdown("""
                    <style>
                    div.st.Button > button:first-child {
                        background-color: #004aad;
                        color: white;
                        width: 100%;
                    }
                    </style>
                """, unsafe_allow_html=True)
            if submit_button:
                from sklearn.model_selection import train_test_split
                x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.1,random_state=0)
                inputx_test=[customer,country,application,thickness,width,selling_price]
                from sklearn.ensemble import GradientBoostingClassifier
                classifier=GradientBoostingClassifier(n_estimators=7, random_state=0)
                classifier.fit(x_train,y_train)
                input_df = pd.DataFrame(data=[inputx_test], columns=['customer', 'country', 'application', 'thickness', 'width', 'selling_price'])
                y_pred = classifier.predict(input_df)
                st.write("Predicted Status:", y_pred)
with tab2:
    # Define the possible values for the dropdown menus
    status_options = ['Won', 'Lost']
    item_type_options = df['item type'].unique()
    country_options = df['country'].unique()
    application_options =df['application'].unique()

    # Define the widgets for user input
    with st.form("my_form1"):
        col1, col2, col3 = st.columns([5, 2, 5])
        with col1:
            st.write(' ')
            Status = st.selectbox("Select Status",sorted(status_options),key=1)
            item_type = st.selectbox("Item Type", item_type_options, key=5)
            country = st.selectbox("Country", sorted(country_options), key=6)
            application = st.selectbox("Application", sorted(application_options), key=7)
        with col3:
            st.write(
                f'<h5 style="color:blue;">NOTE: Min & Max given for reference, you can enter any value</h5>',
                unsafe_allow_html=True)
            quantity_tons = st.slider("Enter Quantity Tons",min_value=611728 , max_value=1722207579)
            thickness = st.slider("Enter thickness",min_value=1,max_value=400)
            width = st.slider("Enter width",min_value=1, max_value=2990)
            customer = st.slider("customer ID" ,min_value=12458,max_value=30408185)
            submit_button = st.form_submit_button(label="PREDICT SELLING PRICE")
            st.markdown("""
                    <style>
                    div.st.Button > button:first-child {
                        background-color: #004aad;
                        color: white;
                        width: 100%;
                    }
                    </style>
                """, unsafe_allow_html=True)
            if submit_button:
                from sklearn.model_selection import train_test_split
                from sklearn.ensemble import GradientBoostingRegressor
                x_train, x_test, y_train, y_test = train_test_split(x1,y1,test_size=0.1,random_state=0)
                inputx_test=[customer,country,application,thickness,width]
                regressor = GradientBoostingRegressor(n_estimators=100, random_state=0)
                regressor.fit(x_train, y_train.ravel())
                input_df = pd.DataFrame(data=[inputx_test], columns=['customer', 'country', 'application', 'thickness', 'width'])
                y_pred = regressor.predict(input_df)
                rounded_pred = round(y_pred[0], 0)
                st.write("Predicted Selling Price:", rounded_pred)
