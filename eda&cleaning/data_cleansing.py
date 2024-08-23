# Import relevant libraries
import pandas as pd
import re

# Open files
df = pd.read_excel('./estate_new.xlsx')

# Extract columns from df; rename columns
extract_df = df[['title-lg',	'title-sm',	'adress',	'adress 2',
                'hidden-xs-only 2', 'area-price', 'box 4', 'area-price 2',
                'price-info', 'installment', 'adress 6', 'facility-tag']]

extract_df = extract_df.rename(columns={'title-lg': 'address', 'title-sm': 'num_room', 'adress': 'district',
                            'adress 2': 'age', 'hidden-xs-only 2': 'sa',
                            'area-price': 'sap', 'box 4': 'gfa', 'area-price 2': 'gfap',
                            'price-info': 'price', 'installment': 'monthly',
                            'adress 6': 'efficiency', 'facility-tag': 'convenience'
                            })
# Regular expressions

# 1. Number of rooms
extract_df['num_room'] = extract_df['num_room'].str.extract(r"(\d+)\s*Rooms?")
extract_df['num_room'] = extract_df['num_room'].astype('Int64') 

# 2. Building age
extract_df['age'] = extract_df['age'].str.extract(r"(\d+)\s*years?")
extract_df['age'] = extract_df['age'].astype('Int64') 

# 3. Saleable Area & Gross area

extract_df['sa'] = extract_df['sa'].str.replace(",","")
extract_df['sa'] = extract_df['sa'].str.extract(r"(\d+)")
extract_df['sa'] = extract_df['sa'].astype('Int64')

extract_df['gfa'] = extract_df['gfa'].str.replace(",","")
extract_df['gfa'] = extract_df['gfa'].str.extract(r"(\d+)")
extract_df['gfa'] = extract_df['gfa'].astype('Int64')

# 4. Saleable Area Price & Gross area Price
extract_df['sap'] = extract_df['sap'].str.replace(r"[@$,]", "", regex=True)
extract_df['sap'] = extract_df['sap'].astype('Int64')

extract_df['gfap'] = extract_df['gfap'].str.replace(r"[@$,]", "", regex=True)
extract_df['gfap'] = extract_df['gfap'].astype('Int64')

# 5. Monthly
extract_df['monthly'] = extract_df['monthly'].str.replace(r"[Monthly$,・]", "", regex=True)
extract_df['monthly'] = extract_df['monthly'].astype('Int64')

# 6. Efficiency
extract_df['efficiency'] = extract_df['efficiency'].str.extract(r'(\d+)')
extract_df['efficiency'] = extract_df['efficiency'].astype('Int64')

# 7. Convenience
extract_df['convenience'] = extract_df['convenience'].str.extract(r'(\d+)')
extract_df['convenience'] = extract_df['convenience'].astype('Int64')

# Further cleansing
extract_df = extract_df.drop(['efficiency'], axis=1)
extract_df = extract_df.dropna()

# Create a new column efficiency after dropping null values
extract_df['efficiency'] = (extract_df['sa'] / extract_df['gfa']) * 100
extract_df['efficiency'] = extract_df['efficiency'].astype('Int64')

# Group the districts into regions; create a new column as region
region_dict = {
    'NT East': [
        'City One Shatin', 'Deep Bay', 'Fanling', 'Fo Tan', 
        'Ha Kwai Chung', 'Heng On', 'Ma On Shan', 'Ma Tau Wai', 
        'Po Lam', 'Sai Ying Pun', 'Sha Tin', 'Sheung Shui', 
        'Tiu Keng Leng', 'Tseung Kwan O', 'Yuen Long Station', 
        'Yuen Long Town Centre'
    ],
    'NT West': [
        'Discovery Park', 'Four Little Dragons', 'Laguna', 
        'Lai King', 'Lai Wan', 'Lam Tin', 'Lohas Park', 
        'Luk Yeung', 'Tai Hang', 'Tai Kok Tsui', 
        'Tai Po Town Centre', 'Tai Wai', 'Tai Wo Hau', 
        'Taikoo Shing', 'Tin Shui Wai', 'Tsuen King Circuit', 
        'Tsuen Wan Hoi Bun', 'Tsuen Wan Town Centre', 
        'Tsuen Wan West', 'Tuen Mun North', 'Tuen Mun Town Centre', 
        'Tung Chung Town Centre'
    ],
    'Kowloon': [
        'Cheung Sha Wan', 'Diamond Hill', 'Hung Hom', 
        'Jordan', 'Kowloon Bay', 'Kowloon City', 'Kowloon Station', 
        'Ngau Chi Wan', 'Prince Edward', 'Wong Tai Sin', 
        'Whampoa', 'San Po Kong', 'Yau Ma Tei'
    ],
    'HK Island': [
        'Causeway Bay', 'Chai Wan', 'Kennedy Town', 'North Point', 
        'Sai Wan Ho', 'Sheung Wan', 'Mid-Levels Central', 
        'Mid-Levels West', 'Tin Hau', 'Tsim Sha Tsui', 
        'Wan Chai', 'Quarry Bay', 'Residence Bel-air', 
        'Olympic Station', 'Kornhill', 'Siu Hong', 
        'Siu Lek Yuen', 'Siu Sai Wan', 'South Horizons', 
        'North Point Mid-Levels'
    ]
}

def get_region(district):
    for region, districts in region_dict.items():
        if district in districts:
            return region

extract_df['region'] = extract_df['district'].apply(get_region)

# Save the file into a csv format for further analysis
extract_df = extract_df.dropna()
extract_df.to_csv("./cleaned.csv", index=False)
