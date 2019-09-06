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
* [Azure Public Client Application](https://docs.microsoft.com/en-us/azure/healthcare-apis/register-public-azure-ad-client-app)
* User account with Microsoft.PolicyInsights/policyStates/triggerEvaluation/action permisssion

## Setup

Ensure the appropriate Python modules are installed.

python azure-policy-evaluate.py --tenantname <TENANTNAME> --clientid <CLIENTID> --subscriptionid <SUB_ID> [--logfile]

