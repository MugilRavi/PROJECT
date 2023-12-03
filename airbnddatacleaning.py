import pandas as pd
df = pd.read_csv(r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\csvairbnb.csv", encoding="ISO-8859-1")
df.drop(['listing_url','summary','description','first_review','last_review','host_id','host_url',
       'host_name', 'host_about', 'host_location', 'host_response_time','notes',
       'host_verifications','is_location_exact','amenities','space', 'neighborhood_overview', 'transit', 'access','interaction','house_rules' ],axis=1,inplace=True)
df.dropna(subset=['name'],inplace=True)
bhk=df['bedrooms'].median()
df['bedrooms'].fillna(bhk, inplace=True)
bed=df['beds'].median()
df['beds'].fillna(bed, inplace=True)
bath=df['bathrooms'].median()
df['bathrooms'].fillna(bath, inplace=True)
deposit=df['security_deposit'].mean()
df['security_deposit'].fillna(deposit, inplace=True)
clean=df['cleaning_fee'].mean()
df['cleaning_fee'].fillna(clean, inplace=True)
df.to_csv(r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\cleandatacsvairbnb.csv")

