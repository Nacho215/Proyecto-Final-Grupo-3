# 👑 Streamlit module
----

### ✍ Brief explanation of the module
----
>Module that displays 5 pages one called home that shows the basic info of the company, another local uploader that uploads locally an xlsx file and allows us to filter it and download the filtered table, another one called s3 filter that applies filters on csv files already preprocessed stored inside the outputs folder of an amazon s3 service, s3 uploader which allows us to upload a file to s3 with previous visualization to see what data it contains and then confirm its upload, finally we have the graphs page where we will see the 3 most significant graphs of the etl csv where we can if we can not visualize them download them locally so we can see their graphs.

#### 🗃 Components of module
----

>📁 Pages folder: Here we have the pages of graphics, upload file to s3, apply filters to csv from s3 and upload file locally and visualize the filters with the possibility to download them..

>🐍 home.py: In this file we have the home page where all the information of the company is shown with the logo and this is the one that is responsible for performing the execution of the module.

>🐍 functions.py: Here we have the filtering functions and other necessary functions for the module.

## 👣 Installation
----

>For the execution and implementation of this module you must first run the virtual environment of the module and then install the project dependencies which are found in the requirements.txt file.



##### Create Virual env with venv name

```bash
virtualenv venv
```

##### Activate path to activate venv

```bash
venv/Scripts/activate
```

##### Install requieremts

```bash
pip install -r requirements.txt
```

### Until you run streamlit you will need to activate api with instruction into api readme in the [api folder](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/api)

>After the previous step we must position ourselves inside the module's folder and then run the following script

```bash
streamlit run home.py
```