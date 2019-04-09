import boto3
import time
import sys
import pprint
import numpy as np
import random
import requests
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

instances = response ['Reservations']
myarray = np.asarray(instances)

AZs = []

pprint.pprint("You have %i running AWS instances, the Id(s) are:" % (len(myarray)))
if len(myarray) == 0:
    pprint.pprint("Quitting")
    quit()

for instance in response ['Reservations']:
    thisAZ = instance['Instances'][0]['Placement']['AvailabilityZone']
    print("    "+instance['Instances'][0]['InstanceId']+"   AZ: "+str(thisAZ))
    if any(thisAZ not in az for az in AZs):
        AZs += thisAZ
Gorilla = False

if len(sys.argv) == 1:
    UserInterupted = input("How many instances would you like to disrupt? ")
    if (len(myarray)) <= int(UserInterupted):
        UserInterupted = len(myarray) -1
        pprint.pprint("Can not interupt all instances, leaving one remaining.")
else:
    if sys.argv[1] == "Gorilla":
        Gorilla = True
        AzInterupted = input("Which AZ would you like to disrupt? ")
    else:
        UserInterupted = sys.argv[1]
        if (len(myarray)) <= int(UserInterupted):
            UserInterupted = len(myarray) -1
            pprint.pprint("Can not interupt all instances, leaving one remaining.")

if Gorilla == False:
    if len(sys.argv) == 2:
        shuffled = input("How many times would you like to shuffle the instance order?  ")
    else:
        shuffled = sys.argv[2]

    pprint.pprint("Shuffling order to introduce randomness")
    for i in range (0, int(shuffled)):
        print("Shuffling")
        random.shuffle(instances)

    pprint.pprint("The randomised order is:")
    for instance in instances:
        print("    "+instance['Instances'][0]['InstanceId'])


healthBefore = client.describe_instance_status(
    IncludeAllInstances=True
)

#print(str(sys.argv))
#exit()

TestStatus = ""

RunningAfterCounter = 0
RunningBeforeCounter = 0
InstancesNotRestarted = []

pprint.pprint("The before state is:")
for instanceHealth in healthBefore["InstanceStatuses"]:
    if instanceHealth['InstanceState']['Name'] == "running":
        pprint.pprint("Instance %s in %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['AvailabilityZone'], instanceHealth['InstanceState']['Name']))
        RunningBeforeCounter += 1
    else:
        pprint.pprint("Instance %s in %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['AvailabilityZone'], instanceHealth['InstanceState']['Name']))
        InstancesNotRestarted += instanceHealth['InstanceId']

if RunningBeforeCounter <= 1:
    pprint.pprint("There are too few instances currently running, none available to be interupted while maintaining service.")
    TestStatus = "Failed"
    UserInterupted = 0

InstancesRestarted = 0
start_time = time.time()
pprint.pprint("[Start] Timing AWS instances recovery:")

if Gorilla == True:
    for instanceHealth in healthBefore["InstanceStatuses"]:
        if instanceHealth['AvailabilityZone'] == AzInterupted:
            pprint.pprint("Terminating instance: "+instanceHealth['InstanceId'])
            client.terminate_instances(InstanceIds=[instanceHealth['InstanceId']])
            InstancesRestarted += 1
else:
    for i in range (0, int(UserInterupted)):
        pprint.pprint("Terminating instance: "+instances[i]["Instances"][0]['InstanceId'])
        client.terminate_instances(InstanceIds=[instances[i]["Instances"][0]['InstanceId']])
        InstancesRestarted += 1

progress = "- "
increment = "- "
while RunningBeforeCounter != RunningAfterCounter:
    healthAfter = client.describe_instance_status(
        IncludeAllInstances=True
    )
    RunningAfterCounter = 0

    for instanceHealth in healthAfter["InstanceStatuses"]:
        pprint.pprint("Instance %s is in state %s" % (instanceHealth['InstanceId'], instanceHealth['InstanceState']['Name']))
        if instanceHealth['InstanceState']['Name'] == "running":
            RunningAfterCounter += 1
        else:
            InstancesNotRestarted += instanceHealth['InstanceId']

    progress = progress + increment
    if len(progress) > 50:
        elapsed_time = time.time() - start_time
        TestStatus = "Failed"
        pprint.pprint("Test of instances recovery failed")
        pprint.pprint("The instances did not recover withing the allowed time")
        pprint.pprint("Timing elapsed: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
        break
    print(progress)
    if TestStatus != "Failed":
        time.sleep(10)

elapsed_time = time.time() - start_time
pretty_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
if TestStatus != "Failed":
    TestStatus = "Passed"

pprint.pprint("[Finish] Timing elapsed for recovery from disruption: " + pretty_time)

message = "Conor's Chaos Test Status: %s \
    \nTest completed in %s\
    \nInstances recovered %s\
    \n--------------------------" % (TestStatus, pretty_time, InstancesRestarted)

pprint.pprint(message)

def sns_Sender(message, TestStatus):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn = 'arn:aws:sns:eu-west-1:535132083307:ChaosMonkeyResults-Conor',
        Subject = 'Test Status: ' + TestStatus,
        Message = message
    )

uri = "https://i3ncbf7vpc.execute-api.eu-west-1.amazonaws.com/Prod/send"
body = { "message": message,
  "subject": "Conor's Chaos Test Status: " + TestStatus,
  "toEmails": [
    "ctolan@gmail.com"#, "tud.devops.cm@gmail.com"
  ]
}

response = requests.post(uri , json=body)
if response.status_code == 204:
    print('Lambda Email sent successfully')
else:
    print('An error occurred sending reaching the lambda.')

sns_Sender(message, TestStatus)