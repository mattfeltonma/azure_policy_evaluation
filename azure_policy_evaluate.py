import sys
import json
import requests
import logging
import msal
import time
from timeit import default_timer as timer

from argparse import ArgumentParser

# Fixed variables
scope = ['https://management.azure.com//.default']

# Reusable function to create a logging mechanism
def create_logger(logfile=None):

    # Create a logging handler that will write to stdout and optionally to a log file
    stdout_handler = logging.StreamHandler(sys.stdout)
    if logfile != None:
        file_handler = logging.FileHandler(filename=logfile)
        handlers = [file_handler, stdout_handler]
    else:
        handlers = [stdout_handler]

    # Configure logging mechanism
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = handlers
    )

# Obtain access token use device flow
def obtain_access_token(tenantname,scope,client_id):
    logging.info("Attempting to obtain an access token...")
    app = msal.PublicClientApplication(
        client_id = client_id,
        authority='https://login.microsoftonline.com/' + tenantname
    )
    result = None
    
    flow = app.initiate_device_flow(
        scopes=scope
    )

    if "user_code" not in flow:
        logging.error('Unable to generate user code')
        logging.error('Error was: %s',flow['error'])
        logging.error('Error description was: %s',flow['error_description'])
        logging.error('Error correlation_id was: %s',flow['correlation_id'])
        raise Exception('Unable to generate user code to initiate device flow')
    
    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        return result['access_token']

    else:
        logging.error("Authentication failure")
        logging.error("Error was: %s",result['error'])
        logging.error("Error description was: %s",result['error_description'])
        logging.error("Error correlation_id was: %s",result['correlation_id'])
        raise Exception("Unable obtaining access token")

# Main function
def main():
    try:

        # Create logger
        create_logger()

        # Process parameters passed
        parser = ArgumentParser()
        parser.add_argument('--tenantname', type=str, help='Azure AD tenant name')
        parser.add_argument('--clientid', type=str, help='Client ID of application')
        parser.add_argument('--subscriptionid', type=str, help='Subscription ID to run policy assessment')
        args = parser.parse_args()

        # Obtain access token
        access_token = obtain_access_token(tenantname=args.tenantname,scope=scope,client_id=args.clientid)
        
        # Start an evaluation

        logging.info('Initiating policy assessment...')
        headers = {'Content-Type':'application/json', \
        'Authorization':'Bearer {0}'.format(access_token)}
        params = {
            'api-version':'2018-07-01-preview'
        }
        endpoint = f"https://management.azure.com/subscriptions/{args.subscriptionid}/providers/Microsoft.PolicyInsights/policyStates/latest/triggerEvaluation"
        policy_scan = requests.post(url=endpoint,headers=headers,params=params)

        # Check the sattus of the evaluation and report when complete

        if policy_scan.status_code == 202:

            start = timer()
            policy_scan_result = requests.get(url=policy_scan.headers['Location'],headers=headers)
            logging.info('Assessment in progress and waiting for results...')
            while(policy_scan_result.status_code == 202):
                time.sleep(30)
                policy_scan_result = requests.get(url=policy_scan.headers['Location'],headers=headers)
            if policy_scan_result.status_code == 200:
                end = timer()
                logging.info('Policy evaluation succeeded.  Evaluation took ' + str((end-start)/60) + ' minutes.')
            
    except Exception:
        logging.error('Execution error',exc_info=True)

if __name__ == "__main__":
    main()
