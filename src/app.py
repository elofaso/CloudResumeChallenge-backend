import os
import json
import boto3

# Grab data from the environment.
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    
    db = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = db.Table(TABLE_NAME)
    response = table.get_item(
        Key={
            'Id': 1
        },            
        'ConsistentRead': True`
    )
    item = int(response['Item']['visit_count'])
    json_string = json.dumps({'visit_count':int(item)})
    return {
        "statusCode": 200,
        "body": json_string
    }
