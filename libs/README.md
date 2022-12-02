# Explanation of the files/modules inside this folder

## 🔨 Structure of files

### 📁 *config.py*
`In these files are all the basic configurations that will be used in the ETL, as well as in the creation of the database, as for example user and password of the database or paths from where the files are extracted for the ETL. All this data is taken from the .env file created in the root of the project`
> **Sample file**

```
# .env example
# Data from the database, in this case postgresql
POSTGRES_USER=user_database
POSTGRES_PASSWORD=password_database
POSTGRES_DB=name_database
POSTGRES_SERVER=host_database(local or cloud)
POSTGRES_PORT=port_database

# Data used for ETL
DATASET_PATH=path_of_data
FOLDER_SAVE_CSV_PATH=path_output_data
```

### 📁 *db.py*
`In this file you will find the necessary to connect to the database, using the ORM SQLAlchemy. Its use is thought to be able to connect to the postgresql database from python and to be able to make different operations, for example ABM type operations.`

### 📁 *models.py*
`This file contains the modeling that the ORM SQLAlchemy performs on the database tables, so that from python we can manipulate the information inside them..`
