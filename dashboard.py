import streamlit as st
import pickle
import pandas as pd

st.image(r'C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\images\house.png')
st.text("The Sound of Silence")
st.audio(r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\music.mp3",format='audio/mp3', loop=True)

st.title('Hong Kong Real Estate Market Analysis')
st.write('Welcome to the Real Estate Market Analysis App! This platform is designed for educational purposes, focusing on machine learning and data analysis within the real estate sector.')

st.subheader('a) Summary of the Data Analysis of Real Estate Trends in Hong Kong.')
st.write('The data was scraped from Centanet to uncover insights into real estate in Hong Kong. After data cleansing, the  dataset contains 667 rows. The parameters include region, district, number of bedrooms, gross floor area, salable area, price, building age, and more.')

st.image(r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\images\barplot.png")
st.write('As illustrated in the bar plot above, the majority of real estate properties are located in the New Territories region, accounting for over 50 percent of the dataset.')

st.image(r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\images\boxplot.png")
st.write("Given that price is a significant factor, the box plot here displays property prices across different regions in Hong Kong. It's widely believed that Hong Kong Island has the most expensive real estate compared to other areas.")

st.image(r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\images\corr_matrix.png")
st.write('A correlation matrix heatmap was drawn to identify the underlying factors influencing property prices. As shown, the gross floor area, salable area, and number of bedrooms are significant factors (>.5) contributing to price fluctuations.')

st.image(r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\images\pairplot.png")
st.write('In the pair plot, the salable area, gross floor area, and number of bedrooms were specifically selected to explore their correlations. The observations indicate a positive correlation among these parameters.')

st.subheader('b) Estimated property value prediction')
st.write('Utilizing the sklearn library, a decision tree regressor model was deployed to predict property prices based on parameters like salable area, gross floor area, and the number of bedrooms. The data was split into a 70:30 training and testing ratio. Finally, the model was saved and deployed it in the app for real-time predictions.')
st.write('In the following boxes and sliders, please adjust the handle to see the predicted real estate price.')
st.write('Parameters to consider:')

def numerical(selected_region):
    convert_num = {
        'NT West': 1,
        'NT East': 2,
        'HK Island': 3,
        'Kowloon': 4
    }
    return convert_num[selected_region]

# Save the input features
def input_features():
    selected_region = st.selectbox('Region to analyse', ['NT West', 'NT East', 'HK Island', 'Kowloon'])
    bedroom_count = st.slider('Number of Bedroom(s)', 1, 5)
    building_age = st.slider('Building Age (Years)', 8, 61)
    sa = st.slider('Saleable Floor Area(ft^2)', 222, 2667)
    efficiency = st.slider('Efficiency (%)', 60, 91)
    convenience = st.slider('Time to reach the station (min)', 1, 15)
    data = {
        'num_room': bedroom_count,
        'age': building_age,
        'sa': sa,
        'convenience': convenience,
        'efficiency': efficiency,
        'region': numerical(selected_region)
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Open the saved models
pickle_path = r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\decision_tree_model.pkl"
pickle_scaler_path = r"C:\Users\Edwin\Python\bootcamp\Projects\Project_2\foolproof_house\scaler.pkl"

with open(pickle_path, 'rb') as file:
    saved_model = pickle.load(file)

with open(pickle_scaler_path, 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)

user_df = input_features()

if st.button('Predict'):
    # Scale the input features  
    user_df_scaled = scaler.transform(user_df)

    prediction = saved_model.predict(user_df_scaled)
    st.write(f'Predicted Output: ${prediction[0]:,.1f}M')  

st.subheader('c) Model Limitations')
st.write(
'The model does not accurately represent market trends due to the omission of one-hot encoding during the implementation of the decision tree regression. As a result, please avoid using this model for real estate analysis, as it tends to overestimate property prices.'   
    )