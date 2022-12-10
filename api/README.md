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

>After the previous step we must position ourselves inside the module's folder and then run the following script

```bash
python apiMain.py
```

As an extra we leave the endpoints and an example script to obtain the paths of the csv to read them.

## API Reference

#### Swagger docs

```http
  /docs
```

#### Get all csv processed items into s3 service

```http
  GET /dataset/get_data
```
~~~Output Format
{
  "customers.csv": "outputs/customers.csv",
  "products.csv": "outputs/products.csv",
  "target_customers.csv": "outputs/target_customers.csv",
  "transactions.csv": "outputs/transactions.csv"
}
~~~

#### Uploar xlxs file to local path

```http
  POST /dataset/upload
```

|   Parameter  |   Type   | Description                    |
| :--------    | :------- | :----------------------------- |
| `file_objet` |  `file`  | **Required**. Upload xsxl file |

~~~Return json
{
  "saved": true,
  "local_path": "C:\\Users\\ale\\desktop\\Proyecto-Final-Grupo-3/datasets/KPMG_VI_New_raw_data_update_final.xlsx"
}
~~~

#### Uploar xlxs file to local path

```http
  POST /dataset/upload_s3
```

|   Parameter  |   Type   | Description                    |
| :--------    | :------- | :----------------------------- |
| `file_objet` |  `file`  | **Required**. Upload xsxl file |

~~~Return json
{
  "saved": true,
  "s3_path": "datasets/KPMG_VI_New_raw_data_update_final.xlsx"
}
~~~

#### Get all csv processed items into local path

```http
  GET /dataset/local_path
```
~~~Output Format
{
  "customers": "C:\\Users\\ale\\desktop\\Proyecto-Final-Grupo-3/outputs/customers.csv",
  "products": "C:\\Users\\ale\\desktop\\Proyecto-Final-Grupo-3/outputs/products.csv",
  "target_customers": "C:\\Users\\ale\\desktop\\Proyecto-Final-Grupo-3/outputs/target_customers.csv",
  "transactions": "C:\\Users\\ale\\desktop\\Proyecto-Final-Grupo-3/outputs/transactions.csv"
}
~~~
