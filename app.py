import streamlit as st
import pickle
import numpy as np
import pandas as pd
import datetime
import os

# Page Config
st.set_page_config(page_title="AI Inventory Dashboard", page_icon="📦", layout="wide")

# Load model
with open("models/model.pkl", "rb") as f:
    model = pickle.load(f)

# Custom CSS
st.markdown("""
    <style>
        .main-container {
            padding: 2rem;
            max-width: 1200px;
            margin: auto;
        }

        .gradient-header {
            font-size: 42px;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #1f77b4, #23a6d5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0;
        }

        .card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .small-text {
            color: gray;
            font-size: 14px;
        }

        footer {
            margin-top: 50px;
            text-align: center;
            color: #aaa;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="gradient-header">📦 AI-Powered Inventory Dashboard</h1>', unsafe_allow_html=True)
st.markdown('Predict demand, reduce waste, and make smarter decisions 🧠')
st.markdown('</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Single Forecast", "📁 Bulk Forecast", "📊 Dashboard"])

# --- TAB 1: Single Prediction ---
with tab1:
    st.markdown("### 🧾 Predict for One Day")

    with st.form("single_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            day = st.selectbox(
                "📅 Day of the Week",
                list(range(7)),
                format_func=lambda x: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][x]
            )
        with col2:
            is_holiday = st.radio("🎉 Is it a Holiday?", [0, 1], format_func=lambda x: "Yes" if x else "No")
        with col3:
            temp = st.slider("🌡️ Temperature (°C)", 10, 45, 25)

        submit1 = st.form_submit_button("Predict")

    if submit1:
        X_input = np.array([[day, is_holiday, temp]])
        prediction = int(model.predict(X_input)[0])

        st.markdown("#### ✅ Prediction Result")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📦 Units to Stock", f"{prediction}")
        with col2:
            st.markdown(f"**Prediction Date:** `{datetime.date.today()}`")

        st.success("Prediction completed!")
        st.balloons()

# --- TAB 2: Bulk Prediction via CSV ---
with tab2:
    st.markdown("### 📂 Upload CSV for Bulk Forecast")

    uploaded_file = st.file_uploader("Upload a CSV with columns: day_of_week, is_holiday, temperature", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        try:
            X_bulk = df[["day_of_week", "is_holiday", "temperature"]]
            df["predicted_units"] = model.predict(X_bulk).astype(int)

            st.markdown("### 📊 Prediction Table")
            st.dataframe(df)

            # Save to output
            os.makedirs("outputs", exist_ok=True)
            output_path = "outputs/predictions.csv"
            df.to_csv(output_path, index=False)

            st.download_button("⬇️ Download Predictions", data=df.to_csv(index=False), file_name="predictions.csv", mime="text/csv")

        except Exception as e:
            st.error(f"Error in file: {e}")

# --- TAB 3: Dashboard ---
with tab3:
    st.markdown("### 📈 Coming Soon: Advanced Insights Dashboard")
    st.markdown("You'll be able to view:")
    st.markdown("- Weekly demand trends")
    st.markdown("- Product category insights")
    st.markdown("- Weather impact analysis")
    st.image("https://cdn-icons-png.flaticon.com/512/553/553416.png", width=120)

# Footer
st.markdown("<footer>🚀 Built by Saikat • Inspired by Too Good To Go • Powered by Streamlit</footer>", unsafe_allow_html=True)
