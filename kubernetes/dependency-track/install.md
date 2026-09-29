```sh 
curl -fsSL https://raw.githubusercontent.com/DependencyTrack/helm-charts/main/KEYS | gpg --import
gpg --export dependencytrack+helm@owasp.org > /tmp/dependencytrack-keyring.gpg 

helm pull oci://ghcr.io/dependencytrack/helm-charts/dependency-track \
  --prov --verify --keyring /tmp/dependencytrack-keyring.gpg
  
tar -xvf dependency-track-2.5.0.tgz
rm dependency-track-2.5.0.tgz

echo dependency-track >> .gitignore

kubectl -n security-dependency-track port-forward svc/dependency-track-api-server 8080:8080 &
kubectl -n security-dependency-track port-forward svc/dependency-track-frontend 8081:8080 &
```