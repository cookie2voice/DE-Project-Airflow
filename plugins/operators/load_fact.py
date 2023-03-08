from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    load_fact_table_insert = '''
        INSERT INTO {} {} VALUES {}
    '''

    load_fact_table_truncate = '''
        TRUNCATE TABLE {}
    '''

    @apply_defaults
    def __init__(self,
                redshift_conn_id='',
                table='',
                values='',
                truncate=False,
                table_columns='',
                *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.values = values
        self.truncate = truncate
        self.table_columns = table_columns

    def execute(self, context):
        self.log.info(f'Started LoadFactOperator on table {self.table} with truncate {self.truncate}')
        redshift_hook = PostgresHook(postgres_conn_id=self.conn_id)
        if not self.truncate:
            self.log.info(f'Append mode only')
            redshift_hook.run(LoadFactOperator.load_fact_table_insert.format(self.table, self.table_columns, self.values))
        else:
            self.log.info(f'Truncate-append mode')
            redshift_hook.run(LoadFactOperator.load_fact_table_truncate.format(self.table, self.values))
            redshift_hook.run(LoadFactOperator.load_fact_table_insert.format(self.table, self.table_columns, self.values))
        self.log.info(f'Ending LoadFactOperator {self.table} with truncate {self.truncate} successfully')
