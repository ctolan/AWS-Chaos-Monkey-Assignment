# Welcome to Conor's TUD Chaos Monkey Project

```code
  _______ _    _ _____     _____ _                       __  __             _
 |__   __| |  | |  __ \   / ____| |                     |  \/  |           | |
    | |  | |  | | |  | | | |    | |__   __ _  ___  ___  | \  / | ___  _ __ | | _____ _   _
    | |  | |  | | |  | | | |    | '_ \ / _` |/ _ \/ __| | |\/| |/ _ \| '_ \| |/ / _ \ | | |
    | |  | |__| | |__| | | |____| | | | (_| | (_) \__ \ | |  | | (_) | | | |   <  __/ |_| |
    |_|   \____/|_____/   \_____|_| |_|\__,_|\___/|___/ |_|  |_|\___/|_| |_|_|\_\___|\__, |
                                                                                      __/ |
                                                                                     |___/
```

The tud_cm.py script in this project can be used to test your HA implementation and resilence against disruption. This is acomplished by randomly terminating instances on AWS to simulate hardware failures in the datacenter.

The script can be run interactively allowing the user to select the number of instances that are disrupted and will measure time elapsed until services are restored. The result of the test will be sent to subscribed email addresses via an SNS topic and pushed through SES by a Lambda function.

## Usage

### Pre-requisites

Configure your:

- aws_access_key_id
- aws_secret_access_key
- default_region - eu-west-1

Review and install any required packages at the top of the script file.

## Screen Cast location

A screen cast demonstration of the project can be found in three parts here:
Part-1
https://youtu.be/5i28HDAefFM

Part-2
https://youtu.be/kuFQ13UGVs0

Part-3
https://youtu.be/ps67EhdjzBs

## Invoke the script

Invoke the python script like any one, it is self contained.

```python
> python tud_cm.py
```

The script can also be run with input parameters for automation purposes.

```python
> python tud_cm.py 1 5
```

In the above example the 1st parameter is how many instances and the second is the number of shuffles to perform.

## Bonus Gorilla Mode

There is a bonus chaos mode - Chaos Gorilla - which will wipe out instances an Availability Zone (AZ) at a time, to simlare AZ outtages.

```python
> python Gorilla
```

## Example Run

The following is an example of the script running, shortened for brevity.

```python
python .\tud_cm.py 1 5

'Welcome to TUD Chaos Monkey by Conor Tolan'
The following program will intentionally disrupt your AWS instances,
please ensure you are authorised to execute these changes.


'You have 3 running AWS instances, the Id(s) are:'
    i-0637587d7d9dd2afd   AZ: eu-west-1a
    i-0127ba7d87debb6ac   AZ: eu-west-1b
    i-0a5ded4e2e3bdfd20   AZ: eu-west-1c
'Shuffling order to introduce randomness'
Shuffling
Shuffling
Shuffling
Shuffling
Shuffling
'The randomised order is:'
    i-0637587d7d9dd2afd
    i-0a5ded4e2e3bdfd20
    i-0127ba7d87debb6ac
'The before state is:'
'Instance i-0637587d7d9dd2afd in eu-west-1a is in state running'
'Instance i-0127ba7d87debb6ac in eu-west-1b is in state running'
'Instance i-0a5ded4e2e3bdfd20 in eu-west-1c is in state running'
'[Start] Timing AWS instances recovery:'
'Terminating instance: i-0637587d7d9dd2afd'
'Instance i-0637587d7d9dd2afd is in state shutting-down'
'Instance i-0127ba7d87debb6ac is in state running'
'Instance i-0a5ded4e2e3bdfd20 is in state running'
- -
'Instance i-0637587d7d9dd2afd is in state shutting-down'
'Instance i-0127ba7d87debb6ac is in state running'
'Instance i-0a5ded4e2e3bdfd20 is in state running'

....
'Instance i-0afe33bee98f641a0 is in state pending'
'Instance i-0127ba7d87debb6ac is in state running'
'Instance i-0a5ded4e2e3bdfd20 is in state running'
- - - - - - - - - - - -
'Instance i-0afe33bee98f641a0 is in state running'
'Instance i-0127ba7d87debb6ac is in state running'
'Instance i-0a5ded4e2e3bdfd20 is in state running'
- - - - - - - - - - - - -
'[Finish] Timing elapsed for recovery from disruption: 00:02:01'
"Conor's Chaos Test Status: Passed     \n"
 'Test completed in 00:02:01    \n'
 'Instances recovered 1    \n'
 '--------------------------'
SNS topic notification sent successfully
Lambda email sent successfully
```

## Gorilla Example Run

```python
python .\tud_cm.py Gorilla


'Welcome to TUD Chaos Monkey by Conor Tolan'
The following program will intentionally disrupt your AWS instances,
please ensure you are authorised to execute these changes.


'You have 3 running AWS instances, the Id(s) are:'
    i-0127ba7d87debb6ac   AZ: eu-west-1b
    i-0afe33bee98f641a0   AZ: eu-west-1a
    i-0a5ded4e2e3bdfd20   AZ: eu-west-1c
Which AZ would you like to disrupt? eu-west-1b
```

## Safety and securty

There is little securty built into this script, it is assumed that if your AWS account has instance terminate permissions than you have been granted permission to terminate instances by the organisation and so can proceed.

The one catch inbuilt to this script is that it will not terminate all instances, if you select more instances than are currently running, one will be left standing. This ensures one  instance will always remain available.

## Notification

The script uses both an AWS SNS topic where interested parties can subscribe to updates, and an AWS Lambda invocation of AWS SES to push email notifications to prescribed parties. This way it can be configured to email support distribution lists, but also allow interested application team members to subscribe to the same information.

### SNS and Email message example

```code
Conor's Chaos Test Status: Passed
Test completed in 00:02:46
Instances recovered 1
--------------------------
```

### Failure message example

```code
Conor's Chaos Test Status: Failed
Test completed in 00:04:02
Instances recovered 2
--------------------------
```

## Link to Azure Comparison discussion and analysis

[Azure TUD Chaos Comparison](https://github.com/MSc-DevOps-ArchDesign/enterprise-architecture-design-ctolan/blob/master/Azure_tud_cm.md)