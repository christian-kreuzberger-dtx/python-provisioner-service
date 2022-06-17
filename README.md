# Python Provisioner Service

This is a simple Python Provisioner Service for [Keptn's automatic git provisioning](https://keptn.sh/docs/0.16.x/api/git_provisioning/) extension.

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

**Install and Configure Keptn accordingly**
```console
helm upgrade --install keptn keptn/keptn -n keptn --create-namespace --version=0.16.0 \ 
  --set=control-plane.apiGatewayNginx.type=LoadBalancer,control-plane.features.automaticProvisioningURL=http://python-provisioner-service.default
```

**Run using skaffold**
```console
skaffold run --tail
``` 

## How to release a new version of this service

It is assumed that the current development takes place in the `main`/`master` branch (either via Pull Requests or directly).

Once you're ready, go to the Actions tab on GitHub, select Pre-Release or Release, and run the action.


## License

Please find more information in the [LICENSE](LICENSE) file.
