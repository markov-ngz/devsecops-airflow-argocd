from __future__ import annotations

import os
from datetime import UTC, datetime

from airflow.providers.snowflake.transfers.copy_into_snowflake import (
    CopyFromExternalStageToSnowflakeOperator,
)

from airflow import DAG

SNOWFLAKE_CONN_ID = "my_snowflake_conn"
SNOWFLAKE_STAGE = "stage_name"
SNOWFLAKE_SAMPLE_TABLE = "sample_table"
S3_FILE_PATH = "</path/to/file/sample_file.csv"

ENV_ID = os.environ.get("SYSTEM_TESTS_ENV_ID")
DAG_ID = "example_s3_to_snowflake"


with DAG(
    DAG_ID,
    start_date=datetime(2021, 1, 1, tzinfo=UTC),
    default_args={"snowflake_conn_id": SNOWFLAKE_CONN_ID},
    tags=["example"],
    schedule="@once",
    catchup=False,
) as dag:
    copy_into_table = CopyFromExternalStageToSnowflakeOperator(
        task_id="copy_into_table",
        snowflake_conn_id=SNOWFLAKE_CONN_ID,
        files=[S3_FILE_PATH],
        table=SNOWFLAKE_SAMPLE_TABLE,
        stage=SNOWFLAKE_STAGE,
        file_format="(type = 'CSV',field_delimiter = ';')",
        pattern=".*[.]csv",
    )

if __name__ == "__main__":
    dag.test()
