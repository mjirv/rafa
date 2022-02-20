# Rafa
_Reasonable Architecture for Analytics_

Rafa is a SQL-based data transformation package.

It allows you to create templated SQL using Python and execute it against your data warehouse to create analytics tables. 

## Usage
1. Run `pip3 install rafa`
2. Run `rafa init hello_world` to create a new Rafa project
3. Run `cd hello_world && rafa run`

## About
Rafa has three components:
1. **Projects** 
    - The DAG of Rafa. A series of tests and transforms to run
    - See `sample_project/project.py`
2. **Transforms** 
    - Similar to dbt models. Files with a `transform()` function that returns a SQL select statement
    - Optionally, they can include a `test(self, rafa)` function that runs any number of unit tests
    - See `sample_project/transforms/`
3. **Functions**
    - Reusable SQL snippets. Similar to a macro in dbt
    - See `sample_project/functions/`

## Configuration
Add connection information in `profiles/.env.default`.
- To specify a different profile, use `rafa run --profile PROFILE_NAME`.
- For example, `rafa run --profile staging` will use `profiles/.env.staging`.

See [sample_project/profiles/.env.default](https://github.com/mjirv/rafa/blob/main/sample_project/profiles/.env.default) for an example including all possible fields.