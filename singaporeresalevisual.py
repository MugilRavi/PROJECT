import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import LabelBinarizer
import streamlit as st
from sklearn.preprocessing import LabelEncoder
st.set_page_config(layout="wide")

st.write("""
<div style='text-align:center'>
    <h1 style='color:Blue;'>Singapore Flats Resale Price Prediction</h1>
</div>
""", unsafe_allow_html=True)
df=pd.read_csv(r'C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\New folder\singaporeresaleflat.csv')


x=df.iloc[:,[0,1,2,3,5,6,7,9,10]].values
y=df.iloc[:,[8]].values

label_encoder = LabelEncoder()

df['block'] = label_encoder.fit_transform(df['block'])
df['month'] = label_encoder.fit_transform(df['month'])
df['region'] = label_encoder.fit_transform(df['region'])
df['flat_model'] = label_encoder.fit_transform(df['flat_model'])

x1=df[['block','month','region','flat_model','floor_area_sqm','flat_type','lease_commence_date','storey_average','remaining_lease_months']]
y1=df['resale_price']
st.subheader("PREDICT RESALE PRICE")
# Define the possible values for the dropdown menus
month_options = df['month'].unique()
region_options = df['region'].unique()
flat_options = df['flat_type'].unique()
block_options =df['block'].unique()

# Define the widgets for user input
with st.form("my_form"):
    col1, col2, col3 = st.columns([5, 2, 5])
with col1:
            st.write(' ')
            block1 = st.selectbox("Block", block_options, key=1)
            MOnth = st.selectbox("Month", month_options, key=2)
            region = st.selectbox("region", region_options, key=3)
            flattype1 = st.selectbox("Flattype", sorted(flat_options), key=4)
with col3:
            floorarea = st.slider("Enter floor area",min_value=df['floor_area_sqm'].min() , max_value=df['floor_area_sqm'].max())
            Flatmodel1 = st.selectbox("Enter flatmodel",df['flat_model'].unique())
            leasecommencedate = st.selectbox("Enter leasecommencedate",df['lease_commence_date'].unique())
            storey = st.slider("Enter storey",min_value=df['storey_average'].min(), max_value=df['storey_average'].max())
            pendingleasemonth = st.slider("lease months remaining" ,min_value=df['remaining_lease_months'].min(),max_value=df['remaining_lease_months'].max())
            submit_button = st.form_submit_button(label="PREDICT Resale Price")
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
                x_train, x_test, y_train, y_test = train_test_split(x1,y1,test_size=0.1,random_state=0)
                inputx_test=[block1,MOnth,region,Flatmodel1,floorarea,flattype1,leasecommencedate,storey,pendingleasemonth]
                from sklearn.ensemble import GradientBoostingRegressor
                Regressor=GradientBoostingRegressor(n_estimators=7, random_state=0)
                Regressor.fit(x_train,y_train)
                input_df = pd.DataFrame(data=[inputx_test], columns=['block','month', 'region', 'flat_model','floor_area_sqm','flat_type', 'lease_commence_date', 
                                                                     'storey_average', 'remaining_lease_months'])
                y_pred = Regressor.predict(input_df)
                roundedPred=round(y_pred[0],0)
                st.markdown(f"<h2 style='color:Red;'>Predicted Resale Price: {roundedPred}</h2>", unsafe_allow_html=True)