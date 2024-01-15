# app.py

import streamlit as st
import pandas as pd
import random
import base64

def convert_to_csv_url(sheet_url):
    # Extract the unique part of the Google Sheets URL (between 'd/' and '/edit')
    start = sheet_url.find('/d/') + 3
    end = sheet_url.find('/edit', start)
    unique_id = sheet_url[start:end]

    # Construct the CSV export URL
    csv_url = f"https://docs.google.com/spreadsheets/d/{unique_id}/export?format=csv"
    return csv_url

# Randomize the selection
def randomize_selection(df):
    year = random.choice(df.iloc[:, 0])  # Assuming column A (index 0) is 'Year'
    option_index = random.choice([1, 2])  # Randomly choose between column B (index 1) and column C (index 2)
    selected_option = df.iloc[:, option_index]
    selected_value = selected_option[df.iloc[:, 0] == year].values[0]
    return f'{selected_value} ({year})'

# Streamlit GUI
def main():
    st.title("Random Movie Selector")

    # Option for user to choose data source
    source_option = st.selectbox("Select data source", ["Upload CSV", "Google Sheets URL"])

    if source_option == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            show_random_movie(data)
    elif source_option == "Google Sheets URL":
        sheet_url = st.text_input("Enter the Google Sheets URL")
        if st.button("Load Sheet"):
            csv_url = convert_to_csv_url(sheet_url)
            try:
                data = pd.read_csv(csv_url)
                show_random_movie(data)
            except Exception as e:
                st.error(f"Error loading data: {e}")

# Function to display random movie
def show_random_movie(data):
    if st.button("Generate Random Movie"):
        result = randomize_selection(data)
        st.markdown(f"<div class='selected-movie'>Selected Movie: {result}</div>", unsafe_allow_html=True
                   )

# Function to display the app logo with color inversion in dark mode
def display_logo():
    file_path = 'Two-Movies-A-Year_LOGO.png'
    with open(file_path, "rb") as file:
        logo_base64 = base64.b64encode(file.read()).decode()
    st.markdown(
        f"<img src='data:image/png;base64,{logo_base64}' class='app-logo' alt='App Logo'>", 
        unsafe_allow_html=True
    )

# Streamlit GUI
def main():
    # Custom CSS
    st.markdown("""
        <style>
        .app-logo {
            height: 100px; 
            filter: invert(var(--logo-invert));
        }
        .selected-movie {
            font-size: 4vw;
        }
        </style>
        """, unsafe_allow_html=True)
    
    display_logo()

    st.title("Random Movie Selector")
    
if __name__ == "__main__":
    main()
