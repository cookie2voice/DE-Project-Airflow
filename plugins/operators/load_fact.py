from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    load_fact_table_insert = '''
        INSERT INTO {} {}
    '''

    load_fact_table_truncate = '''
        TRUNCATE TABLE {}
    '''

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 # Example:
                 # conn_id = your-connection-name
                redshift_conn_id='',
                table='',
                values='',
                operation='',
                *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        # Example:
        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.values = values
        self.operation = operation

    def execute(self, context):
        self.log.info(f'Started LoadFactOperator {self.table} started with operation {self.operation}')
        redshift_hook = PostgresHook(postgres_conn_id=self.conn_id)
        if self.operation == 'truncate':
            redshift_hook.run(LoadFactOperator.load_fact_table_truncate.format(self.table))
        if self.operation == 'append':
            redshift_hook.run(LoadFactOperator.load_fact_table_insert.format(self.table, self.values))
        self.log.info(f'Ending LoadFactOperator {self.table} with {self.operation} sucess')
