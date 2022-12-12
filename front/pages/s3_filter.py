'''To create filters to process datasets in csv processed in s3 service

Receives:
list of url to download csv of s3 service

Returns:
cleaned and processed tables
'''

# Imports
from functions import filter_dataframe, s3_csv_downloader
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Forever filters",
    page_icon="🚲",
    layout="wide",
)

#set up containers to work in 
header = st.container()

# Get root project root
rootPath = Path(__file__).parent.parent.parent

# title
with header:
    st.title('🚲 Bikes forever store')

# If outputs path not exists so clean cache memory to s3:csv function downloader download
# the csv files of s3 service
if not (Path(__file__).parent.parent.parent/'outputs').exists():
    st.experimental_singleton.clear()

# exexute function that download csv files if files had been downloaded so continue with 
# next lines and flag would be true
flag = s3_csv_downloader()
if flag:
    # If flag is True continue the process and mean that csv file had been downloaded
    dataset_local_path = f'{Path(__file__).parent.parent.parent}/outputs'
    output_dir = f'{rootPath}/outputs'
    output_dir = Path(output_dir)

    file_names = []
    
    st.text("Look into ETL modified Files")
    file_container = st.expander("ETL Modified csv files")
    # Loop which gets each of the paths from the address
    # stored in the output_dir variable
    for i in output_dir.iterdir():

        file_container.write(pd.read_csv(i))
        file_names.append(f"{i.name}")
        # displays filtered dataframe on screen

    st.write("Filter tables:")

    # Select name of table to aply filers
    df_option = st.selectbox('Select table', file_names)
    st.write(df_option)
    for index, name in enumerate(file_names):
        # If selection is equal to the actual name in the list of names use it to 
        # create path to extract information of csv file to make the filter
        if df_option == file_names[index]:
            df_filtered = filter_dataframe(pd.read_csv(f"{dataset_local_path}/{name}"))
            st.dataframe(df_filtered)
            st.download_button('Download file', data=df_filtered.to_csv(), file_name=name)
else:
    st.write("File can´t be downloaded")
