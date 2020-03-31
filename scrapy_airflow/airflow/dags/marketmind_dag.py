from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1)
}

with DAG(dag_id='marketmind_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    t_1_ssd = BashOperator(task_id='us_exchange', bash_command='echo "I/O intensive task"')

    t_1_ssd