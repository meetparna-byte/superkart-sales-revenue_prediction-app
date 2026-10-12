import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend (resolves over Docker network name)
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Sales Revenue Prediction")

# Section for online prediction
st.subheader("Online Predictor")

# Collect user input for SuperKart features
product_weight = st.number_input("Product Weight (kg)", min_value=0.1, max_value=50.0, value=12.5, step=0.1)
product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_allocated_area = st.number_input("Product Allocated Area Ratio (0 to 1)", min_value=0.0, max_value=1.0, value=0.06, format="%.4f")
product_mrp = st.number_input("Product Maximum Retail Price (MRP) ($)", min_value=1.0, value=150.0, step=0.5)
store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
product_id_char = st.number_input("Product Id", ["FD","NC", "DR"] )
store_age_years = st.number_input("Store Age (Years)", min_value=1, max_value=100, value=15)
product_type_category = st.selectbox("Product Type Category", ["Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", "Household", "Baking Goods", "Canned", "Health and Hygiene", "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Others", "Starchy Foods", "Breakfast", "Seafood"])

# Convert user input into JSON payload
payload = {
    'Product_Weight': product_weight,
    'Product_Sugar_Content': product_sugar_content,
    'Product_Allocated_Area': product_allocated_area,
    'Product_MRP': product_mrp,
    'Store_Size': store_size,
    'Store_Location_City_Type': store_location_city_type,
    'Store_Type': store_type,
    'Product_Id_char': product_id_char,
    'Store_Age_Years': store_age_years,
    'Product_Type_Category': product_type_category
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict Sales", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales']
        st.success(f"Predicted Store Sales Revenue: ${prediction:,.2f}")
    else:
        st.error(f"Unable to connect to the prediction API (Status Code: {response.status_code}).")

# Section for batch prediction
st.subheader("Batch Predictor")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload SuperKart CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch Sales", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display predictions mapping
        else:
            st.error("Unable to connect to the prediction API.")
