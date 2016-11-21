# AWS CloudWatch to ServiceNow Event Management Lambda Integration

This integration serves as a replacement for the OOTB ServiceNow AWS CloudWatch integration. It can be expanded to support a wider set of features and configuration scenarios.

## Requirements
* An SNS topic must exist.
* CloudWatch Alarms must be notifying to that topic
    * The alarms should have two conditions: ALARM and OK. This will allow for clearing events to be sent to ServiceNow Event Management
* A proper lambda execution IAM role configured.
    * The following minimum permissions are required:
        * AmazonEC2ReadOnlyAccess
        * AmazonAPIGatewayPushToCloudWatchLogs
        * AmazonSNSReadOnlyAccess
    * As well as the following in-line policy (built by one-click deployment in AWS)
    ```
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ],
          "Resource": "arn:aws:logs:*:*:*"
        }
      ]
    }
    ```
        
## How to build and deploy
* Lambda requires python2.7.
* Lambda also requires all the external libraries to be in the root of the application's directory.
* ```cd cloudwatch_to_em```
* ```pip install -r requirements.txt -t . ```
* ```zip -r deploy.zip .```
* Deploy the deploy.zip to Lambda
* The following environment variables will need to be set in Lambda:
    * ```username```: Username to authenticate against your ServiceNow Instance
    * ```password```: Password to authenticate against your ServiceNow Instance
    * ```table_namespace```: Namespace of the table API for ServiceNow Event Management. e.g. ```/api/now/table/em_event```
    * ```domain```: Domain of your servicenow instance. Should be ```service-now.com``` unless you have an on-prem install.
    * ```instance```: Your ServiceNow instance name.
* Lambda execution time will need to be increased. Will vary by instance.