import json
import boto3
from boto3.dynamodb.conditions import Key # this is used for the DynamoDB Table Resource

TABLE_NAME = "cloud-resume-visitor-count"  # Used to declare table 
# Creating the DynamoDB Client
dynamodb_client = boto3.client('dynamodb', region_name="us-east-1")

# Creating the DynamoDB Table Resource
dynamodb_table = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb_table.Table(TABLE_NAME)

# Use the DynamoDB Table update item method to increment item
def lambda_handler(event, context):
    response = table.get_item(
        TableName =TABLE_NAME,
        Key={
            "visitor":'VisitorCount',
        }
        )
    item = response['Item']

    table.update_item(
        Key={
            "visitor":'VisitorCount',
        },
        UpdateExpression='SET visitor_counter = :val1',
        ExpressionAttributeValues={
            ':val1': item['visitor_counter'] + 1
        }
    )
    return{
      "body":{"Visit_Count": str(item['visitor_counter'] + 1)}
    }