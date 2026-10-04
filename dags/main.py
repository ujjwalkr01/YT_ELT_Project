from airflow import DAG
import pendulum #used for timezone handling
from datetime import timedelta, datetime
from api.video_stats import get_playlist_id,get_video_ids,extract_video_data,save_to_json

#define local timezone
local_tz = pendulum.timezone("Asia/Kolkata")

#default args:
default_args = {
    "owner": "dataengineers",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "data@engineers.com",
    # "retries" : 1,
    # "retry_delay": timedelta(minutes=5),
    "max_active_runs": 1,
    "dagrun_timeout": timedelta(hours=1),
    "start_date": datetime(2026, 1, 1, tzinfo=local_tz),
    # "end_date": datetime(2026, 12, 31, tzinfo=local_tz),
}

with DAG(
    dag_id="produce_json",
    default_args=default_args,
    description="A DAG to extract video data from a YouTube channel and produce JSON file with raw data",
    schedule="0 14 * * *", # At 14:00 (2 PM) every day
    catchup=False,
)as dag:
    
    #Define the task in the DAG
    playlist_id=get_playlist_id()
    video_ids=get_video_ids(playlist_id)
    extract_data=extract_video_data(video_ids)
    save_to_json_task=save_to_json(extract_data)
    
    #Define the task dependencies
    playlist_id >> video_ids >> extract_data >> save_to_json_task
