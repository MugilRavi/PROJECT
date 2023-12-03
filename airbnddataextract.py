import csv
import pymongo as py

# Connect to MongoDB
client = py.MongoClient("mongodb+srv://mugilpubic:12345Mugil@cluster0.cb2ccau.mongodb.net/?retrywrites=true&w=majority")
db1 = client['sample_airbnb']
mycol = db1['listingsAndReviews']

# Extract data from MongoDB
result = mycol.find()

# Define the CSV file name
csv_file_name = r"C:\Users\DELL\OneDrive\Documents\GitHub\Mugilan\csv\csvairbnb.csv"

# Open the CSV file in write mode
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer
    csv_writer = csv.writer(csv_file)

    # Write the header row
    header_row = ["_id", "listing_url", "name", "summary", "space", "description", "neighborhood_overview",
                  "notes", "transit", "access", "interaction", "house_rules", "property_type", "room_type",
                  "bed_type", "minimum_nights", "maximum_nights", "cancellation_policy", "last_scraped",
                  "calendar_last_scraped", "first_review", "last_review", "accommodates", "bedrooms", "beds",
                  "number_of_reviews", "bathrooms", "amenities", "price", "security_deposit", "cleaning_fee",
                  "extra_people", "guests_included", "picture_url", "host_id", "host_url", "host_name",
                  "host_about", "host_location", "host_response_time", "host_verifications", "area",
                  "longitude", "is_location_exact", "country", "market","latitude"]

    csv_writer.writerow(header_row)

    # Write each document to the CSV file
    for a in result:
        # Extract data from MongoDB document
        v47 =a.get('address',{}).get('location', {}).get('coordinates',[])
        v1 = a.get('_id')
        v2 = str(a.get('listing_url'))
        v3 = str(a.get('name'))
        v4 = str(a.get('summary'))
        v5 = str(a.get('space'))
        v6 = str(a.get('description'))
        v7 = str(a.get('neighborhood_overview'))
        v8 = str(a.get('notes'))
        v9 = str(a.get('transit'))
        v10 = str(a.get('access'))
        v11 = str(a.get('interaction'))
        v12 = str(a.get('house_rules'))
        v13 = str(a.get('property_type'))
        v14 = str(a.get('room_type'))
        v15 = str(a.get('bed_type'))
        v16 = str(a.get('minimum_nights'))
        v17 = str(a.get('maximum_nights'))
        v18 = str(a.get('cancellation_policy'))
        v19 = str(a.get('last_scraped'))
        v20 = str(a.get('calendar_last_scraped'))
        v21 = str(a.get('first_review'))
        v22 = str(a.get('last_review'))
        v23 = str(a.get('accommodates'))
        v24 = str(a.get('bedrooms'))
        v25 = str(a.get('beds'))
        v26 = str(a.get('number_of_reviews'))
        v27 = str(a.get('bathrooms'))
        v28 = ', '.join(map(str, a.get('amenities', [])))
        v29 = str(a.get('price'))
        v30 = str(a.get('security_deposit'))
        v31 = str(a.get('cleaning_fee'))
        v32 = str(a.get('extra_people'))
        v33 = str(a.get('guests_included'))
        v34 = str(a.get('images', {}).get('picture_url'))
        v35 = str(a.get('host', {}).get('host_id'))
        v36 = str(a.get('host', {}).get('host_url'))
        v37 = str(a.get('host', {}).get('host_name'))
        v38 = str(a.get('host', {}).get('host_about'))
        v39 = str(a.get('host', {}).get('host_location'))
        v40 = str(a.get('host', {}).get('host_response_time'))
        v41 = ', '.join(map(str, a.get('host_verifications', [])))
        v42 = str(a.get('address', {}).get('government_area'))
        v43 = v47[0]
        v44 = str(a.get('location', {}).get('is_location_exact'))
        v45= str(a.get('address', {}).get('country'))
        v46= str(a.get('address', {}).get('market'))
        v48=v47[1]

        # Write a row to the CSV file
        csv_writer.writerow([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10,
                             v11, v12, v13, v14, v15, v16, v17, v18, v19, v20,
                             v21, v22, v23, v24, v25, v26, v27, v28, v29, v30,
                             v31, v32, v33, v34, v35, v36, v37, v38, v39, v40,
                             v41, v42, v43, v44, v45, v46,v48])

print(f"CSV file '{csv_file_name}' has been created.")
