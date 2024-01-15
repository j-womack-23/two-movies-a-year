# app.py

import streamlit as st
import pandas as pd
import random

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
    year = random.choice(df['Year'])
    option = random.choice(['Option_J', 'Option_K'])
    selected_option = df.loc[df['Year'] == year, option].values[0]
    return f'{selected_option} ({year})'

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
        if sheet_url:
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
        st.write("Selected Movie:", result)

if __name__ == "__main__":
    main()
