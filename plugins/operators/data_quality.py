from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                redshift_conn_id='',
                tables=[],
                *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables

    def execute(self, context):
        self.log.info(f'Started DataQualityOperator on tables {self.tables}')
        redshift_hook = PostgresHook(postgres_conn_id=self.conn_id)
        for table in self.tables:
            self.log.info(f'Started DataQualityOperator on table {table}')
            table_records = redshift_hook.get_records(f'SELECT COUNT(*) FROM {table}')
            if len(table_records) < 1 or len(table_records[0]) < 1 or table_records[0][0] < 1:
                raise ValueError(f'Data quality check failed on table {table}')
            else:
                self.log.info(f'Ended DataQualityOperator on {table} with success')