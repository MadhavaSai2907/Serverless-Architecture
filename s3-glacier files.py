import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client('s3')

BUCKET_NAME = 's3-glacier-task'

def lambda_handler(event, context):
    
    threshold_date = datetime.now(timezone.utc) - timedelta(days=180)
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    
    if 'Contents' not in response:
        print("Bucket is empty")
        return
    
    archived_files = []
    
    for obj in response['Contents']:
        
        key = obj['Key']
        last_modified = obj['LastModified']
        storage_class = obj.get('StorageClass', 'STANDARD')
        
        if storage_class in ['GLACIER', 'DEEP_ARCHIVE']:
            continue
        
        if last_modified < threshold_date:
            
            print(f"Archiving: {key}")
            
            s3.copy_object(
                Bucket=BUCKET_NAME,
                CopySource={'Bucket': BUCKET_NAME, 'Key': key},
                Key=key,
                StorageClass='GLACIER',
                MetadataDirective='COPY'
            )
            
            archived_files.append(key)
    
    print(f"Archived Files: {archived_files}")
    
    return {
        "archived_files": archived_files
    }