eval $(minikube docker-env)

docker build -t markreduce/airflow-database-backend:0.1.0 .
