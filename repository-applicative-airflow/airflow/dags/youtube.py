from __future__ import annotations

from airflow.sdk import dag, task


@dag(
    tags=["youtube"],
)
def youtube():
    @task
    def my_task():
        return "Bonjour youtube !"

    my_task()


dag = youtube()

if __name__ == "__main__":
    dag.test()
