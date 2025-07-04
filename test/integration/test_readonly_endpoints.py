import os
import boto3
import time
import uuid
import json
import functools
from botocore.exceptions import ClientError


def get_table(dynamodb=None):
    if not dynamodb:
        URL = os.environ['ENDPOINT_OVERRIDE']
        if URL:
            print('URL dynamoDB:'+URL)
            boto3.client = functools.partial(boto3.client, endpoint_url=URL)
            boto3.resource = functools.partial(boto3.resource,
                                               endpoint_url=URL)
        dynamodb = boto3.resource("dynamodb")
    # fetch todo from the database
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    return table


def get_item(key, dynamodb=None):
    table = get_table(dynamodb)
    try:
        result = table.get_item(
            Key={
                'id': key
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Result getItem:'+str(result))
        if 'Item' in result:
            return result['Item']


def get_items(dynamodb=None):
    table = get_table(dynamodb)
    # fetch todo from the database
    result = table.scan()
    return result['Items']
