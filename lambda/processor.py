import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    client = boto3.client('sagemaker-runtime')
    anomalies = []
    
    for record in event['Records']:
        payload = json.loads(record['kinesis']['data'])
        
        # Anomaly detection
        response = client.invoke_endpoint(
            EndpointName=os.environ['SAGEMAKER_ENDPOINT'],
            ContentType='application/json',
            Body=json.dumps(payload)
        )
        
        if json.loads(response['Body'].read())['is_anomalous']:
            anomalies.append(payload)
            
    if anomalies:
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:alerts',
            Message=json.dumps({'anomalies': anomalies})
        )