import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = 'vol-0da6698869ef41c53'

def lambda_handler(event, context):
    
    # Create snapshot
    description = f"Automated snapshot - {datetime.now(timezone.utc)}"
    
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=description
    )
    
    snapshot_id = snapshot['SnapshotId']
    print(f"Created Snapshot: {snapshot_id}")
    
    # Cleanup old snapshots
    threshold_date = datetime.now(timezone.utc) - timedelta(minutes=5)
    
    response = ec2.describe_snapshots(
        OwnerIds=['self']
    )
    
    deleted_snapshots = []
    
    for snap in response['Snapshots']:
        
        snap_id = snap['SnapshotId']
        start_time = snap['StartTime']
        
        print(f"Checking: {snap_id}, Time: {start_time}")
        
        # Optional safety filter (recommended)
        # if "Automated snapshot" in snap.get('Description', ''):
        
        if start_time < threshold_date:
            print(f"Deleting: {snap_id}")
            
            ec2.delete_snapshot(SnapshotId=snap_id)
            deleted_snapshots.append(snap_id)
    
    print(f"Deleted Snapshots: {deleted_snapshots}")
    
    return {
        "created_snapshot": snapshot_id,
        "deleted_snapshots": deleted_snapshots
    }