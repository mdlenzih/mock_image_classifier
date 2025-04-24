# Deploying the Mock Image Classifier to Azure Container Apps

This guide walks you through deploying the mock image classifier application to Azure using Azure Container Registry (ACR) and Azure Container Apps. The application is a Flask-based API that accepts image uploads and returns mock predictions.

---

## Prerequisites

- Docker installed and running
- Azure CLI installed (`az`)
- Logged in to Azure:  
  az login
- Access to an Azure subscription and an existing resource group

---

## Step 1 – Set Your Variables

For Windows PowerShell users, set the following variables:

```powershell
# e.g., mockclassifieracr123 (no dashes allowed)
$ACR_NAME = "mockclassifieracr"     
$RESOURCE_GROUP = "model-deploy-course-rg"
$IMAGE_NAME = "mock-image-classifier"
$IMAGE_TAG = "latest"
$CONTAINER_APP_NAME = "mock-classifier"
$CONTAINER_ENV_NAME = "mock-classifier-env"
$LOCATION = "westeurope"

$ACR_LOGIN_SERVER = "$ACR_NAME.azurecr.io"
$FULL_IMAGE_NAME = "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"
```

For Linux/Mac users (bash)
(not tested):

```bash
export ACR_NAME=mockclassifieracr     # e.g., mockclassifieracr123 (no dashes allowed)
export RESOURCE_GROUP=model-deploy-course-rg
export IMAGE_NAME=mock-image-classifier
export IMAGE_TAG=latest
export CONTAINER_APP_NAME=mock-classifier
export CONTAINER_ENV_NAME=mock-classifier-env
export LOCATION=westeurope

export ACR_LOGIN_SERVER="$ACR_NAME.azurecr.io"
export FULL_IMAGE_NAME="$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
```

---

## Step 2 – Build and Tag the Docker Image

For Windows PowerShell users:

```powershell
docker build -t $IMAGE_NAME .
docker tag "${IMAGE_NAME}:${IMAGE_TAG}" $FULL_IMAGE_NAME
```

For Linux/Mac users (bash)
(not tested):

```bash
docker build -t $IMAGE_NAME .
docker tag $IMAGE_NAME:$IMAGE_TAG $FULL_IMAGE_NAME
```

---

## Step 3 – Push the Image to Azure Container Registry

Ensure your ACR exists:

For Windows PowerShell users:
```powershell
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
```

For Linux/Mac users (bash)
(not tested):
```bash
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
```

Enable admin access for the registry:
```powershell
az acr update --name $ACR_NAME --admin-enabled true
```

Get the ACR credentials:
```powershell
$ACR_USERNAME = (az acr credential show --name $ACR_NAME --query "username" --output tsv)
$ACR_PASSWORD = (az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)
```

Login to ACR with credentials:
```powershell
docker login $ACR_LOGIN_SERVER --username $ACR_USERNAME --password $ACR_PASSWORD
```

Push the image:
```powershell
docker push $FULL_IMAGE_NAME
```

---

## Step 4 – Create the Container App Environment (Only Once)

For Windows PowerShell users:
```powershell
az containerapp env create --name $CONTAINER_ENV_NAME --resource-group $RESOURCE_GROUP --location $LOCATION
```

For Linux/Mac users (bash)
(not tested):
```bash
az containerapp env create \
  --name $CONTAINER_ENV_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
```

---

## Step 5 – Deploy the Container App

For Windows PowerShell users:
```powershell
az containerapp create --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --environment $CONTAINER_ENV_NAME --image $FULL_IMAGE_NAME --target-port 5000 --ingress external --registry-server $ACR_LOGIN_SERVER
```

For Linux/Mac users (bash)
(not tested):
```bash
az containerapp create \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --environment $CONTAINER_ENV_NAME \
  --image $FULL_IMAGE_NAME \
  --target-port 5000 \
  --ingress external \
  --registry-server $ACR_LOGIN_SERVER
```

---

## Step 6 – Get the Public URL

For Windows PowerShell users:
```powershell
$FQDN = (az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)
Write-Host "Your app is available at: https://$FQDN"
```

For Linux/Mac users (bash)
(not tested):
```bash
az containerapp show \
  --name $CONTAINER_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --query properties.configuration.ingress.fqdn \
  --output tsv
```

---

## Testing the Deployed API

Once deployed, you can test the API using the following endpoints:

1. **Image Upload Endpoint**: `POST https://<your-fqdn>/predict`
   - Accepts multipart form data with an image file
   - Or JSON with a base64-encoded image

Example PowerShell command:
```powershell
$FQDN = (az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)
curl.exe -X POST -F "file=@your_image.jpg" "https://$FQDN/predict"
```

For Linux/Mac users (bash)
(not tested):
```bash
curl -X POST -F "file=@your_image.jpg" https://<your-fqdn>/predict
```

---

## ✅ Done

Your mock image classifier is now live on Azure Container Apps and ready to accept image uploads for prediction.
