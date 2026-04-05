import json
import boto3

sns = boto3.client('sns')

SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:202606334696:ec2-state-alerts'

def lambda_handler(event, context):
    

    detail = event.get('detail', {})
    
    instance_id = detail.get('instance-id')
    state = detail.get('state')
    
    message = f"""
    EC2 Instance State Change Detected
    
    Instance ID: {instance_id}
    New State: {state}
    """
    
    print(message)
    
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="EC2 State Change Alert"
    )
    
    return {
        "instance_id": instance_id,
        "state": state
    }