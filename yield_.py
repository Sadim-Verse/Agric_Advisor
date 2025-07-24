import numpy as np
import pandas as pd
import streamlit as st
import time

yield_data = pd.read_csv(r"new_yield_df.csv")

yield_data

def get_countries():
    return tuple(yield_data['Country'].unique())

def get_crops():
    return tuple(yield_data['Crop'].unique())

def get_min_max(min, max, col):
    if( (min > 0) and (max == 0) ):
        if(col == 'rain'):
            return yield_data['Average_annual_rainfall(mm)'].min()
        elif(col == 'pest'):
            return yield_data['Pesticides_used(tonnes)'].min()
        elif(col == 'temp'):
            return yield_data['Average_temperature(degree C)'].min()

    elif( (min < 0) and (max == 0) ):
        if(col == 'rain'):
            return yield_data['Average_annual_rainfall(mm)'].max()
        elif(col == 'pest'):
            return yield_data['Pesticides_used(tonnes)'].max()
        elif(col == 'temp'):
            return yield_data['Average_temperature(degree C)'].max()

crop_type = ""  
# Classify the crops into different categories:
def crop_classification(crop_name, predicted_yield):
    global crop_type 

    cereal_crops = ['Maize', 'Rice, paddy', 'Sorghum', 'Wheat']
    root_crops = ['Potatoes', 'Yams']
    tuber_crops = ['Cassava', 'Sweet potatoes']
    legume_crops = ['Soybeans']
    fruit_crops = ['Plantains and others']

    crop = crop_name.capitalize()

    if(crop in cereal_crops): crop_type = "cereal"
    elif(crop in root_crops): crop_type = "root"
    elif(crop in tuber_crops): crop_type = "tuber"
    elif(crop in legume_crops): crop_type = "legume"
    elif(crop in fruit_crops): crop_type = "fruit"
    
    with st.spinner("Loading..."):
        time.sleep(1.5)
    crop_specs(crop_name, predicted_yield)

specs = {
    "Rainfall": {
        "Poor": "If your area receives less rain than your crop needs,"
        " consider adding water-saving methods like zai pits, contour ridges, or mulch to retain moisture.",

        "Average": "If the rains are unpredictable, wait until you’ve had two steady rainfall events before planting."
        " You can also shape shallow ridges in your field to help more water soak in when it does rain.",

        "Good": "If rainfall differs by at least 15% across your field,"
        " install multiple rain gauges and apply extra water only where it's needed.",

        "Excellent": "If your soil isn’t holding enough water, try deep ripping,"
        " apply organic mulch, or grow cover crops to improve retention."
    },

    "Temperature": {
        "Poor": "Does the temperature fall outside the crop’s comfort zone?"
        " Shift planting dates or switch to stress-tolerant varieties.",

        "Average": "If your area stays in the 30–35 °C range during early growth stages, "
        "apply foliar nutrients like zinc and boron to support healthy grain formation even under heat stress.",

        "Good": "If you’re seeing occasional bursts of heat or cold, "
        "sign up for local weather alerts. Use these to time biostimulant or growth regulator sprays more effectively.",

        "Excellent": "If your crops already handle tough weather well, "
        "run small on-farm trials with new, stress-tolerant varieties to future-proof your production."
    },

    "Pesticide": {
        "Poor": "Are you scouting for pests/diseases regularly? If you're not inspecting your field regularly,"
        " start doing weekly checks. And make sure your spraying equipment is properly calibrated before applying any treatments.",

        "Average": "If you’re using a fixed spray calendar, it's time to switch. "
        "Spray only when pest thresholds are reached, and use seed treatments at planting to reduce early-season outbreaks.",

        "Good": "If you notice pest or disease hotspots,"
        " use traps or field imagery to find those zones and treat them specifically—no need to spray the entire field.",

        "Excellent": "If you’re spraying more than recommended for your crop type, consider forming a local IPM (Integrated Pest Management) "
        "group to share natural controls and remove the least effective treatments from your routine."
    }
}

def crop_specs(crop_name, predicted_yield):

    if(crop_name == "rice, paddy"):
        crop_name = "rice(paddy)"
    st.write(f"{crop_name.capitalize()} is a {crop_type} crop.")

    if predicted_yield < 20000:
        st.markdown("""<html>
            <p>Your annual crop yield is <b>low.</b> <i>Here are a few things worth checking:</i>
                    </p>
            <p></p>
            </html>
            """, unsafe_allow_html=True)
        my_list = [specs["Rainfall"]["Poor"], specs["Temperature"]["Poor"], specs["Pesticide"]["Poor"]]
        markdown_list = "\n".join([f"- {item}" for item in my_list])
        st.markdown(markdown_list)
        
        

    elif predicted_yield < 40000:
        st.markdown("""<html>
            <p>Your yield is average—<b>not bad,</b> <i>but there's room to grow. Try these steps to push closer to good or excellent: </i>
                    </p>
            <p></p>
            </html>
            """, unsafe_allow_html=True)
        my_list = [specs["Rainfall"]["Average"], specs["Temperature"]["Average"], specs["Pesticide"]["Average"]]
        markdown_list = "\n".join([f"- {item}" for item in my_list])
        st.markdown(markdown_list)

    
    elif predicted_yield < 60000:
        st.markdown("""<html>
            <p>Your crop yield is good—<b>well done!</b>! <i>To improve even further, consider the following:   </i>
                    </p>
            <p></p>
            </html>
            """, unsafe_allow_html=True)
        my_list = [specs["Rainfall"]["Good"], specs["Temperature"]["Good"], specs["Pesticide"]["Good"]]
        markdown_list = "\n".join([f"- {item}" for item in my_list])
        st.markdown(markdown_list)
    

    elif predicted_yield >= 60000:
        st.markdown("""<html>
            <p>Your annual crop yield is excellent—<b>great job!</b> <i>But even high-performing farms have room to level up:</i>
                    </p>
            <p></p>
            </html>
            """, unsafe_allow_html=True)
        my_list = [specs["Rainfall"]["Excellent"], specs["Temperature"]["Excellent"], specs["Pesticide"]["Excellent"]]
        markdown_list = "\n".join([f"- {item}" for item in my_list])
        st.markdown(markdown_list)


