import json
import logging
import os
from datetime import datetime
from urllib.request import HTTPError, Request, URLError, urlopen

# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def retirement_date(raw_date):
    return datetime.strptime(raw_date, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y-%m-%d')


def standalone_task_message(resources, event):
    '''
    This logic will parse the standalone task event message
    '''

    task_list = ''
    for task in resources:
        task_list += ('\n' + str(task))

    message = str(
        'AWS Fargate tasks will be retired on *' + retirement_date(event['detail']['startTime']) + '*.' +
        '\nThese are standalone tasks, therefore action maybe required to replace them after this date.' +
        '\n\n*Task IDs:* ' + task_list +
        '\n\n<https://phd.aws.amazon.com/phd/home?region=us-east-1#/event-log?eventID=' +
        event['detail']['eventArn'] +
        '|Click here> for details.'
    )
    logging.info(json.dumps(message))

    return message


def service_message(resources, event):
    '''
    This logic will parse the service task event message
    '''

    service_list = ''
    for service in resources:
        service_split = service.split('|')
        service_list += ('\nCluster: _' +
                         service_split[0].rstrip() + '_ Service: _' + service_split[1].lstrip() + '_')

    message = str(
        'AWS Fargate tasks will be retired on *' + retirement_date(event['detail']['startTime']) + '*.' +
        '\nThere are ' + str(len(resources)) + ' ECS services affected. ECS will attempt to start replacement tasks after this date.' +
        '\n\n*Services:* ' + service_list +
        '\n\n<https://phd.aws.amazon.com/phd/home?region=us-east-1#/event-log?eventID=' +
        event['detail']['eventArn'] +
        '|Click here> for details.'
    )
    logging.info(json.dumps(message))

    return message


def lambda_handler(event, context):
    logging.info(json.dumps(event))

    # Check that the required environment variables for Slack have been set. If
    # they have not, then raise an exception.
    required_vars = [
        'SLACK_WORKSPACE_URL',
        'SLACK_CHANNEL'
    ]
    for var in required_vars:
        if not os.environ[var]:
            raise 'Environment variable ' + var + ' not set'

    slack_uri = os.environ['SLACK_WORKSPACE_URL']
    slack_channel = os.environ['SLACK_CHANNEL']

    # Depending on if this task retirement notification is for ECS Services or a
    # Standalone Tasks. We will generate a slack message accordingly.
    resources = event['resources']
    if ':' in resources[0]:
        message = standalone_task_message(resources, event)
    elif '|' in resources[0]:
        message = service_message(resources, event)
    else:
        raise 'Unable to parse affected tasks'

    slack_message = {
        'channel': slack_channel,
        'text': message,
        'username': 'AWS Fargate Task Retirement',
        'icon_emoji': ':warning:'
    }
    logger.info(str(slack_message))

    # Post the message to the Slack channel.
    req = Request(
        slack_uri,
        data=json.dumps(slack_message).encode('utf-8'),
        headers={'content-type': 'application/json'}
    )
    try:
        response = urlopen(req)
        response.read()
        logger.info('Message posted to: %s', slack_message['channel'])
    except HTTPError as e:
        logger.error('Request failed : %d %s', e.code, e.reason)
    except URLError as e:
        logger.error('Server connection failed: %s', e.reason)
