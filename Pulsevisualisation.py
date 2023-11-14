import pandas as pd 
import csv
import plotly.express as px
import streamlit as st 
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import geopandas as gpd
import matplotlib.pyplot as plt
import mysql.connector
mydatabase = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "mydatabase1",
            auth_plugin="mysql_native_password",
            charset="utf8mb4"
        )
mycursor = mydatabase.cursor()

##Creating New Table

Newtable="""CREATE TABLE IF NOT EXISTS agg_trans(
                    state VARCHAR(255), 
                    Year VARCHAR(255), 
                    Quarter VARCHAR(255),
                    Transactiontype VARCHAR(255), 
                    Transactioncount VARCHAR(255),
                    Transactionamount VARCHAR(255))
                """
mycursor.execute(Newtable)

st. set_page_config(layout="wide")
Data_Aggregated_Transaction=r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\Aggregatedstatetransaction1.csv"
Geo_Dataset=r"C:\Users\DELL\Documents\GitHub\PhonePe-Pulse-Data-2018-2022-Analysis\data\Longitude_Latitude_State_Table.csv"
mapstatetrans=r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\mapstatetransaction.csv"
df=pd.read_csv(Data_Aggregated_Transaction)
df1=pd.read_csv(Geo_Dataset)
df2=pd.read_csv(mapstatetrans)
colT1,colT2 = st.columns([2,8])
with colT2:
    st.title(':Violet[PhonePe Pulse Data Analysis:]')

c1,c2,c3=st.columns(3)
with c1:
    a= st.button('Refresh here!!!, Before Start')
    if a:
        delete_query = f"DELETE FROM agg_trans"
        mycursor.execute(delete_query)
        mydatabase.commit() 
        st.write("Cool!!!!!!!..... You can Start Phonepe Visualisation NOW:----)))))")
with c2:
    Year = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022','2023'))
with c3:
    Quarter = st.selectbox(
            'Please select the Quarter',
            ('1', '2', '3','4'))
year=int(Year)
quarter=int(Quarter)
Showpie = st.button("Show Pie Chart:")

if Showpie:
    with open(Data_Aggregated_Transaction, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            row = [str(row[0]), int(row[1]), int(row[2]), row[3], int(row[4]), float(row[5])]
            query = f"INSERT INTO agg_trans VALUES ({', '.join(['%s']*len(row))})"
            mycursor.execute(query, row)
            mydatabase.commit() 
    mycursor.execute(f"SELECT state, sum(Transactioncount) as Total_Transactions_Count, sum(Transactionamount) as Total FROM agg_trans WHERE year = {year} AND quarter = {quarter} GROUP BY state ORDER BY Total DESC LIMIT 10")
    
    # Fetch results
    results_pie = mycursor.fetchall()

    # Check if there are results for the pie chart
    if not results_pie:
        st.warning("No data available for the selected Year and Quarter.")
    else:
        filtered_data_pie = pd.DataFrame(results_pie, columns=['state', 'Transactioncount', 'Transactionamount'])

        fig_pie = px.pie(filtered_data_pie, values='Transactionamount',
                         names='state',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Transactioncount'],
                         labels={'Transactions_Count': 'Transactioncount'})
        st.plotly_chart(fig_pie, use_container_width=True)

        # Fetch results for the choropleth map
        mycursor.execute(f"SELECT state, sum(Transactioncount) as Total_Transactions_Count, sum(Transactionamount) as Total FROM agg_trans WHERE year = {Year} AND quarter = {Quarter} GROUP BY state ORDER BY Total DESC LIMIT 10")
        results_choropleth = mycursor.fetchall()

        # Check if there are results for the choropleth map
        if not results_choropleth:
            st.warning("No data available for the selected Year and Quarter.")
        else:
            filtered_data_choropleth = pd.DataFrame(results_choropleth, columns=['state', 'Transactioncount', 'Transactionamount'])

            # Load GeoJSON file
            mapdf = gpd.read_file("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson")

            # Join GeoJSON with the DataFrame
            merged_data = mapdf.set_index('ST_NM').join(filtered_data_choropleth.set_index('state'))

            fig_choropleth = px.choropleth(
                merged_data.reset_index(),
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='ST_NM',
                color='Transactionamount',
                color_continuous_scale='viridis',
                title='Choropleth Map - State Transaction Data',
                labels={'Transactionamount': 'Total Transaction Amount'}
            )

            # Display Choropleth Map in Streamlit
            st.plotly_chart(fig_choropleth, use_container_width=True)