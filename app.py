# app.py

import streamlit as st
import pandas as pd
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from io import StringIO

# Google Sheets API setup
def authenticate_gsheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Read data from Google Sheets
def read_google_sheets(sheet_url):
    client = authenticate_gsheets()
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_values()
    headers = data.pop(0)
    return pd.DataFrame(data, columns=headers)

# Randomize the selection
def randomize_selection(df):
    year = random.choice(df['Year'])
    option = random.choice(['Option_J', 'Option_K'])
    selected_option = df.loc[df['Year'] == year, option].values[0]
    return f'{selected_option} ({year})'

# Streamlit GUI
def main():
    st.title("Random Movie Selector")

    # Options for data source
    source_option = st.selectbox("Select data source", ["Upload CSV", "Google Sheets URL"])

    # Depending on the source, render appropriate input method
    if source_option == "Upload CSV":
        uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            process_data(data)
    elif source_option == "Google Sheets URL":
        sheet_url = st.text_input("Enter the Google Sheets URL")
        if sheet_url:
            data = read_google_sheets(sheet_url)
            process_data(data)

# Process and display data
def process_data(data):
    if st.button("Generate Random Movie"):
        result = randomize_selection(data)
        st.write("Selected Movie:", result)

if __name__ == "__main__":
    main()
