from airflow import DAG
from airflow.operators.python_operator import PythonVirtualenvOperator
from loader import ScrapyRunner


from datetime import datetime

default_args = {
    'start_date': datetime(2019, 1, 1)
}

with DAG(dag_id='marketmind_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:

    scrapy_runner = ScrapyRunner(spider_module='us_exchange')

    t1 = PythonVirtualenvOperator(task_id='us_exchange',
                                  python_version='3.6',
                                  requirements='scrapy==2.0.1',
                                  python_callable=scrapy_runner.run_process(),
                                  spider_name='us_exchange')

    t1
