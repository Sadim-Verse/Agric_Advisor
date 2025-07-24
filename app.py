import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import time

from yield_ import get_countries, get_crops, get_min_max, crop_classification
from huggingface_hub import InferenceApi

# # Load the required files
# inference = InferenceApi(
#     repo_id = "Sad1m/agric_advisor",
#     token= "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"
# )

model = joblib.load(r"rfc_model_c.joblib")
le_co = joblib.load(r"country_le")
le_cr = joblib.load(r"crop_le")

st.set_page_config(
    page_title="An Agric Advisor",
    layout="wide"
)
    
# Change the font size and style of the page
st.markdown("""
            <style>
            html, body {
            font-size: 20px;
            font-family: 'courier', 'sans-serif';
            }
            </style>
            """, unsafe_allow_html=True)



with st.sidebar:
    st.header("🌾 Crop Yield Predictor")
    st.write(
        """
        This app uses a regression model to predict a crop’s **annual yield** based on:
        - **Country** where it’s planted  
        - **Crop** 
        - Average annual **temperature**
        - Total annual **rainfall**
        - Average annual **pesticide use**
        """
    )
    st.info(
        """
        To get an accurate prediction, please make sure *all* inputs are provided correctly.
        """
    )

# Interface for the user to get input the features
st.title("Agric Advisor")
st.markdown("""<html>
            <i>Planning your next big harvest? Agric Advisor provides data-driven predictions and tailored suggestions
             for large-scale farmers looking to maximize crop yields and streamline operations.</i>
            <p></p>
            </html>
            """, unsafe_allow_html=True)
st.write("#")


# Get the country names
country_names = get_countries()
country_name = st.selectbox(
    "**Where are you planting your crops?**", country_names,
    index=None,
    placeholder="Select your country...",
    accept_new_options=False,
    )
st.write(f"You Selected: **{country_name}**")


st.write("--------------------------")

# Get the Crop names
crop_names = get_crops()
crop_name = st.selectbox("**What crop are you planting?**", crop_names, 
                      index=None, placeholder="Select your crop...")
st.write(f"You Selected: {crop_name}")


st.write("--------------------------")

# Enter the numerical values
avg_rainfall = st.number_input("Average Annual Rainfall: ", 
                               min_value=get_min_max(1, 0, 'rain'), 
                               max_value=get_min_max(0, 1, 'rain'),
                               value=None, placeholder=0.00)

st.write("--")
pesticide_use = st.number_input("Amount of pesticides used: ", 
                                min_value=get_min_max(1, 0, 'pest'),
                                max_value=get_min_max(0, 1, 'pest'),
                                value=None, placeholder=0.00)

st.write("--")
avg_temp = st.number_input("Average Weather Temperature: ",
                           min_value=get_min_max(1, 0, 'temp'),
                           max_value=get_min_max(0, 1, 'temp'),
                           value=None, placeholder=0.00)


country_name = le_co.transform(pd.Series(data=country_name))
crop_name = le_cr.transform(pd.Series(data=crop_name))

# Model prediction

predict_button = st.button("Predict Annual Crop Yield")
predicted_yield = 0

# if predict_button and 

if predict_button:
    features = pd.DataFrame({'Country': country_name, 'Crop': crop_name, 'Average_annual_rainfall(mm)': avg_rainfall,
       'Pesticides_used(tonnes)': pesticide_use, 'Average_temperature(degree C)': avg_temp})
    
    predicted_yield = model.predict(features)[0]
    crop_name = le_cr.inverse_transform(crop_name)[0].lower()
    st.write(f"Predicted yield for {crop_name} is {predicted_yield} hectogram per hectare")

# Logic for the suggestions to the user

if predicted_yield != 0:
    crop_classification(crop_name, predicted_yield)



from huggingface_hub import HfApi
from huggingface_hub import upload_file

# api = HfApi()
# api.create_repo(repo_id="agric_advisor", private=True)

# api.upload_folder(
#     repo_id = "Sad1m/agric_advisor",
#     folder_path= r"C:\Users\HP\Projects\Python_for_ML\Regression\Agric_advisor",
#     path_in_repo="",
#     repo_type= "space"
# )
