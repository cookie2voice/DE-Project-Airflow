from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                redshift_conn_id='',
                tables=[],
                checks=[],
                *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables
        self.checks = checks

    def execute(self, context):
        self.log.info(f'Started DataQualityOperator on tables {self.tables}')
        redshift_hook = PostgresHook(postgres_conn_id=self.conn_id)
        failed_count = 0
        failed_sql = []
        for check in self.checks:
            sql = check.get('check_sql')
            expected_result = check.get('expected_result')
            if redshift_hook.get_records(sql)[0] != expected_result:
                failed_count += 1
                failed_sql.append(sql)
        if failed_count > 0:
            self.log.info(f'Constraint tests failed on {failed_sql}')
        else:
            self.log.info(f'Constraint test passed on {self.tables}')

        self.log.info(f'Ended DataQualityOperator on tables {self.tables}')
