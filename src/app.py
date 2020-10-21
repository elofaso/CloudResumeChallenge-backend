import os
import json
import boto3

# Grab data from the environment.
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    db = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = db.Table(TABLE_NAME)
    
    visit_count = None

    try:
        response = table.get_item(Key={
            Key={
                'Id': 1
            }            
        )
        old_visit_count = int(response['Item']['visit_count'])
    except Exception:
        table.put_item(
            Item={
                    'Id':  1,
                    'visit_count': 0
            }
        )
        old_visit_count = 0
        
    new_visit_count = old_visit_count + 1
    
    table.update_item(
        Key={'Id': 1},
        UpdateExpression="set visit_count= :vc",
         ExpressionAttributeValues={
            ':vc' : new_visit_count
        },
    )
    
    return {
        "statusCode": 200,
        "body": json.dumps(new_visit_count)
    }
    
    
