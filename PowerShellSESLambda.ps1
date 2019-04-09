# PowerShell script file to be executed as a AWS Lambda function. 
# 
# When executing in Lambda the following variables will be predefined.
#   $LambdaInput - A PSObject that contains the Lambda function input data.
#   $LambdaContext - An Amazon.Lambda.Core.ILambdaContext object that contains information about the currently running Lambda environment.
#
# The last item in the PowerShell pipeline will be returned as the result of the Lambda function.
#
# To include PowerShell modules with your Lambda function, like the AWSPowerShell.NetCore module, add a "#Requires" statement 
# indicating the module and version.

#Requires -Modules @{ModuleName='AWSPowerShell.NetCore';ModuleVersion='3.3.365.0'}

#Uncomment to send the input event to CloudWatch Logs
Write-Host "Starting Script to Send Email"

Write-Host (ConvertTo-Json -InputObject $LambdaInput -Compress -Depth 5)

$destination = $LambdaInput.toEmails
$message = $LambdaInput.message
$subject = $LambdaInput.subject

Write-host $destination
Write-host $message
Write-host $subject

Send-SESEmail -Source "ctolan@gmail.com" -Destination_ToAddress $destination -Subject_Data $subject -Text_Data $message