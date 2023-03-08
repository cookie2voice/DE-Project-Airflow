from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    checks = [
        {'check_sql': "SELECT COUNT(*) FROM users WHERE userid is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM songs WHERE song_id is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM artists WHERE artist_id is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM time WHERE start_time is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM songplays WHERE userid is null", 'expected_result':0}
   ]

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
                raise ValueError(f'Valid query results failed on table {table}')
            else:
                self.log.info(f'Valid query results success on {table}')

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
