import boto3
import time
import pprint
import numpy as np
import random
import json
from random import shuffle


print("\n")
pprint.pprint("Welcome to TUD Chaos Monkey by Conor Tolan")
print("The following program will intentionally disrupt you AWS instances,")
print("please ensure you are authorised to execute these changes.")
print("\n")

client = boto3.client('ec2')
response = client.describe_instances(
    Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        },
    ],
)

#pprint.pprint(response['Reservations'][0]['Instances'][0].items())
#pprint.pprint(response['Reservations'][0]['Instances'][0])
#pprint.pprint(response['Reservations'][0])
#pprint.pprint(response['Reservations'][1])
#responseJson = json.dumps(responseDict)
#responseObj = json.loads(responseJson)

instances = response ['Reservations']
myarray = np.asarray(instances)

pprint.pprint("You have %i AWS instances, the Id(s) are:" % (len(myarray)))
for instance in response ['Reservations']:
    pprint.pprint("    "+instance['Instances'][0]['InstanceId'])

pprint.pprint("Shuffling order to introduce randomness")
shuffled = input("How many times would you like to shuffle the instance order?")

for i in range (0, int(shuffled)):
    print("Shuffling")
    random.shuffle(instances)

for instance in response ['Reservations']:
    pprint.pprint("    "+instance['Instances'][0]['InstanceId'])


UserInterupted = input("How many instances would you like to disrupt?")


#pprint.pprint(type(instances))

healthBefore = client.describe_instance_status(
    IncludeAllInstances=True
)

for instanceHealth in healthBefore:
    pprint.pprint(instanceHealth['InstanceStatuses']['InstanceState']['Name'])

for i in range (0, int(UserInterupted)):
    pprint.pprint("Terminating instance id"+instances[i]['Instances'][0]['InstanceId'])
    pprint.pprint(client.terminate_instances(InstanceIds=[instances[i]['Instances'][0]['InstanceId']]))



pprint.pprint("Please wait will wait for AWS instances to restart:")
time.sleep(15)

healthAfter = client.describe_instance_status(
    IncludeAllInstances=True
)

NewResponse = ""

for instanceHealth in healthAfter:
    pprint.pprint(instanceHealth['InstanceStatuses']['InstanceState']['Name'])

while len(response) != len(NewResponse):
    pprint.pprint("Checking for new AWS instances:")
    healthAfter = client.describe_instance_status(
        IncludeAllInstances=True
    )
    NewResponse = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
        ],
    )
    print("Instances running: "+str(len(NewResponse)))

    pprint.pprint("Current instances:")
    for instance in NewResponse ['Reservations']:
        pprint.pprint("    "+instance['Instances'][0]['InstanceId'])

    time.sleep(15)


#for instance in response ['Reservations']:
#    pprint.pprint(client.terminate_instances(InstanceIds=[instance['Instances'][0]['InstanceId']]))