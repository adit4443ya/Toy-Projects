import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load the machine learning model
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))

# Load the car dataset
car = pd.read_csv('Cleaned.csv')

# Create dropdown menus
companies = sorted(car['company'].unique())
car_models = sorted(car['name'].unique())
years = sorted(car['year'].unique(), reverse=True)
fuel_types = car['fuel_type'].unique()

# Create the Streamlit app
st.title('Used Car Price Prediction')
# pipe.predict(pd.DataFrame(columns=['name','company','year','kms_driven','fuel_type'],data=np.array(['Maruti Suzuki Swift','Maruti',2019,100,'Petrol']).reshape(1,5)))

# Add dropdowns for user input
company = st.selectbox('Select Company', companies)
car_model = st.selectbox('Select Car Model', car_models)
year = st.selectbox('Select Year', years)
fuel_type = st.selectbox('Select Fuel Type', fuel_types)
kilo_driven = st.number_input('Enter Number of Kilometers Driven')

# Predict function
def predict_price(company, car_model, year, fuel_type, kilo_driven):
    # input_data = np.array([car_model, company, year, kilo_driven, fuel_type]).reshape(1, -1)
    prediction = model.predict(pd.DataFrame(columns=['name','company','year','kms_driven','fuel_type'],data=np.array([car_model, company, year, kilo_driven, fuel_type]).reshape(1,5)))
    return prediction[0]

# When 'Predict' button is clicked
if st.button('Predict'):
    price = predict_price(company, car_model, year, fuel_type, kilo_driven)
    st.success(f'The predicted price of the car is: {round(price, 2)}')
