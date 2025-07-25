import streamlit as st
import pickle
import numpy as np

# Load model and columns
model = pickle.load(open('best_model.pkl', 'rb'))
model_columns = pickle.load(open('model_columns.pkl', 'rb'))

# Collect user input
total_sqft = st.number_input("Total Area (sqft)", min_value=300, max_value=10000)
bath = st.slider("Number of Bathrooms", 1, 5)
balcony = st.slider("Number of Balconies", 1, 3)
area_type = st.selectbox("Area Type", ["Super built-up Area", "Built-up Area", "Plot Area"])
location = st.selectbox("Location", ["Electronic City Phase II", "Uttarahalli", "Lingadheeranahalli", "Kothanur", "Other"])

# Map categorical inputs to dummy variables
area_type_dummy = {
    "Super built-up Area": [1, 0, 0],
    "Built-up Area": [0, 1, 0],
    "Plot Area": [0, 0, 1],
}
location_dummy = {
    "Electronic City Phase II": [1, 0, 0, 0, 0],
    "Uttarahalli": [0, 1, 0, 0, 0],
    "Lingadheeranahalli": [0, 0, 1, 0, 0],
    "Kothanur": [0, 0, 0, 1, 0],
    "Other": [0, 0, 0, 0, 1],
}

if st.button("Predict Price"):
    # Construct a dictionary with keys matching model_columns
    input_dict = {
        'total_sqft': total_sqft,
        'bath': bath,
        'balcony': balcony,
        **{f'area_type_{k}': v for k, v in zip(["Super built-up Area", "Built-up Area", "Plot Area"], area_type_dummy[area_type])},
        **{f'location_{k}': v for k, v in zip(["Electronic City Phase II", "Uttarahalli", "Lingadheeranahalli", "Kothanur", "Other"], location_dummy[location])},
    }

    # Created a row with zeros, then fill in the user's selections
    X_pred = np.zeros(len(model_columns))
    for idx, col in enumerate(model_columns):
        if col in input_dict:
            X_pred[idx] = input_dict[col]

    # Predict
    pred = model.predict(X_pred.reshape(1, -1))
    st.success(f"Predicted Price: ₹{pred[0]:,.2f} lakhs")
