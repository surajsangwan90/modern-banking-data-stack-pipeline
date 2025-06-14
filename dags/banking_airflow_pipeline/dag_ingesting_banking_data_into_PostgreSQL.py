from banking_airflow_pipeline.load_data_from_2Source_into_pg import load_accounts_data_into_pg
from banking_airflow_pipeline.load_data_from_2Source_into_pg import load_transaction_data_into_pg
from banking_airflow_pipeline.load_data_from_2Source_into_pg import load_credit_cards_data_into_pg
from banking_airflow_pipeline.load_data_from_2Source_into_pg import load_credit_card_transactions_data_into_pg
from banking_airflow_pipeline.load_data_from_2Source_into_pg import load_customer_data_into_pg
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.sensors.external_task import ExternalTaskSensor


default_args = {
    'owner': 'airflow',
    # 'depends_on_past': True,
    'start_date': datetime(2025, 6, 10),
    'email': 'suraj.chaudhary58@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

@dag(default_args=default_args, max_active_runs=1 ,
     schedule=None, catchup=False, 
     description='Load data from SFTP and local sources file to PostgreSQL Customers table', tags=['banking_pipeline'])

def dag_load_data_into_postgres():
    """
    Function to load data from SFTP and local sources into PostgreSQL.
    This function will load customer, accounts, transactions, credit cards, and credit card transactions data.
    """
    # wait_for_data_generation = ExternalTaskSensor(
    #     task_id='wait_for_data_generation',
    #     external_dag_id='dag_banking_data_generation_v2',  # The DAG ID of the data generation DAG
    #     external_task_id='generate_data',  # Wait for all tasks in the external DAG
    #     mode='reschedule',  # Use reschedule mode to avoid blocking the scheduler
    #     timeout=300,  # Timeout after 5 minutes if the external task does not complete
    #     poke_interval=30,  # Check every 30 seconds
    # )

    @task
    def load_customer_data():
        load_customer_data_into_pg()
    # load_customer_data()

    @task
    def load_accounts_data():
        load_accounts_data_into_pg()
    # load_accounts_data()

    @task
    def load_transactions_data():
        load_transaction_data_into_pg()
    # load_transactions_data()

    @task
    def load_credit_cards_data():
        load_credit_cards_data_into_pg()
    # load_credit_cards_data()

    @task
    def load_credit_card_transactions_data():
        load_credit_card_transactions_data_into_pg()
    # load_credit_card_transactions_data()


    # Define task dependencies
    customer_task = load_customer_data()
    accounts_task = load_accounts_data()
    transactions_task = load_transactions_data()
    credit_cards_task = load_credit_cards_data()
    credit_card_transactions_task = load_credit_card_transactions_data()

    [customer_task >> accounts_task >> transactions_task >> credit_cards_task >> credit_card_transactions_task]

#instantiate the DAG
dag_load_data_into_postgres = dag_load_data_into_postgres()
