# athena-calculator

This project helps in creating the rest api to calculate serviceability.

## Description

The serviceability is composed by:

Total income\
Total expenses\
Surplus = monthly income - monthly expenses<br /> 
Serviceability = surplus * FACTOR<br />

Where: FACTOR is a configuration internal to the application, ideally easily configurable

We achived this by API gateway endpoint calling a lambda function using proxy integration.

## Prerequisites
i) Create a zip of contents of lambda folder present in the repository and upload it to the bucket of your choice. 

ii) IAM user with below access to start with(can be fine grained):
* AWSLambdaFullAccess
* IAMFullAccess 
* AmazonS3FullAccess
* AmazonAPIGatewayAdministrator
* AWSCloudFormationFullAccess

## CloudFormation Template

* Upload the template with updating the parameters. s3BucketName, s3ZipFileName are the mandatory parameters need to be changed
  to the corresponding bucket where you uploaded the lamdba zip code. Rest all values can be set to default.
* Output will be the API Gateway Invoke URL.

## Usage

* Once the deployment is successful, we can consume the rest api without any authentication.
* Corresponding log groups will be created.
* Create a data.json file with the below content.\
 {
  "incomes": [[200,"fortnightly"], [100, "monthly"], [1200, "yearly"]],
  "expenses": [50,20,30]
 }
* Run:-<br />
curl -d "@data.json" -X POST \<API Gateway Invoke URL from the output of template deployment>/calculate  

## Stretched Content

* I assume all code must be present in the github and then we can amend "git tag" to the file name while creating the zip folder of the lambda code. 
  This will be refered in the cloud formation template under lambda function creation. We need a deployment by using this approach. This gives clear picture
  in backtracking to code base and compare to the changes that happened on top.
* We can handle autherization by using API Gateway Lambda authorizers or using Amazon Cognito User Pools.

