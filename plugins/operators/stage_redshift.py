from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    cpy_query = '''
        COPY {}
        FROM {}
        ACCESS_KEY_ID {}
        SECRET_ACCESS_KEY {}
        compupdate off region 'us-west-2'
    '''

    insert = '''
        INSERT INTO {} {}
    '''

    truncate_query = '''
        TRUNCATE TABLE {}
    '''

    ui_color = '#358140'
    templated_fields = ('s3_key',)

    @apply_defaults
    def __init__(self,
                table='',
                redshift_conn_id='',
                s3_bucket='',
                s3_key='',
                aws_credentials_id='',
                *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.table = table
        self.redshift_conn_id = redshift_conn_id
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.aws_credentials_id = aws_credentials_id

    def execute(self, context):
        self.log.info('Connecting to redshift')
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        self.log.info('Connected with {}'.format(self.redshift_conn_id))

        redshift_hook.run(StageToRedshiftOperator.truncate_query.format(self.table))
        self.log.info("Staging data from s3 to Redshift")
        rendered_key = self.s3_key.format(**context)
        s3_path = 's3://{}/{}'.format(self.s3_bucket, rendered_key)
        stage_sql = StageToRedshiftOperator.cpy_query.format(
            self.table,
            s3_path,
            credentials.access_key,
            credentials.secret_key,
        )
        redshift_hook.run(stage_sql)
