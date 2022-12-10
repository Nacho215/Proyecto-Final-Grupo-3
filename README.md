# 🚲 Ecommerce Bikes data project
----

<div align="center" width="50">

<img src="https://i.pinimg.com/550x/2b/1c/5f/2b1c5f11939d2faca9c0b2536f7e7c9e.jpg" alt="ForeverBicycles" width="300"/>

</div>

# 🎯 Objectives
The general objectives set out in the project are:
- Develop a python application that performs an ETL starting from a plain text file (.csv) to a relational database (PostgreSQL).
- Develop an API with a graphical interface for the use of the application from python that performs ETL.
- Develop functionalities that allow transformations, ABM and queries against a relational database.
- Develop tests on the developed python application.
- Design and develop a dashboard in MicroStrategy that consumes data from a relational database.
# 📈 Dataset
Chosen dataset contains data about Sprocket Central Pty Ltd (a medium size bikes & cycling accessories organization), its transactions, customers and prodcuts.

The Dataset can be downloaded here:

🔗[Customer transactions dataset](https://www.kaggle.com/datasets/archit9406/customer-transaction-dataset)

# 📁Files structure
## Folders
- ***api***: internal files structure needed to launch FastAPI library (used to communicate Python scripts with Streamlit WebApp interface).
- ***front***: WebApp interface related files (Streamlit).
- ***libs***: Python libraries (modules) used in the project.
- ***logs***: Logs files that record different events during the program execution.
- ***notebooks***: Jupyter notebook with an EDA explaining the nature of the dataset.
- ***database***: contains a SQL script (for tables generation), an ERD (entity-relation diagram) and the documentation associated to the database.
- ***src***: contains source files (Python scripts).
## Files
- ***.gitignore***: list with intentionally untracked files.
- ***config_logs.conf***: logger configuration file.
- ***requirements.txt***: dependencies needed for this project.

# 🔨 Setup
First, create a virtual enviroment called 'venv' for this project:
```
python -m venv venv
```
Activate it (this command can be different for each OS):
```
source venv/Scripts/activate
```
Then install dependencies from requirements file:
```
pip install -r requirements.txt
```
And run main script:
```
cd src
python main.py
```

## 📄 Index
----
> Through this idice you can go directly to the module you want to see how it works and execute it separately through its instructions.

1 - [FastAPI](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/api)

2 - [Streamlit - Fron End](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/front)

3 - [Database connections and management - Configurations - Templates - Models](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/libs)

4 - [EDA - Insight Queries](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/notebooks)

5 - [Main Project execution](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/src)

6 - [Tests](https://github.com/Nacho215/Proyecto-Final-Grupo-3/tree/main/test)

# 🚀 Team
- Chen, Isaac
- Gomez, Alejandro
- Hernández, Juan Ignacio 
- Lujan, Ricardo
- Montaña, Carlos

