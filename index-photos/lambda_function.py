import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
import time




def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    reko_client = boto3.client('rekognition')
    
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        print("here")

        response = reko_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            MaxLabels=5
        )
        
        labeldict = {}
        labeldict["objectKey"] = key
        labeldict["bucket"] = bucket
        labeldict["createdTimestamp"] = local_time = time.ctime(time.time())
        labeldict["labels"] = []
        
        for item in response["Labels"]:
            labeldict["labels"].append(item["Name"])
        
        os.system(
            "curl -XPUT -u 'https://vpc-photos-fntfv7yrgxc4zptmna5agsqkqe.us-west-2.es.amazonaws.com' -d " +
            str(labeldict) + " -H 'Content-Type: application/json'"
            )
        print(str(labeldict))

