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

Set the following variables in PowerShell:

```powershell
#Adjust these 
$ACR_NAME = "mockclassifieracr"     # e.g., mockclassifieracr123 (no dashes allowed)
$RESOURCE_GROUP = "model-deploy-course-rg" # Change with inholland RG
$IMAGE_NAME = "mock-image-classifier" # you image name ...
$IMAGE_TAG = "latest"
$CONTAINER_APP_NAME = "mock-classifier"
$CONTAINER_ENV_NAME = "mock-classifier-env"
$LOCATION = "westeurope"

$ACR_LOGIN_SERVER = "$ACR_NAME.azurecr.io"
$FULL_IMAGE_NAME = "$ACR_LOGIN_SERVER/$IMAGE_NAME`:$IMAGE_TAG"
```

---

## Step 2 – Build and Tag the Docker Image

```powershell
docker build -t $IMAGE_NAME .
docker tag "${IMAGE_NAME}:${IMAGE_TAG}" $FULL_IMAGE_NAME
```

---

## Step 3 – Push the Image to Azure Container Registry

### Option 1: Using Azure CLI (Recommended)

1. Create the ACR:
```powershell
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic
```

2. Enable admin access:
```powershell
az acr update --name $ACR_NAME --admin-enabled true
```

3. Get credentials:
```powershell
$ACR_USERNAME = (az acr credential show --name $ACR_NAME --query "username" --output tsv)
$ACR_PASSWORD = (az acr credential show --name $ACR_NAME --query "passwords[0].value" --output tsv)
```

4. Login and push:
```powershell
docker login $ACR_LOGIN_SERVER --username $ACR_USERNAME --password $ACR_PASSWORD
docker push $FULL_IMAGE_NAME
```

### Option 2: Using Azure Portal UI

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" > "Containers" > "Container Registry"
3. Fill in the details:
   - Registry name: `$ACR_NAME`
   - Resource group: `$RESOURCE_GROUP`
   - Location: `$LOCATION`
   - SKU: Basic
4. Click "Review + create" then "Create"
5. Once created, go to your registry
6. Under "Settings" > "Access keys", enable "Admin user"
7. Use the provided credentials to login and push your image

---

## Step 4 – Create the Container App Environment

### Option 1: Using Azure CLI (Recommended)

```powershell
az containerapp env create --name $CONTAINER_ENV_NAME --resource-group $RESOURCE_GROUP --location $LOCATION
```

### Option 2: Using Azure Portal UI

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" > "Containers" > "Container Apps Environment"
3. Fill in the details:
   - Environment name: `$CONTAINER_ENV_NAME`
   - Resource group: `$RESOURCE_GROUP`
   - Location: `$LOCATION`
4. Click "Review + create" then "Create"

---

## Step 5 – Deploy the Container App

### Option 1: Using Azure CLI (Recommended)

```powershell
az containerapp create --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --environment $CONTAINER_ENV_NAME --image $FULL_IMAGE_NAME --target-port 5000 --ingress external --registry-server $ACR_LOGIN_SERVER
```

### Option 2: Using Azure Portal UI

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" > "Containers" > "Container App"
3. Fill in the details:
   - App name: `$CONTAINER_APP_NAME`
   - Resource group: `$RESOURCE_GROUP`
   - Container Apps Environment: `$CONTAINER_ENV_NAME`
4. Under "Container" section:
   - Image source: Azure Container Registry
   - Registry: Select your ACR
   - Image: `$IMAGE_NAME`
   - Tag: `$IMAGE_TAG`
5. Under "Ingress" section:
   - Enable ingress: Yes
   - Target port: 5000
   - Traffic: External
6. Click "Review + create" then "Create"

---

## Step 6 – Get the Public URL

### Option 1: Using Azure CLI (Recommended)

```powershell
$FQDN = (az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)
Write-Host "Your app is available at: https://$FQDN"
```

### Option 2: Using Azure Portal UI

1. Go to your Container App in the Azure Portal
2. The URL is displayed in the "Overview" section under "Application URL"

---

## Testing the Deployed API

Once deployed, you can test the API using PowerShell:

```powershell
$FQDN = (az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn --output tsv)
curl.exe -X POST -F "file=@your_image.jpg" "https://$FQDN/predict"
```

The API accepts:
1. Multipart form data with an image file
2. JSON with a base64-encoded image

---

## ✅ Done

Your mock image classifier is now live on Azure Container Apps and ready to accept image uploads for prediction.
