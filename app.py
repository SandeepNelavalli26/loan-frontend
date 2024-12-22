import streamlit as st
import requests

# Hardcoded dropdown options
education_options = ["High School", "Bachelor's", "Master's", "Doctorate"]
loan_intent_options = ["Education", "Medical", "Business", "Personal", "Home", "Venture"]

# Streamlit App Title
st.title("Loan Approval Prediction")

# Input Fields
st.header("Enter Applicant Details")

age = st.number_input("Age:", min_value=18, max_value=100, step=1, value=30)
gender = st.selectbox("Gender:", options=["Male", "Female"])
education = st.selectbox("Education Level:", options=education_options)
income = st.number_input("Annual Income ($):", min_value=1000, step=500, value=50000)
loan_amount = st.number_input("Loan Amount ($):", min_value=500, step=500, value=5000)
loan_intent = st.selectbox("Loan Intent:", options=loan_intent_options)

# Credit Score with slider and input field
st.markdown("### Credit Score")
credit_score_slider = st.slider("Drag to select credit score:", min_value=300, max_value=850, value=600, key="slider")

# Synchronize slider and input field
credit_score_input = st.number_input(
    "Enter credit score:", min_value=300, max_value=850, value=credit_score_slider, step=1, key="input"
)

# Ensure synchronization between slider and input
if credit_score_input != credit_score_slider:
    credit_score_slider = credit_score_input
elif credit_score_slider != credit_score_input:
    credit_score_input = credit_score_slider

# Convert categorical inputs to numeric values
gender_mapping = {"Male": 1, "Female": 0}
education_mapping = {value: idx for idx, value in enumerate(education_options)}
loan_intent_mapping = {value: idx for idx, value in enumerate(loan_intent_options)}

# Prepare input for the backend
input_data = {
    "age": age,
    "gender": gender_mapping[gender],
    "education": education_mapping[education],
    "income": income,
    "loan_amount": loan_amount,
    "loan_intent": loan_intent_mapping[loan_intent],
    "credit_score": credit_score_input,  # Use synchronized value
}

# Center the button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Predict Loan Approval"):
    try:
        # API URL
        api_url = "https://my-app-latest-sr66.onrender.com/predict"
        
        # Make a POST request to the FastAPI backend
        response = requests.post(api_url, json=input_data)
        
        if response.status_code == 200:
            result = response.json()
            prediction = result['prediction']
            probabilities = result['probabilities']
            
            # Display appropriate message based on prediction
            if prediction == 0:
                approval_prob = probabilities['class_0'] * 100
                st.success(f"Loan Approved: {approval_prob:.2f}% chance of approval.")
            else:
                rejection_prob = probabilities['class_1'] * 100
                st.error(f"Loan Rejected: {rejection_prob:.2f}% chance of rejection.")
        else:
            st.error(f"Error: {response.text}")
    except Exception as e:
        st.error(f"Failed to connect to the backend. Details: {str(e)}")
st.markdown("</div>", unsafe_allow_html=True)
