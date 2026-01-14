import streamlit as st


from prediction_helper import predict


# -------------------------------------------------------------------------------

st.set_page_config(page_title="Credit Risk Model", page_icon="💳", layout="wide")

# Custom CSS to spruce up the look
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💳 Credit Risk Scoring System")
st.markdown("Enter the applicant's details below to calculate credit risk, score, and rating.")

# --- SECTION 1: Personal & Financial ---
st.subheader("👤 Applicant Information")
col1, col2, col3 = st.columns(3)

with col1:
    age = st.number_input('Age', min_value=18, max_value=100, step=1, value=28)
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])

with col2:
    income = st.number_input('Annual Income (₹)', min_value=0, value=1200000, step=10000)
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])

with col3:
    loan_amount = st.number_input('Loan Amount Request (₹)', min_value=0, value=2560000, step=10000)
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

# --- SECTION 2: Loan & History ---
st.subheader("📊 Credit History & Loan Details")
col4, col5, col6 = st.columns(3)

with col4:
    loan_tenure_months = st.number_input('Loan Tenure (Months)', min_value=0, step=1, value=36)
    delinquency_ratio = st.slider('Delinquency Ratio (%)', 0, 100, 30)

with col5:
    avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20)
    credit_utilization_ratio = st.slider('Credit Utilization Ratio (%)', 0, 100, 30)

with col6:
    num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)

    # Calculate Ratio dynamically for display
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    st.metric(label="Loan to Income Ratio", value=f"{loan_to_income_ratio:.2f}")

st.markdown("---")

# --- SECTION 3: Prediction ---
if st.button('🚀 Calculate Risk Profile'):

    # Call your actual predict function
    probability, credit_score, rating = predict(age, income, loan_amount, loan_tenure_months,
                                                avg_dpd_per_delinquency, delinquency_ratio,
                                                credit_utilization_ratio, num_open_accounts,
                                                residence_type, loan_purpose, loan_type)

    st.subheader("Risk Analysis Results")

    res_col1, res_col2, res_col3 = st.columns(3)

    with res_col1:
        st.metric(label="Credit Score", value=credit_score)

    with res_col2:
        st.metric(label="Rating", value=rating)
        if rating in ['Poor', 'Very Poor']:
            st.error("High Risk Applicant")
        elif rating in ['Average', 'Fair']:
            st.warning("Moderate Risk Applicant")
        else:
            st.success("Low Risk Applicant")

    with res_col3:
        st.write("Default Probability")
        st.progress(probability)
        st.caption(f"Probability: {probability:.2%}")