import boto3
import pprint

print("\n")
pprint.pprint("Welcome to TUD Chaos Monkey by Conor Tolan")
print("The following program will intentionally disrupt you AWS instances,")
print("please ensure you are authorised to execute these changes.")

client = boto3.client('ec2')
response = client.describe_instances()
#pprint.pprint(response['Reservations'][0]['Instances'][0].items())
#pprint.pprint(response['Reservations'][0]['Instances'][0])
#pprint.pprint(response['Reservations'][0])
#pprint.pprint(response['Reservations'][1])

pprint.pprint("Your AWS instance Id(s) are:")
for instance in response ['Reservations']:
    pprint.pprint(instance['Instances'][0]['InstanceId'])

pprint.pprint("Terminating your AWS instances:")
for instance in response ['Reservations']:
    pprint.pprint(client.terminate_instances(InstanceIds=[instance['Instances'][0]['InstanceId']]))