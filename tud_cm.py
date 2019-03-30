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

pprint.pprint("You have %i running AWS instances, the Id(s) are:" % (len(myarray)))
for instance in response ['Reservations']:
    print("    "+instance['Instances'][0]['InstanceId'])

UserInterupted = input("How many instances would you like to disrupt?")

shuffled = input("How many times would you like to shuffle the instance order?")

pprint.pprint("Shuffling order to introduce randomness")

for i in range (0, int(shuffled)):
    print("Shuffling")
    random.shuffle(instances)

pprint.pprint("The randomised order is:")
for instance in response ['Reservations']:
    print("    "+instance['Instances'][0]['InstanceId'])




#pprint.pprint(type(instances))

healthBefore = client.describe_instance_status(
    IncludeAllInstances=True
)

RunningAfterCounter = 0
RunningBeforeCounter = 0
InstancesNotRestarted = []

for instanceHealth in healthBefore["InstanceStatuses"]:
    if instanceHealth['InstanceState']['Name'] == "running":
        pprint.pprint("Instance %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['InstanceState']['Name']))
        RunningBeforeCounter += 1
    else:
        pprint.pprint("Instance %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['InstanceState']['Name']))
        InstancesNotRestarted += instanceHealth['InstanceId']


start_time = time.time()

for i in range (0, int(UserInterupted)):
    pprint.pprint("Terminating instance: "+instances[i]['Instances'][0]['InstanceId'])
    #pprint.pprint(client.terminate_instances(InstanceIds=[instances[i]['Instances'][0]['InstanceId']]))
    client.terminate_instances(InstanceIds=[instances[i]['Instances'][0]['InstanceId']])


pprint.pprint("[Start] Timing AWS instances recovery:")
time.sleep(15)

i = 0
progress = "- "
increment = "- "
while RunningBeforeCounter != RunningAfterCounter:
    healthAfter = client.describe_instance_status(
        IncludeAllInstances=True
    )
    RunningAfterCounter = 0

    for instanceHealth in healthAfter["InstanceStatuses"]:
        if instanceHealth['InstanceState']['Name'] == "running":
            pprint.pprint("Instance %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['InstanceState']['Name']))
            RunningAfterCounter += 1
        else:
            pprint.pprint("Instance %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['InstanceState']['Name']))
            InstancesNotRestarted += instanceHealth['InstanceId']

    progress = progress + increment
    if len(progress) > 50:
        elapsed_time = time.time() - start_time
        pprint.pprint("Test of instances recovery failed")
        pprint.pprint("The instances did not recover withing the allowed time")
        pprint.pprint("Timing elapsed: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    print(progress)
    time.sleep(10)

elapsed_time = time.time() - start_time

pprint.pprint("Timing elapsed for recovery from disruption: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))


#for instance in response ['Reservations']:
#    pprint.pprint(client.terminate_instances(InstanceIds=[instance['Instances'][0]['InstanceId']]))