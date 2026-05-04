# Steps to deploy the defined resources to Azure

1. Install and configure terraform if not installed - https://learn.microsoft.com/en-us/azure/developer/terraform/quickstart-configure

2. Install the Azure CLI - https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

3. Define the resources needed in terraform

4. Use the Azure CLI command to set the ARM_SUBSTRICTION_ID environment variable to the ID of our current subscription:
export ARM_SUBSCRIPTION_ID=$(az account show --query "id" --output tsv)

5. Initialize terraform, create an execution plan and apply the plan:
terraform init -upgrade
terraform plan -out main.tfplan -var="runtime_name=python" -var="runtime_version=3.12"
terraform apply main.tfplan

6. Clean up resource if needed:
terraform plan -destroy -out main.destroy.tfplan
terraform apply main.destroy.tfplan

7. After resources are deployed the actual function code can be deployed either from the command line or using a VS Code Azure extension:
    a. Command line option:
        1. https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#create-your-local-project
        2. https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#run-a-local-function
        3. https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local#publish
    
    b. VS Code option:
        1. https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code#create-an-azure-functions-project
        2. https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code#run-functions-locally
        3. https://learn.microsoft.com/en-us/azure/azure-functions/functions-develop-vs-code#republish-project-files
