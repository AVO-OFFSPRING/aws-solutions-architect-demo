import json
import boto3

# SAA BEST PRACTICE: Initialize the SDK client OUTSIDE the handler loop.
# When Lambda runs multiple requests consecutively, AWS reuses the container.
# Keeping initialization here speeds up subsequent executions (reduces cold start lag).
dynamodb = boto3.resource('dynamodb') #SDK client for DynamoDB
table = dynamodb.Table('SAA-Demo-Orders') #DynamoDB table resource

def lambda_handler(event, context):
    """
    Main entry point triggered by Amazon API Gateway proxy integration.
    """
    try:
        # 1. API Gateway sends the incoming payload inside the 'body' key as a raw text string.
        # We parse this string back into a functional Python dictionary.
        body = json.loads(event.get('body', '{}'))
        
        # 2. Extract values sent from our frontend app.js script
        extracted_order_id = body.get('orderId')
        extracted_item_name = body.get('itemName')
        
        # 3. Write data to our NoSQL DynamoDB Table.
        # Key fields must perfectly match the database partition key casing ('OrderID').
        table.put_item(
            Item={
                'OrderID': extracted_order_id,
                'ItemName': extracted_item_name
            }
        )
        
        # 4. SAA COMPLIANCE: Web browsers block cross-origin requests unless headers explicitly allow them.
        # Because S3 and API Gateway run on separate URLs, we MUST return these exact CORS response headers.
        return {
            'statusCode': 200,
            'headers': { 
                'Access-Control-Allow-Origin': '*',        # Allows access from any frontend URL (like S3)
                'Access-Control-Allow-Headers': 'Content-Type', # Confirms Content-Type payload is allowed
                'Access-Control-Allow-Methods': 'OPTIONS,POST' # Lists acceptable request methods
            },
            'body': json.dumps({
                'status': 'Success',
                'message': f'Order {extracted_order_id} recorded successfully in AWS!'
            })
        }
        
    except Exception as e:
        # SAA Architecture Note: Any 'print' statement in Python Lambda 
        # is automatically forwarded and logged inside AWS CloudWatch Logs.
        print(f"Server-side failure error exception logged: {str(e)}")
        
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal backend application failure occurred.'})
        }

