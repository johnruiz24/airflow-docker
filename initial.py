try:
    from datetime import timedelta
    from airflow import DAG #scheduler
    from airflow.operators.python_operator import PythonOperator #to execute a python function
    from datetime import datetime
    print("All DAG modules are OK ....")
except Exception as e:
    print("Error {}".format(e))

def first_function_execute():
    print("Hello World")
    return "Hello World"

#arguments (id, schedule interval, default_args(owner,retries,delay,start)
with DAG(
        dag_id="first_dag",
        schedule_interval="@daily",
        default_args={
            "owner":"airflow",
            "retries":1,
            "retry_delay":timedelta(minutes=5),
            "start_date": datetime(2021,1,1)
        },#catchup having false will skip the executions comprised between the current date and start_date in case the initial execution comes from the past
        catchup=False) as f:

    first_function_execute = PythonOperator(
        task_id="first_function_execute",
        python_callable=first_function_execute}
    )

    #next step is to pass data across different functions
