import boto3

client = boto3.client('autoscaling')

response = client.update_auto_scaling_group(
    AutoScalingGroupName='CM_ASG',
    MinSize=3,
    MaxSize=6
)

response = client.set_desired_capacity(
    AutoScalingGroupName='CM_ASG',
    DesiredCapacity=3,
    HonorCooldown=False
)
