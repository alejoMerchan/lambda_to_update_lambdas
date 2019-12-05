import json
import boto3
import os

awslambda = boto3.client('lambda')
bucket = os.environ['bucket']
config_file = os.environ['config_file']
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    content_object = s3.Object(bucket, config_file)
    file_content = content_object.get()['Body'].read().decode('utf-8')
    json_content = json.loads(file_content)
    lambdas = json_content['lambda_names']
    
    for lambda_name in lambdas:
        print("updating lambda: " + lambda_name)
        result = awslambda.list_event_source_mappings(FunctionName=lambda_name)
        result_json_test = result['EventSourceMappings']
        for result in result_json_test:
            print("updating trigger...")
            a = result['UUID']
            awslambda.update_event_source_mapping(UUID=a,FunctionName=lambda_name,Enabled=True)
    
    return {
        'statusCode': 200,
        'body': json.dumps('update lambdas finished')
    }
