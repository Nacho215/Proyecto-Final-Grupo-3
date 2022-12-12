'''Streamlit is launched from this file

'''

# Imports
import streamlit as st

# Set default configuration for the page
st.set_page_config(
    page_title="Bikes forever store",
    page_icon="🚲",
    layout="wide",
)

# Set a container
body = st.container()

with body:
    st.image("https://i.pinimg.com/550x/2b/1c/5f/2b1c5f11939d2faca9c0b2536f7e7c9e.jpg",width=200,use_column_width=False)
    # Welcome message and descriptions
    st.markdown(
        """
            # Welcome to bike 🚲 forever ♾, where all your biking needs will
            # be satisfied. 🙌

            In this webpage you will be able to:
            * 👉 upload our dataset
            * 👉 filter the dataset according to your needs
            * 👉 graph out the most relevant data available.
            More information at [Bikes Forever](bikesforever.com.ar)

        """
        )

st.text('Fuente: https://www.kaggle.com/datasets/archit9406/customer-transaction-dataset')
