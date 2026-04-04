# Serverless-Architecture Assignment
Assignment on Serverless Architecture using Lambda functions, Boto3, etc.

#

# Task-1 Automated EC2 Instance Management using AWS Lambda & Boto3

## Overview

This project demonstrates how to automate the **starting and stopping of EC2 instances** based on resource tags using **AWS Lambda** and **Boto3 (Python SDK)**.

The Lambda function scans EC2 instances and performs actions based on a predefined tag:

* `Auto-Stop` → Stops the instance
* `Auto-Start` → Starts the instance

---

## Architecture

```
AWS Lambda (Python + Boto3)
        ↓
Describe EC2 Instances
        ↓
Filter by Tag (Action)
        ↓
Start / Stop Instances
        ↓
Logs → CloudWatch
```

---

##  Services Used

* Amazon EC2
* AWS Lambda
* AWS Identity and Access Management (IAM)
* Amazon CloudWatch
* Boto3

---

##  Setup Instructions

### Create EC2 Instances

Create two instances:

| Instance Name | Tag Key | Tag Value  |
| ------------- | ------- | ---------- |
| Auto-Stop     | Action  | Auto-Stop  |
| Auto-Start    | Action  | Auto-Start |

<img width="1917" height="476" alt="ec2 creation" src="https://github.com/user-attachments/assets/fad64a7e-a7ba-49bc-bb10-7d05d6c6b2d3" />

---


### Create IAM Role for Lambda

* Name - Lambda-EC2-Automation-Role (my IAM role)

Attach the following policies:

* `AmazonEC2FullAccess`
* `AWSLambdaBasicExecutionRole`  *(required for logging)*

<img width="1883" height="711" alt="IAM role" src="https://github.com/user-attachments/assets/e94c999a-6740-45c6-b8fe-42d4e78cbab6" />

---

### Create Lambda Function

* Name - manage-ec2 (my Lambda function name)
* Runtime: Python 3.x
* Role: Use the IAM role created above

<img width="1790" height="791" alt="lambda function" src="https://github.com/user-attachments/assets/70c6bd52-ede4-4ffc-87c9-51a41db4fb54" />

---

## Lambda Code

Attached in `EC2 instances.py` file

---

## Execution Steps

1. Deploy the Lambda function
2. Click **Test** to invoke manually
3. Navigate to EC2 dashboard
4. Verify:

   * `Auto-Stop` → Instance stopped
   * `Auto-Start` → Instance running

---

## Logs & Monitoring

Logs are available in:

```
/aws/lambda/manage-ec2
```

<img width="1628" height="726" alt="logs" src="https://github.com/user-attachments/assets/8ab729ae-47eb-41ee-9073-3fc711bbb937" />

---

## Sample Output

```
Stopped Instances: ['i-1234567890']
Started Instances: ['i-0987654321']
```

<img width="1908" height="322" alt="ec2 execution" src="https://github.com/user-attachments/assets/d7ec6262-6fb2-4462-9d0c-df0221784f39" />

---

## Common Issues & Fixes

| Issue                        | Cause               | Fix                                  |
| ---------------------------- | ------------------- | ------------------------------------ |
| Log group not found          | Missing permissions | Attach `AWSLambdaBasicExecutionRole` |
| Instances not changing state | Wrong tag key/value | Ensure exact match (`Action`)        |
| No instances detected        | Region mismatch     | Use same region for EC2 & Lambda     |

---


