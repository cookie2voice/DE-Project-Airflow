from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'

    load_dimention_table_insert = '''
        INSERT INTO {} {} VALUES {}
    '''

    load_dimention_table_truncate = '''
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

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.values = values
        self.truncate = truncate
        self.table_columns = table_columns

    def execute(self, context):
        self.log.info(f'Started LoadDimensionOperator {self.table} started with truncate {self.truncate} ')
        redshift_hook = PostgresHook(postgres_conn_id=self.conn_id)
        if self.truncate:
            self.log.info(f'Truncate-append mode')
            redshift_hook.run(LoadDimensionOperator.load_dimention_table_truncate.format(self.table))
            redshift_hook.run(LoadDimensionOperator.load_dimention_table_insert.format(self.table, self.table_columns, self.values))
        else:
            self.log.info(f'Append mode only')
            redshift_hook.run(LoadDimensionOperator.load_dimention_table_insert.format(self.table, self.table_columns, self.values))
        self.log.info(f'Ending LoadDimensionOperator {self.table} with truncate {self.truncate} sucessfully')