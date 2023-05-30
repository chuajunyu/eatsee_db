import psycopg2
import csv
conn = psycopg2.connect("host=localhost dbname=Eatsee user=postgres password=eatseegng")
cur = conn.cursor()
with open (r'C:\Users\liuyu\OneDrive\Documents\school\pgadmin\data.csv') as file:
    reader = csv.DictReader(file)
    next(reader)
    cuisine = ['Chinese', 'Malay', 'Indian', 'Western', 'Korean', 'Japanese', 'Indonesian', 'Vietnamese']
    diet = ['Halal', 'No Halal', 'Vegetarian', 'No Vegetarian', 'Vegan', 'No Vegan']
    area = ['Bishan', 'Bukit Merah', 'Bukit Timah', 'Downtown Core', 'Geylang', 'Kallang', 'Marina East', 'Marina South', 'Marine Parade', 'Museum', 
            'Newton', 'Novena', 'Orchard', 'Outram', 'Queenstown', 'River Valley', 'Rochor', 'Singapore River', 'Southern Islands', 'Straits View', 
            'Tanglin', 'Toa Payoh', 'Bedok', 'Changi', 'Changi Bay', 'Pasir Ris', 'Paya Lebar', 'Tampines', 'Central Water Catchment', 'Lim Chu Kang', 
            'Mandai', 'Sembawang', 'Simpang', 'Sungei Kadut', 'Woodlands', 'Yishun', 'Ang Mo Kio', 'Hougang', 'North-Eastern Islands', 'Punggol', 
            'Seletar', 'Sengkang', 'Serangoon', 'Boon Lay', 'Bukit Batok', 'Bukit Panjang', 'Choa Chu Kang', 'Clementi', 'Jurong East', 'Jurong West', 
            'Pioneer', 'Tengah', 'Tuas', 'Western Islands', 'Western Water Catchment']
    for row in reader:      
        cur.execute(
        "INSERT INTO restaurant(restaurant_name) VALUES (%s)",
        (row['Restaurant Name'],)
        )
        cur.execute(
                    "SELECT restaurant_id FROM restaurant WHERE restaurant_name = %s",
                    (row['Restaurant Name'],)
                    )
        restaurant_id = cur.fetchone()
        
        for areas in area:
            if row['Town/Region'] == areas:
                cur.execute(
                            "SELECT area_id FROM area WHERE area_name = %s",
                            (areas,)
                            )
                area_id = cur.fetchone()
                cur.execute(
                'INSERT INTO restaurant_location_ref(address, postal_code, restaurant_ref_id, area_ref_id) VALUES (%s,%s, %s, %s)',
                (row['Restaurant Name'], (row['Postal Code']),restaurant_id, area_id)
                )

        for cuisines in cuisine:
            if row['Cuisine'] == cuisines:
                cur.execute(
                            "SELECT cuisine_id FROM cuisine WHERE cuisine = %s",
                            (cuisines,)
                            )
                cuisine_id = cur.fetchone()
                cur.execute(
                "INSERT INTO restaurant_cuisine_ref(restaurant_ref_id, restaurant_cuisine_ref_id) VALUES (%s, %s)",
                (restaurant_id, cuisine_id,)
                )
        
            
        for row_diet in row['Dietary Restrictions'].split(','):
            
            for diets in diet:    
                if row_diet.strip() == diets:
                    
                    cur.execute(
                            "SELECT diet_id FROM diet WHERE diet_res_type = %s",
                            (diets,)
                            )
                    diet_id = cur.fetchone()
                    cur.execute(
                        "INSERT INTO restaurant_diet_ref(restaurant_ref_id, restaurant_diet_ref_id) VALUES (%s, %s)",
                    (restaurant_id, diet_id,)    
                    )
        
        
conn.commit()