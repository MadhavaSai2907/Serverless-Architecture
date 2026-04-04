import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    
    response = ec2.describe_instances()
    
    stop_instances = []
    start_instances = []
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            
            instance_id = instance['InstanceId']
            
            if 'Tags' in instance:
                for tag in instance['Tags']:
                    
                    if tag['Key'] == 'Action':
                        
                        if tag['Value'] == 'Auto-Stop':
                            stop_instances.append(instance_id)
                            
                        elif tag['Value'] == 'Auto-Start':
                            start_instances.append(instance_id)
    
    if stop_instances:
        ec2.stop_instances(InstanceIds=stop_instances)
        print(f"Stopped Instances: {stop_instances}")
    
    if start_instances:
        ec2.start_instances(InstanceIds=start_instances)
        print(f"Started Instances: {start_instances}")
    
    return {
        'statusCode': 200,
        'body': 'EC2 instances managed successfully'
    }