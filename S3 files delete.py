import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 'lambda-s3-assignment'

def lambda_handler(event, context):
    
    threshold_date = datetime.now(timezone.utc) - timedelta(days=30)
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' not in response:
        print("Bucket is empty")
        return
    
    deleted_files = []
    
    for obj in response['Contents']:
        
        file_name = obj['Key']
        last_modified = obj['LastModified']
        
        if last_modified < threshold_date:
            
            s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)
            deleted_files.append(file_name)
    
    print(f"Deleted Files: {deleted_files}")
    
    return {
        'statusCode': 200,
        'body': f"Deleted {len(deleted_files)} files"
    }