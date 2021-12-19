# Showcase API
A showcase API for job applications

## Local development setup

### Install Python dependencies
Run the following to install project dependencies

``` bash
pip install requirements.txt
```

Optionally, install dev packages to assist development

``` bash
pip install requirements_dev.txt
```

### Add auth token environment variable
Add an authentication token as an OS environment variable.  This token will be used to authenticate users in the API.

``` bash
export API_AUTH_TOKEN=myChosenToken
```

### Run local server
Run the api by navigating to the `app` directory and running the following command:

``` bash
uvicorn main:app --reload
```

### Test endpoints
Endpoints can be found by navigating to `localhost:8000/docs`. Ensure the auth_token provided in requests matches the value set in API_AUTH_TOKEN.

### Dockerisation
This API can be run in a docker container by navigating to the project's root directory, then running:

``` bash
docker build -t showcase-api . && docker run --name showcase
-api -p 80:8000 -d -e API_AUTH_TOKEN=$API_AUTH_TOKEN --rm showcase-api
```

The API can be queried as above.

To stop the dockerised API, run:

``` bash
docker stop showcase-api
```

## Deployment
Deployment of the API assumes the following is set up:
- A kubernetes cluster
- A docker repository accessible from the cluster
- kubectl on the deployer's machine, configured to connect to the k8s cluster

### Build the API as a docker image
Build the API's docker image and tag it to include your docker repository URL (DockerRepoURL here).  Navigate to the project's root directory and run:

``` bash
docker build -t <DockerRepoURL>/showcase-api .
```

### Push the API docker image to the docker repository
Ensure you are authenticated with the remote docker repository then run:

``` bash
docker push <DockerRepoURL>/showcase-api
```

### Create a k8s namespace
``` bash
kubectl create namespace showcase-api
```

### Create docker credential secret
Create a secret containing the URL, username, and password of the docker repository to which the API's image was pushed earlier.

``` bash
kubectl create secret docker-registry regcred --docker-server=<DockerRepoURL> --docker-username=<username> --docker-password=<password> -n showcase-api
```

### Create API auth token secret
Create a secret containing the API auth token.

``` bash
kubectl create secret generic api_auth_token_secret --from-literal=auth_token=$API_AUTH_TOKEN -n showcase-api
```

### Create the k8s deployment
Edit the `api_deployment.yaml` deployment file to change the image name to match that which was pushed earlier.

``` bash
kubectl create -f api_deployment.yaml
```

### Create the k8s loadbalancer service
Run the following command to create a loadbalancer service for the showcase API.

Beware: depending on the cluster's configuration, port 80 may not be available. If the creation command below returns an error to this effect, choose a different port.

Also beware: if deploying to Azure and its region has a duplicate DNS record to the one defined in the loadbalancer yaml (in this case 'showcase-api'), then the record will not be created.  Check the Azure logs if the URL is inaccessible.

``` bash
kubectl create -f api_loadbalancer.yaml
```

Once created, you can find the application's IP under 'EXTERNAL-IP' after running this command:

``` bash
kubectl get service showcase-api-service -n showcase-api
```

If deploying to Azure, you can also access the API at the following URL (changing 'uksouth' to the relevant deployment region if necessary)
showcase-api.uksouth.cloudapp.azure.com

### Test the API endpoints
Test the endpoints by querying the IP and/or the URL identified during the loadbalancer creation step.

## Jenkins pipeline
A Jenkinsfile is contained in this codebase to provide a basic Python scanning pipeline.
