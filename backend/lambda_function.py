import json
import boto3
import os

#Initialize the DynamoDB client outside the handler fumction to leverage execution context
dynamodb = boto3.resource('dynamodb')
