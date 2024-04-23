import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
print('let go ')
def lambda_handler(event, context):
    
    ec2_client = boto3.client('ec2')
    print('event_data', event)
    
    if 'detail' not in event :
        return
    
    detail = event['detail']
    if 'instance-id' not in detail and 'state' not in detail:
        return
    
    instance_id = detail['instance-id']
    state = detail['state']
    
    if state == 'running':
        instance = ec2_client.describe_instances(InstanceIds=[instance_id])
        tags = instance['Reservations'][0]['Instances'][0]['Tags']
        
        for tag in tags:
            if tag['Value'] == 'BC-1234':
                create_tag = ec2_client.create_tags(Resources=[instance_id], Tags=[{'Key': 'Environment', 'Value': 'Sandbox'}, {'Key': 'Project', 'Value': 'CDN'}, 
                                                                                   {'Key': 'MachineRole', 'Value': 'EBMachine'}, {'Key': 'Maturity', 'Value': 'Sandbox'}, 
                                                                                   {'Key': 'ChargeCode', 'Value': '00000.AAAAA.99999'}, {'Key': 'Owner', 'Value': 'support@support.com'}])
            elif tag['Value'] == 'BC-5678':
                create_tag = ec2_client.create_tags(Resources=[instance_id], Tags=[{'Key': 'Environment', 'Value': 'Production'}, {'Key': 'Project', 'Value': 'CDN'}, 
                                                                                   {'Key': 'MachineRole', 'Value': 'EBMachine'}, {'Key': 'Maturity', 'Value': 'Production'}, 
                                                                                   {'Key': 'ChargeCode', 'Value': '00000.AAAAA.99999'}, {'Key': 'Owner', 'Value': 'support@support.com'}])
  
    
