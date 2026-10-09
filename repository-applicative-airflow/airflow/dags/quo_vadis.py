from __future__ import annotations

from airflow.sdk import dag, task


@dag(
    tags=["example"],
    params={"miasto": "Gdańsku"},
)
def quo_vadis():
    @task
    def my_task(city):
        return f"Pracuję w {city}"

    my_task("{{ params['miasto'] }}")


dag = quo_vadis()

if __name__ == "__main__":
    dag.test(run_conf={"miasto": "Poznaniu"})
