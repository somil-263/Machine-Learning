import streamlit as st

st.title("⚖️ Premium BMI Calculator")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    heightft = st.number_input("Height (Feet)", min_value=1, max_value=8, value=5, step=1)
with col2:
    heightin = st.number_input("Height (Inches)", min_value=0, max_value=11, value=7, step=1)
with col3:
    weight = st.number_input("Weight (in kg)", min_value=1, value=65, step=1)

total_inches = heightin + (heightft * 12)

height_m = (total_inches * 2.54) / 100

bmi = weight / (height_m ** 2)

st.markdown("### Your Results")

st.metric(label="Calculated BMI", value=f"{bmi:.1f}")

if bmi < 18.5:
    st.info("Category: **Underweight** 🟡")
elif 18.5 <= bmi < 24.9:
    st.success("Category: **Healthy / Normal Weight** 🟢")
elif 24.9 <= bmi < 29.9:
    st.warning("Category: **Overweight** 🟠")
else:
    st.error("Category: **Obese** 🔴")