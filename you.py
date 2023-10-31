import streamlit as st
st.set_page_config(page_title="utubechannel")
st.header("*Youtube Channel Details*")
st.subheader("*_Find your favourite Utube details here_*")

#Connecting Mongodb

import pymongo as py
client=py.MongoClient("mongodb://localhost:27017/")
db1=client['otube_data']
mycol = db1["ychanneldetails"]
mycol2 = db1["Y-video"]
#Connecting MySQL

import mysql.connector
mydatabase = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "root",
            database = "mydatabase",
            auth_plugin="mysql_native_password",
            charset="utf8mb4"
        )
mycursor = mydatabase.cursor()

##Creating New Table

Newtable="""CREATE TABLE IF NOT EXISTS Youtube(
                    channel_id VARCHAR(255), 
                    channel_Name VARCHAR(255), 
                    channel_description text(1555),
                    channel_views text(11132768), 
                    channel_subscribers text(32768),
                    channel_videocount text(32768))
                """
mycursor.execute(Newtable)
Newtable2="""CREATE TABLE IF NOT EXISTS Youtubevideo(
                videoid VARCHAR(255),
                videotag VARCHAR(255),
                videotitle TEXT,
                videoreleasedate TEXT,
                channelid VARCHAR(255))
                CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """
mycursor.execute(Newtable2)
####Column Separation
col1,col2,col3= st.tabs(["Pre-Start","Select Here","Visualize"])
with col1:
    a= st.button('Refresh here!!!, Before Start')
    if a:
        mycol.delete_many({})
        mycol2.delete_many({})
        delete_query = f"DELETE FROM Youtube"
        delete_query2= f"DELETE FROM Youtubevideo"
        mycursor.execute(delete_query)
        mycursor.execute(delete_query2)
        mydatabase.commit()
        st.write("Cool!!!!!!!..... You can Start Exploring NOW:----)))))")

