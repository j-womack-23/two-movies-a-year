# app.py

import streamlit as st
import pandas as pd
import random

# Randomize the selection
def randomize_selection(df):
    year = random.choice(df['Year'])
    option = random.choice(['Option_J', 'Option_K'])
    selected_option = df.loc[df['Year'] == year, option].values[0]
    return f'{selected_option} ({year})'

# Streamlit GUI
def main():
    st.title("Random Movie Selector")

    uploaded_file = st.file_uploader("Upload your CSV", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        if st.button("Generate Random Movie"):
            result = randomize_selection(data)
            st.write("Selected Movie:", result)

if __name__ == "__main__":
    main()
