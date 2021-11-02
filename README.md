# airflow-docker
Airflow Docker

This project aims to walk through the utilization of airflow with docker, the project is composed by:
1. Create container using Docker and YAML files
2. Declare dependencies between functions
   - first_function_execute
   - second_function_execute
3. Share parameters between functions taking hand from contexts
   - xcom_push: adding values (key, value)
   - xcom_pull: extracting data by key
