eval $(minikube docker-env)

docker build -t airflow-database-backend:0.1.0 .