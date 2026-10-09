# Kubernetes cluster setup

1. Starting minikube
```shell
minikube start --memory=8192 --cpus=3
```
2. Create base namespaces
```sh
kubectl apply -f kubernetes/namespace.yaml
```
3. Create base airflow secrets for each env
```sh
kubectl create secret generic airflow-git-conn-secret \
  --namespace dev-airflow-core \
  --from-literal=AIRFLOW_CONN_GIT_REPO_CONN='{ "conn_type": "git", "host": "https://github.com/markov-ngz/devsecops-lab-airflow.git", "login": "markov-ngz", "password": "<PAT>" }'
kubectl create secret generic airflow-redis-secret \
  --namespace dev-airflow-core \
  --from-literal=password='<STRONG_RANDOM_PASSWORD>'

kubectl create secret generic airflow-broker-url-secret \
  --namespace dev-airflow-core \
  --from-literal=connection='redis://:<STRONG_RANDOM_PASSWORD>@airflow-redis:6379/0'
  
# fernet key 
FERNET_KEY=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
kubectl create secret generic airflow-fernet-key \
  --namespace dev-airflow-core \
  --from-literal=fernet-key=${FERNET_KEY}
```
4. Add ArgoCD git secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: repo-config
  namespace: argocd
  labels:
    argocd.argoproj.io/secret-type: repository
stringData:
  type: git
  url: git@github.com:markov-ngz/devsecops-lab-gitops.git
  sshPrivateKey: |
    <key>
```
5. Install argocd helm chart
```sh 
HELM_CHART_VERSION="10.9.0"

helm install argocd argo/argo-cd --version "${HELM_CHART_VERSION}" \
--namespace argocd \
-f kubernetes/argocd/install/argocd-helm-values.yaml
```
6. Retrieve Password
```sh 
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
7. Open another shell and forward argocd service
```sh 
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
8. Login with init password and change it
```sh 
argocd login localhost:8080 \
--password $(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d) \
--username admin \
--insecure

argocd account update-password
```
9. Deploy base applications which will trigger full deployment !
```sh 
kubectl apply -f kubernetes/argocd/projects/appproject-argocd.yaml
kubectl apply -f bootstrap-argocd/app-root-project.yaml
kubectl apply -f bootstrap-argocd/app-root.yaml
```