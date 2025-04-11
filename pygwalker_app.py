import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html

# Adjust the width of the Streamlit page
st.set_page_config(page_title="Use Pygwalker In Streamlit", layout="wide")

# Properly formatted file path (use double backslashes or raw string)
file_path = r"C:\Users\iao\Desktop\Patstat_TIP\Patent_family\applicants_inventors_analyse\dataTable_NO_2020_2020\data\applicants_inventors\combined_counts.csv"

# Load your data
try:
    df = pd.read_csv(file_path)
    st.write("Data loaded successfully!")
    st.write("Preview of the data:")
    st.dataframe(df.head())

    # Initialize pygwalker communication
    init_streamlit_comm()

    # Get the HTML for the pygwalker chart
    html = get_streamlit_html(
        df,
        spec="./gw_config.json",
        use_kernel_calc=True,
        theme="media",
        dark_mode=False,
    )

    # Display pygwalker
    st.components.v1.html(html, height=800)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.write("Please check if your file path is correct.")
