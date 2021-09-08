try:
    from datetime import timedelta
    from airflow import DAG #scheduler
    from airflow.operators.python_operator import PythonOperator #to execute a python function
    from datetime import datetime
    import pandas as pd
    print("All DAG modules are OK ....")
except Exception as e:
    print("Error {}".format(e))

#passing data between functions through a context
def first_function_execute(**context):
    print('first_function_execute ')
    #pushing the data
    context['ti'].xcom_push(key='mykey', value="first_function_execute says Hello")

def second_function_execute(**context):
    #grabbing the key which is ti
    instance = context.get('ti').xcom_pull(key='mykey')
    data = [{"name":"John Ruiz", "title":"systems engineering"}, {"name":"Francilene Francisco", "title":"SAP Consultant"}, {"name":"Ricardo Rei", "title":"Text Mining Professor"}]
    df = pd.DataFrame(data=data)
    print('@'*20)
    print(df)
    print('@'*20)
    print(f'I am in second_function_execute got value: {instance} from function 1')

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
        python_callable=first_function_execute,
        #next step will be: how you can write multiple functions and share data across those and give query parameters to that
        #adding op_kwargs to give & pass query parameters
        provide_context=True,
        op_kwargs={"name":"John Ruiz"}
    )

    second_function_execute = PythonOperator(
        task_id='second_function_execute',
        python_callable=second_function_execute,
        #enabling the flag to share data across functions
        provide_context=True
    )
    #next step is to pass data across different functions

#as the second function depends on the first we might write this dependency
first_function_execute >> second_function_execute
