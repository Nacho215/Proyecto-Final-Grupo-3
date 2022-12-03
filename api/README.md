# ⚡ FastAPI Module
----

### ✍ Brief explanation of the module
----
>Module in which an api is created, where you can connect the streamlit frontend part with the data files and thus be able to upload files to the project folder directories as well as access the files already processed to view the information in the form of graphs and perform custom filters on them.

#### 🗃 Components of module
----
>📁 Repository folder: here we find the functionality.py file where we make the functionalities that will make the endpoints

>📁 Routers folder: Here we find the enpoints which one returns the paths of the csv files already processed that are inside the outputs folder and the other allows us to upload through it a file to the folder system of the project.

>🐍 Finally we find apiMain.py file where you can run fastAPI server and all your components

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

<code>python apiMain.py</code>

As an extra we leave the endpoints and an example script to obtain the paths of the csv to read them.

- Api swagger Documentation for endpoint testing
  
1. <code>localhost:8000/docs</code>

- Internal paths of processed csv's
  
2. <code>localhost:8000/dataset/get_data</code>

- File upload to the system
  
3. <code>localhost:8000/dataset/update</code>

##### 📦 Example of code to obtain the url and with these your dataframes

~~~
dats = requests.get('localhost:8000/dataset/get_data')
    # Convert json object into python dict
    dats = dats.json()
    for i in dats:
        # Obtain eachone of paths into dictionary that 
        # will be used to read into read_csv function
        print(pd.read_csv(dats[i]))
~~~