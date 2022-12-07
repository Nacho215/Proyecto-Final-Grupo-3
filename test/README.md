# ✅ Tests
----

### ✍ Brief explanation of the module
----
>Modulo en el cual se realizan los test de la aplicacion tendremos 3 secciones de test 2 corresponden a test unitarios y una a test de integracion.

#### 🗃 Components of module
----
>📄  

>✅ test_api.py: aca se realizan los test unitarios de el modulo de api, en especifico se realizan test de los dos endpoint tanto el de lectura de archivos como el de upload, con pruebas tanto con archivos vacios como con archivos con contenido en su interior.

>✅ test_integration.py: en este modlo

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

#### Get all csv processed items

```http
  GET /dataset/get_data
```

#### Uploar xlxs file

```http
  POST /dataset/update
```

|   Parameter  |   Type   | Description                    |
| :--------    | :------- | :----------------------------- |
| `file_objet` |  `file`  | **Required**. Upload xsxl file |


##### 📦 Usage/Examples
-----
>Obtain the url and with these your dataframes

~~~
dats = requests.get('localhost:8000/dataset/get_data')
    # Convert json object into python dict
    dats = dats.json()
    for i in dats:
        # Obtain eachone of paths into dictionary that 
        # will be used to read into read_csv function
        print(pd.read_csv(dats[i]))
~~~