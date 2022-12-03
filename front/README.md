# 👑 Streamlit module
----

### ✍ Brief explanation of the module
----
>Module that creates a graphical interface with 3 pages, one to display the company logo and a brief description of it as well as its website. Another one that allows to upload an excel file and apply some filters on it and then download the filtered csv of the table, it also allows to filter the csv obtained from the etl process and thus obtain a specific range of data in a simple way and also with the option to download in csv format the table with the filters applied. Finally the page where 3 graphs are shown one to show the variation of the amounts of transactions with respect to the months of the year, another where you can see the dispersion along with the trend line of the costs with respect to product prices and finally a grouped bar chart where we see how the brands are related to the sales of different types of bicycles that these have.

#### 🗃 Components of module
----

>📁 Pages folder: Here we have two files one for the part of the filters and how they will be displayed on the screen and another with the graphics.

>🐍 home.py: In this file we have the home page where all the information of the company is shown with the logo and this is the one that is responsible for performing the execution of the module.

>🐍 functions.py: Here we have the filtering functions and other necessary functions for the module.

## 👣 Setup
----

>For the execution and implementation of this module you must first run the virtual environment of the module and then install the project dependencies which are found in the requirements.txt file.

Create Virual env with venv name

<code>virtualenv venv</code>

Activate path to activate venv

<code>venv/Scripts/activate</code>

Install requieremts

<code>pip install -r requirements.txt</code>

>After the previous step we must position ourselves inside the module's folder and then run the following script

<code>streamlit run home.py</code>