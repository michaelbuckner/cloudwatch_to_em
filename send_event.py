from __future__ import print_function
from config import headers, url, user, pwd
from event import Event
import requests
import json


def send_event(event, context):
    """
    :param event: A JSON representation of the event triggering the Lambda execution.
    :param context: The context of the event trigger.
    """
    # Logging
    print('LOG Log stream name: ', context.log_stream_name)
    print('LOG Log group name: ', context.log_group_name)
    print("LOG Request ID:", context.aws_request_id)
    print("LOG Mem. limits(MB):", context.memory_limit_in_mb)
    # Normalize raw SNS data
    raw_message = json.loads(event['Records'][0]['Sns']['Message'])
    # Get instance ID for node
    instance_id = raw_message['Trigger']['Dimensions'][0]['value']
    # Logging
    print('LOG Function execution start')
    print('LOG SNS Payload: ', raw_message)

    # Check Severity of current event. Use this to open/close events
    if raw_message['NewStateValue'] == 'ALARM':
        severity = '2'
    elif raw_message['NewStateValue'] == 'OK':
        severity = '0'
    # Logging
    print('LOG Severity: ', raw_message['NewStateValue'])

    # Check region associated with event. This will be used to lookup tag info
    if raw_message['Region'] == 'US East - N. Virginia':
        region = 'us-east-1'
    elif raw_message['Region'] == 'US West - N. California':
        region = 'us-west-1'
    else:
        # TODO Add more regions as needed
        print("LOG Error: Region not supported yet")
        exit()

    # Construct an event object
    event = Event(
        instance_id=instance_id,
        region=region,
        alarm_type=raw_message['Trigger']['MetricName'],
        resource=raw_message['Trigger']['Namespace'],
        description=raw_message['Trigger']['MetricName'] + ' ' + raw_message['NewStateReason'],
        severity=severity,
        additional_info=json.dumps(raw_message)
    )

    # Make the HTTP request
    try:
        response = requests.post(url, auth=(user, pwd), headers=headers, data=json.dumps(event.__dict__))
        # Check for HTTP codes other than 201
        if response.status_code != 201:
            print('Error: ', 'Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',
                  response.json())
    except Exception as e:
        print('LOG Error: ', e)
    finally:
        # Log the response
        print('LOG Response: ', response.status_code)
        print("LOG Function execution end")
