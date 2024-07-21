from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# Import your data processing functions
import logging
from etl_jobs.data_load import download_and_extract_data
from etl_jobs.data_preprocessing import preprocess_data
from etl_jobs.data_transform import process_hard_drive_data
from etl_jobs.data_publish import export_csv_to_rdb, get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define default arguments for your DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define your DAG
dag = DAG(
    'pyspark_etl',
    default_args=default_args,
    description='A simple PySpark ETL DAG',
    schedule_interval=timedelta(days=1),
)

# Define tasks
start = DummyOperator(task_id='start', dag=dag)

# Define input and output directories
raw_data_directory = "../data/raw_data"
preprocess_data_directory = "../data/preprocessed_data"
transform_data_directory = "../data/transformed_data"
db_connection_string = get_db_connection(user_name, password, host, port, database_name)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=download_and_extract_data,
    op_kwargs={'raw_data_directory': raw_data_directory},
    dag=dag,
)

preprocess_data_task = PythonOperator(
    task_id='preprocess_data',
    python_callable=preprocess_data,
    op_kwargs={'input_directory': raw_data_directory, 'output_directory': preprocess_data_directory},
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=process_hard_drive_data,
    op_kwargs={'input_dir': preprocess_data_directory, 'output_dir': transform_data_directory},
    dag=dag,
)

export_data_task = PythonOperator(
    task_id='export_data',
    python_callable=export_csv_to_rdb,
    op_kwargs={'input_dir': transform_data_directory, 'db_connection_string': db_connection_string},
    dag=dag,
)

end = DummyOperator(task_id='end', dag=dag)

# Define task dependencies
start >> load_data_task >> preprocess_data_task >> transform_data_task >> export_data_task >> end