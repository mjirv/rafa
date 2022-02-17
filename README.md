# Rafa
_Reasonable Architecture for Analytics_

Rafa is a SQL-based data transformation package.

It allows you to create templated SQL using Python and execute it against your data warehouse to create analytics tables. 

## Usage
1. Run `pip3 install rafa`
2. Copy the files from `sample_project/` to get started
3. Run `python3 project.py`

## About
Rafa has three components:
1. **Projects** 
    - The DAG of Rafa. A series of transforms to run against your database
    - See `sample_project/project.py`
2. **Transforms** 
    - Similar to dbt models. Files with a `transform()` function that returns a SQL select statement
    - See `sample_project/transforms/`
3. **Functions**
    - Reusable SQL snippets. Similar to a macro in dbt
    - See `sample_project/functions/`

