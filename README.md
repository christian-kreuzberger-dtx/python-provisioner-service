# Python Provisioner Service

This is a simple Python Provisioner Service for [Keptn's automatic git provisioning](https://keptn.sh/docs/0.16.x/api/git_provisioning/) extension based on Gitea.

## Install

**Pre-requesits**

* Kubernetes cluster
* Keptn

First, we will install gitea in the `gitea` namespace. After that, we will install python-provisioner-service.
### Install Gitea
```console
GITEA_NAMESPACE=gitea
helm repo add gitea-charts https://dl.gitea.io/charts/
helm repo update
helm install -n ${GITEA_NAMESPACE} gitea gitea-charts/gitea --create-namespace \
  --set memcached.enabled=false \
  --set postgresql.enabled=false \
  --set gitea.config.database.DB_TYPE=sqlite3 \
  --set gitea.config.server.OFFLINE_MODE=true \
  --set gitea.config.server.ROOT_URL=http://gitea-http.${GITEA_NAMESPACE}:3000/
```

You can access your gitea installation using
```console
kubectl -n ${GITEA_NAMESPACE} port-forward services/gitea-http 3000:3000
```
on http://localhost:3000

### Install python-provisioner-service

This will install python-provisioner-service into the default namespace

```console
helm install python-provisioner-service https://github.com/christian-kreuzberger-dtx/python-provisioner-service/releases/download/1.0.1-next.0/python-provisioner-service-1.0.1-next.0.tgz
```

**Verify it's installed**
```console
kubectl get pods -l app.kubernetes.io/instance=python-provisioner-service
```

### Configure Keptn to use the python-provisioner-service

This is done by setting `control-plane.features.automaticProvisioningURL` to `http://python-provisioner-service.default` (without trailing slash), e.g.:

```console
helm upgrade --install keptn keptn/keptn -n keptn --create-namespace --version=0.16.0 \ 
  --set=control-plane.apiGatewayNginx.type=LoadBalancer,control-plane.features.automaticProvisioningURL=http://python-provisioner-service.default
```


## Development

**Create a Python 3 virtual environment**
```console
virtualenv -p python3 venv
```

**Activate virtual environment**
```console
source venv/bin/activate
```

**Develop**

## Running on Kubernetes

**Run using skaffold**
```console
skaffold run --tail
``` 
## How to release a new version of this service

It is assumed that the current development takes place in the `main`/`master` branch (either via Pull Requests or directly).

Once you're ready, go to the Actions tab on GitHub, select Pre-Release or Release, and run the action.

## License

Please find more information in the [LICENSE](LICENSE) file.
