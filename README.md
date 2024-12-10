
<img width="791" alt="Screenshot 2024-12-10 at 1 25 57 PM" src="https://github.com/user-attachments/assets/faed544c-42cc-40cb-a20f-74aaf1115709">



# TaskManagerGT
Task manager for CSCI399

Steps:
Clone the repository

Create S3 Bucket

Uncheck Block Public Access settings for this bucket and acknowledgement box

Change bucket policy - the bucket policy in our texts

Upload templates without links in s3

Go to amplify

Create new app

Deploy without git 

Next

Choose s3

Browse

Choose s3 bucket

S3 links should now be in https for index.html and task-manager.html

Create Dynamodb with with partition key: user_id (String) and sort key: task_id (String) and default settings

API gateway

Create a rest API and build with whatever name

Click create resource and name it task and don't enable cors

Select tasks and hit create resource and name the resource {taskId}

Go to lambda

Click Create function

Author from scratch

Name first function GetTask

Change Runtime to python 3.*

Click change default execution role

Use the existing role LabRole

Do the same and name it DeleteTask

Again and do CreateTask

Import all the lambda functions

Go back to API gateway and attach functions

Click create methods on tasks

Get is GetFunction

Check lambda proxy integration

Open HTTP request headers

Name is Authorizer and make sure required is selected

Click /tasks and hit enable cors

Enable everything except what is under additional settings

Do the same for /{taskId}

Open cognito 

Create user pool

Select SPA

Configure options are email and username

Set return url to task-manager.html from s3 the https link

Go to app clients

Go to domain under branding and select actions and select edit cognito domain branding version

Switch to Hosted UI (classic)

Copy your Cognito domain that is under cognito domain and save it somewhere

Open view login page

Copy login page link

Navigate back to API Gateway

Select your Api

Select authorizers

Create authorizer

Name it CongitoUserAuth

Choose Cognito under Authorizer type

Choose your created cognito user pool

As the token source make it Authorization

Go back to resources

Click on your Get method

Scroll down to method requests and click edit

Select your Cognito authorizer and hit save

Redo the same for the POST and DELETE methods

Hit Deloy API

Click new stage and name your API Stage

Under Stages you should have an invoke url

Save this somewhere

Open index.html in an Cloud9

Add your AWS Cognito Hosted Login URL under where it says link to AWS Cognito login in the quotes

Save change

Put updated index into S3 bucket

Open task-manager.html in IDE

On Line 100 insert the same link you had put into the index.html

On Line 106 add that link again but delete everything after amazoncognito.com/ and add oauth2/token instead

On line 109 your redirect_uri is your object url for your task manager

On line 110 add your client id from your Cognito app client

On line 133 for your cognito hosted ui url add the same on that you did in the index.html

On line 139 add your API gateway invoke url from stages

On line 162 you are going to add your invoke url and leave the /${task.task_id}

On line 202 add your invoke url again

On line 230 add your link from your index object url

Save all those changes

Upload task-manager.html into your s3 bucket

To access task manager open your s3 index object link in your browser

