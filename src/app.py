import os
import json
import boto3
import botocore

# Grab data from the environment.
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
TABLE_NAME = os.environ['TABLE_NAME']

def lambda_handler(event, context):
    db = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = db.Table(TABLE_NAME)
    
    visit_count = None

    # Try to get current value of visit_count from db.
    try:
        response = table.get_item(
            Key={
                'Id': 1
            }            
        )
        old_visit_count = int(response['Item']['visit_count'])
    # Create and initialize visit_count in db if item does not exist.
    except KeyError:
        table.put_item(
            Item={
                    'Id':  1,
                    'visit_count': 0
            }
        )
        old_visit_count = 0
    
    # Add 1 to count for current visit.   
    new_visit_count = old_visit_count + 1
    
    # Update visit_count in db to new_vist_count
    table.update_item(
        Key={'Id': 1},
        UpdateExpression="set visit_count= :vc",
         ExpressionAttributeValues={
            ':vc' : new_visit_count
        },
    )
    
    # Return success status code and value of new_visit_count.
    return {
        "statusCode": 200,
        "body": json.dumps(new_visit_count)
    }