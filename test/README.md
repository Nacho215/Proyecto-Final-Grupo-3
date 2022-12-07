# ✅ Tests
----

### ✍ Brief explanation of the module
----
>Module in which the application tests are performed, we will have 3 test sections, 2 correspond to unit tests and one to integration tests.

#### 🗃 Components of module
----
>🗃 htmlcov: folder with the index.html file containing the percentage of coverage of the folder's codes

>🗃 test_doc: folder containing all the txt files with the log of the execution of each test module.

>✅ test_api.py: here the unit tests of the api module are performed, specifically tests of the two endpoints are performed, both the file reading and upload, with tests with empty files as well as with files with content inside.

>✅ test_integration.py: in this one we test the load function of the etl that what it does is to load the csv to s3 and the database to rds, this function makes integration tests since load integrates executions of practically all the etl so the percentage of coverage is of 100% in this.

> ✅ test_unitest_etl.py: module that tests etl functions in a unitary way.

## 👣 Installation
----

>To run the tests of this module we first activate the virtual environment and install the requirements.txt dependencies.

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

>After this, what we must do is to execute the tests, which we can do individually or globally all at once. Always located on the folder test we execute the commands

##### We run all tests in the folder together

```bash
pytest -v .
```
##### We run each test separately

```bash
pytest -v ./test_archivo.py
```
