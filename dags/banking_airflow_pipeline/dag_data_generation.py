from airflow.decorators import dag, task
from datetime import datetime, timedelta
# from airflow.sensors.external_task import ExternalTaskSensor
from banking_airflow_pipeline.data_generation import data_generation
# from airflow.utils.email import send_email
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': True,
    'start_date': datetime(2025, 6, 10),
    'email': 'suraj.chaudhary58@gmail.com',
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

@dag(
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    max_active_runs=1,
    description='Generating test data for banking application',
    tags=['banking_pipeline']
)
def dag_banking_data_generation():

    @task(task_id="generate_data")
    def generate_data_task():
        data_generation()

    @task(task_id="send_notification")
    def send_notification():
        """
        Send an email notification after data generation.
        """
        subject = "Data Generation Completed"
        html_content = """
        <h3>Data Generation Completed Successfully!</h3>
        <p>The data generation task has completed successfully.</p>
        """
        send_email(
            to='suraj.chaudhary58@gmail.com',
            subject=subject,
            html_content=html_content
        )

    trigger_postgres=TriggerDagRunOperator(
        task_id='trigger_postgres_dag',
        trigger_dag_id='dag_load_data_into_postgres'
    )

    trigger_mongodb=TriggerDagRunOperator(
        task_id='trigger_mongodb_dag',
        trigger_dag_id='dag_load_data_into_mongodb',
        trigger_run_id='mongodb_run_{{ ts_nodash }}',
        wait_for_completion=False,
        trigger_rule='all_success',  # Ensure this task runs only if the data generation task is successful
        reset_dag_run=True  # Reset the DAG run ID for each execution
        )


    gen=generate_data_task()
    # notify=send_notification()

    gen  >> trigger_postgres >> trigger_mongodb
    



dag_banking_data_generation = dag_banking_data_generation()
