import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import os
from PIL import Image
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(page_title="AirBnb-Analysis", page_icon="chart_with_upwards_trend", layout="wide")

st.title("chart_with_upwards_trend   AirBnb-Analysis")
df = pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\cleandatacsvairbnb.csv", encoding="ISO-8859-1")
a=st.sidebar.header("Choose your filter: ")

# Create for countrylist
try:
     countrylist = st.sidebar.multiselect("Pick your country", df["country"].unique())
except:
     st.warning("There is No Valid Selection")
 
 # Filter the data based on neighbourhood_group, neighbourhood
filtered_df = df[df['country'].isin(countrylist)]


room_type_df = filtered_df.groupby(by=["room_type"], as_index=False)["price"].mean()

col1, col2 = st.columns(2)
with col1:
    st.subheader("room_type_ViewData")
    fig = px.bar(room_type_df, x="room_type", y="price", text=['${:,.2f}'.format(x) for x in room_type_df["price"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("countrywise ViewData")
    fig = px.pie(filtered_df, values="price", names="country", hole=0.4)
    fig.update_traces(text=filtered_df["country"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("room_type wise price"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="room_type.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("country wise price"):
        neighbourhood_group = filtered_df.groupby(by="country", as_index=False)["price"].sum()
        st.write(neighbourhood_group.style.background_gradient(cmap="Oranges"))
        csv = neighbourhood_group.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="neighbourhood_group.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

 # Create a scatter plot
data1 = px.scatter(filtered_df, x="country", y="price", color="room_type")
data1['layout'].update(title="Room_type in the country and price trend data using Scatter Plot.",
                        titlefont=dict(size=20), xaxis=dict(title="country", titlefont=dict(size=20)),
                        yaxis=dict(title="price", titlefont=dict(size=20)))
st.plotly_chart(data1, use_container_width=True)

with st.expander("Detailed Room Availability and Price View Data in the Neighbourhood"):
     st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

 # Download orginal DataSet
csv = df.to_csv(index=False).encode('utf-8')
st.download_button('Download Data', data=csv, file_name="Data.csv", mime="text/csv")

import plotly.figure_factory as ff

st.subheader(":point_right: Neighbourhood_group wise Room_type and Minimum stay nights")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["country", "market", "number_of_reviews", "room_type", "price", "minimum_nights", "name"]]
    fig = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig, use_container_width=True)

 # map function for room_type

# If your DataFrame has columns 'Latitude' and 'Longitude':
st.subheader("Airbnb Analysis in Map view")
map_data = filtered_df[['longitude', 'latitude']]

st.map(map_data)
