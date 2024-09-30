import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Set the page config at the beginning
st.set_page_config(page_title="EV Charger Product Info", layout="centered")

# Function to display the product image
def display_image(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        st.image(img, use_column_width=True)
    except Exception as e:
        st.error("Image could not be loaded. Please check the Image URL.")

# Function to display the product PDF using an iframe
def display_pdf(url):
    try:
        pdf_display = f'<iframe src="{url}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error("PDF could not be loaded. Please check the PDF URL.")

# Load data from Google Sheet (public URL)
@st.cache_data
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1zDVJ5vLKVpP2mxMHjA3SvRnpBNEcHvVW0cP_trh5QGg/pub?output=csv"
    return pd.read_csv(sheet_url)

# Streamlit UI
st.title("🚗 EV Charger Product Information")
st.markdown("---")  # Horizontal line for separation

# Load the data
data = load_data()

# Dropdown for selecting a product
product = st.selectbox("🔍 Select a Product", data['Product Name'].unique())

# Fetch and display product-specific information
if product:
    product_data = data[data['Product Name'] == product].iloc[0]

    # Display image
    st.subheader(f"🖼️ {product} Image")
    display_image(product_data['Image URL'])

    # Display specifications with formatting
    st.subheader(f"📋 {product} Specifications")
    
    st.markdown(f"""
    - **Power**: {product_data['Power Rating']}
    - **Voltage**: {product_data['Voltage']}
    - **Dimensions**: {product_data['Dimensions']}
    """)

    # Display PDF
    st.subheader(f"📄 {product} PDF Manual")
    display_pdf(product_data['PDF URL'])

# Footer
st.markdown("---")
st.write("© 2024 EV Charger Company. All rights reserved.")
