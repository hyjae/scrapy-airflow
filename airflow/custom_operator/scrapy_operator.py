from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults
from loader import ScrapyRunner
from airflow.exceptions import AirflowException


class ScrapyOperator(BaseOperator):

    @apply_defaults
    def __init__(self,
                 spider_name: str,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.spider_name = spider_name

    def execute(self, context):
        if not ScrapyRunner(self.spider_name):
            raise AirflowException("You have an error!")
