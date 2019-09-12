# Azure Policy On-Demand Evaluation
This Python solution initiates an on-demand Azure Policy evaluation on the specified subscription

## What problem does this solve?
Azure Policy is a service used to enforce governance and compliance in Microsoft Azure.  Evaluation of policy is performed automatically under the circumstances referenced in this [article](https://docs.microsoft.com/en-us/azure/governance/policy/how-to/get-compliance-data).  At this time, initiating an on-demand scan requires a request to the Azure REST API.  

This Python solution can be used to initiate an on-demand scan.  Be aware on-demand evaluations can take anywhere from 5-10 minutes to complete.

## Requirements

### Python Runtime and Modules
* [Python 3.6](https://www.python.org/downloads/release/python-360/)
* [MSAL](https://github.com/AzureAD/microsoft-authentication-library-for-python)

## Azure Requirements
* [Application Registered with Azure AD as Confidential Client](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
* Service principal must be granted Resource Policy Contributor Azure RBAC Role

## Setup

Ensure the appropriate Python modules are installed.

python azure_policy_evaluate.py --tenantname TENANTNAME --clientid CLIENTID --clientsecret CLIENTSECRET --subscriptionid SUB_ID [--logfile]