with col2:
    import pandas as pd
    from googleapiclient.discovery import build
    apikey="AIzaSyC7VQdUlkl1uvqB3sUV7tn2Mst-WLFRIBI"
    apiservicename="youtube"
    apiversion="v3"
    channel_ids=["UCzh5hQc_O3r3xjh9sXrM7-A", #blacksheep
             "UCiPmhfdCL06cSVTXKabF0Zg", #nakkalities
             "UCNwcxhfBVDgwx9Lv3CBpu6A", #lmes
             "UCduIoIMfD8tT3KoU0-zBRgQ", #guvi
             "UCbCmjCuTUZos6Inko4u57UQ", #cocomelon
             "UCj0t9VmB-FNrXuVJJCW7etw", #Shankar IAS Academy
             "UCvhU9qF1xtUsFXdKrcJxbFA", #Curious Freaks
             "UCnz-ZXXER4jOvuED5trXfEA", #techTFQ
             "UCOeq-7Q3OohvOp_L_8BUoxA", #infactcmd
             "UC1aBfiSLSjWhguorXtLxs6w" #behindwoodhits
]
    options=st.multiselect("select the Youtube channel:",channel_ids)
    youtube=build(apiservicename,apiversion,developerKey=apikey)
    def YT(youtube, channel_ids):
        alldata=[]
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=','.join(options)
         )
        response = request.execute()
        for i in range(len(response['items'])):
            data1=dict(channel_id =response['items'][i]['id'],channel_Name =response['items'][i]['snippet']['title'],channel_description =response['items'][i]['snippet']['description'],
              channel_views =response['items'][i]['statistics']['viewCount'], channel_subscribers =response['items'][i]['statistics']['subscriberCount'],
             channel_videocount =response['items'][i]['statistics']['videoCount'])
            alldata.append(data1)
        return alldata
    def YTVideo(youtube, options):
        videos=[]
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            id=','.join(options)
         )
        response = request.execute()
        for n in range(len(response['items'])):
                playlist_id =response['items'][n]['contentDetails']['relatedPlaylists']['uploads']
                next_page_token = None
                while True:
                        play_response= youtube.playlistItems().list(playlistId=playlist_id,
                                                       part="snippet",
                                                       pageToken=next_page_token,
                                                       maxResults = 50000).execute()
                        next_page_token=play_response.get('nextPageToken')
                        for item in play_response['items']:
                            data2 = dict(videoid=item['id'], videotag=item['etag'],videotitle=item['snippet']['title'], videodescription=item['snippet']['description'], videoreleasedate=item['snippet']['publishedAt'], 
                                         channelid =item['snippet']['channelId'])
                            videos.append(data2)
                        if next_page_token is None:
                                break
        return videos
    try:
        st.write('You selected:',YT(youtube, channel_ids))
    except KeyError:
        st.write("Oops!!!!! There was no valid selection")
    
    alldocument=mycol.find()
    alldocument2=mycol2.find()
    submit=st.button("Save at mongodb:")
    if submit:
        mycol.insert_many(YT(youtube, channel_ids))
        mycol2.insert_many(YTVideo(youtube, options))
        st.write("Hurry!!!!! Data moved to MongoDB")
    insert_table=st.button("Insert data to SQL Table:")
    if insert_table:
        insert_query="INSERT INTO Youtube(channel_id, channel_Name, channel_description, channel_views, channel_subscribers, channel_videocount) VALUES (%s, %s, %s, %s, %s, %s)"
        for b in alldocument:
            v1=b.get("channel_id",None)
            v2=b.get("channel_Name", None)
            v3=b.get("channel_description",None)
            v4=b.get("channel_views", None)
            v5=b.get("channel_subscribers", None)
            v6=b.get("channel_videocount", None)
            mycursor.execute(insert_query, (v1, v2, v3, v4, v5, v6))
            mydatabase.commit()
        insert_query2="INSERT INTO Youtubevideo(videoid, videotag, videotitle, videoreleasedate,channelid) VALUES (%s, %s, %s, %s, %s)"
        for b in alldocument2:
            u1=b.get("videoid", None)
            u2=b.get("videotag",None)
            u3=b.get("videotitle", None)
            u5=b.get("videoreleasedate", None)
            u6=b.get("channelid",None)
            mycursor.execute(insert_query2, (u1, u2, u3, u5, u6))
            mydatabase.commit()
        st.write(":-)))))  Data inserted into MySQL Table") 
    #Join
    Jointable=st.button("Join the selected table")    
    if Jointable: 
        Join = """
        SELECT Youtube.channel_id, Youtube.channel_Name, Youtube.channel_description, Youtube.channel_views, 
        Youtube.channel_subscribers, Youtube.channel_videocount, Youtubevideo.videoid, Youtubevideo.videoreleasedate, 
        Youtubevideo.videotitle, Youtubevideo.videotag
        FROM Youtube
        INNER JOIN Youtubevideo ON Youtube.channel_id = Youtubevideo.channelid
        """
        mycursor.execute(Join)
        results = mycursor.fetchall()
        mydatabase.commit()
        st.write("The tables has been Joined#####")
with col3:
   #Query
    Q1=st.button("VideoTitle and their Corresponding Youtube channel Name")
    if Q1:
        Query1 = "SELECT DISTINCT Youtubevideo.videotitle, Youtube.channel_Name FROM Youtube INNER JOIN Youtubevideo ON Youtube.channel_id = Youtubevideo.channelid"
        mycursor.execute(Query1)
        results1 = mycursor.fetchall()
        mydatabase.commit()
        st.write(pd.DataFrame(results1))
    Q2=st.button("Channel Contains Highest Number of Videos")
    if Q2:
        Query2 = "SELECT Youtube.channel_Name FROM Youtube INNER JOIN Youtubevideo ON Youtube.channel_id = Youtubevideo.channelid WHERE Youtubevideo.videoid = (SELECT DISTINCT MIN(Youtubevideo.videoid) FROM Youtube INNER JOIN Youtubevideo ON Youtube.channel_id = Youtubevideo.channelid)"
        mycursor.execute(Query2)
        results2 = mycursor.fetchall()
        mydatabase.commit()
        st.write(f"The channel with the highest number of videos is: {results2[0][0]}")
    Q3=st.button("Number of Videos released after 2022")
    if Q3:
        Query3 = "SELECT COUNT(DISTINCT(Youtubevideo.videoid)) FROM Youtube INNER JOIN Youtubevideo ON Youtube.channel_id = Youtubevideo.channelid WHERE Youtubevideo.videoreleasedate > '2022-01-01'"
        mycursor.execute(Query3)
        results3 = mycursor.fetchall()
        mydatabase.commit()
        st.write(f"Number of Videos released after 2022: {results3[0][0]}")