from datetime import datetime, timedelta
from airflow.decorators import dag, task
# from airflow.sensors.external_task import ExternalTaskSensor
from banking_airflow_pipeline.load_mongodb import load_data_into_mongodb
from airflow.utils.email import send_email

default_args = {
    'owner': 'airflow',
    # 'depends_on_past': True,
    'start_date': datetime(2025, 6, 10),
    'email': 'suraj.chaudhary58@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(hours=12)
}

@dag(default_args=default_args,max_active_runs=1, 
     schedule=None, catchup=False, 
     description='Load generated data into MongoDB', 
     tags=['banking_pipeline'])

def dag_load_data_into_mongodb():
    """
    Function to load data from SFTP and local sources into MongoDB.
    This function will load customer, accounts, transactions, credit cards, and credit card transactions data.
    """

    @task
    def load_data_into_mongodb():
        load_data_into_mongodb()

    load_data_into_mongodb()

#reinitialize the DAG
dag_load_data_into_mongodb = dag_load_data_into_mongodb()

