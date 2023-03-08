from datetime import datetime, timedelta
# import os
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators import (StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries

# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime(2019, 1, 12),
    'depends_on_past' : False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False,
    'catchup' : False,
}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='@hourly',
          max_active_runs=1
        )

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    redshift_conn_id='redshift',
    table='staging_events',
    s3_key='log-data/{execution_date.year}/{execution_date.month}/{ds}-events.json',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend'
)


stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='Stage_songs',
    dag=dag,
    redshift_conn_id='redshift',
    table='staging_songs',
    s3_key='song-data',
    aws_credentials_id='aws_credentials',
    s3_bucket='udacity-dend'
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songplays',
    aws_credentials_id='aws_credentials',
    table_columns='(playid, start_time, userid, level, songid, artistid, sessionid, location, user_agent)',
    values=SqlQueries.songplay_table_insert,
    truncate=False
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='users',
    aws_credentials_id='aws_credentials',
    table_columns='(userid, first_name, last_name, gender, level)',
    values=SqlQueries.user_table_insert,
    truncate=True
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Load_song_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='songs',
    aws_credentials_id='aws_credentials',
    table_columns='(songid, title, artistid, year, duration)',
    values=SqlQueries.song_table_insert,
    truncate=True
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='artists',
    aws_credentials_id='aws_credentials',
    table_columns='(artistid, name, location, lattitude, longitude)',
    values=SqlQueries.artist_table_insert,
    truncate=True
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    redshift_conn_id='redshift',
    table='time',
    aws_credentials_id='aws_credentials',
    table_columns='(start_time, hour, day, week, month, year, weekday)',
    values=SqlQueries.time_table_insert,
    truncate=True
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id='redshift',
    table=['users', 'songs', 'artists', 'time', 'songplays'],
    checks = [
        {'check_sql': "SELECT COUNT(*) FROM users WHERE userid is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM songs WHERE song_id is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM artists WHERE artist_id is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM time WHERE start_time is null", 'expected_result':0},
        {'check_sql': "SELECT COUNT(*) FROM songplays WHERE userid is null", 'expected_result':0}
   ]
)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)


start_operator >> [stage_events_to_redshift, stage_songs_to_redshift]
stage_events_to_redshift >> load_songplays_table
stage_songs_to_redshift >> load_songplays_table
load_songplays_table >> [load_song_dimension_table, load_user_dimension_table, load_artist_dimension_table, load_time_dimension_table]
load_song_dimension_table >> run_quality_checks
load_user_dimension_table >> run_quality_checks
load_artist_dimension_table >> run_quality_checks
load_time_dimension_table >> run_quality_checks
run_quality_checks >> end_operator
