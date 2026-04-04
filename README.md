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


<img width="1908" height="322" alt="ec2 execution" src="https://github.com/user-attachments/assets/d7ec6262-6fb2-4462-9d0c-df0221784f39" />

---

## Common Issues & Fixes

| Issue                        | Cause               | Fix                                  |
| ---------------------------- | ------------------- | ------------------------------------ |
| Log group not found          | Missing permissions | Attach `AWSLambdaBasicExecutionRole` |
| Instances not changing state | Wrong tag key/value | Ensure exact match (`Action`)        |
| No instances detected        | Region mismatch     | Use same region for EC2 & Lambda     |

---


# Task-2 Automated S3 Bucket Cleanup using AWS Lambda & Boto3

## Overview

This project automates the deletion of old files from an S3 bucket using **AWS Lambda** and **Boto3**.

The Lambda function scans objects in a bucket and deletes files older than a defined time threshold (e.g., 30 days or configurable duration).

---

##  Architecture

```
AWS Lambda (Python + Boto3)
        ↓
List S3 Objects
        ↓
Check LastModified Timestamp
        ↓
Delete Old Files
        ↓
Logs → CloudWatch
```

---

##  Services Used

* Amazon S3
* AWS Lambda
* AWS Identity and Access Management
* Amazon CloudWatch
* Boto3

---

##  Setup Instructions

### Create S3 Bucket

* Create a new S3 bucket - lambda-s3-assignment(my bucket)
* Upload sample files for testing


<img width="1637" height="412" alt="Create and Upload" src="https://github.com/user-attachments/assets/70f32f73-6d61-4eb6-8f6e-4a00b30a0a51" />


---

### Create IAM Role for Lambda

* Create IAM role - Lambda-S3-Cleanup-role (my role)
Attach the following policies:

* `AmazonS3FullAccess`
* `AWSLambdaBasicExecutionRole`  *(required for logging)*

<img width="1918" height="732" alt="role" src="https://github.com/user-attachments/assets/07dab355-827c-4259-9ec9-b82a5a5ac309" />

---

### Create Lambda Function
* Create Lambda function - s3-cleanup-function (my function)
* Runtime: Python 3.x
* Assign IAM role created above

<img width="1852" height="716" alt="lambda" src="https://github.com/user-attachments/assets/3d49d2fa-e161-4e3c-9736-52ed7d8ac366" />

---

## Lambda Code

Attached in `S3 files delete.py` file

**Note:** For testing purpose i have taken time as 5 minutes. Only condition replaced is ```timedelta(days=30)``` with ``` timedelta(minutes=5) ```


---

## Execution Steps

1. Deploy the Lambda function
2. Click **Test** to invoke manually
3. Navigate to S3 bucket
4. Verify:

   * Old files →  deleted
   * Recent files →  retained

---

## Logs & Monitoring

Logs are available in:

```
/aws/lambda/s3-cleanup-function
```

via **CloudWatch Logs**

---

## Sample Output

### logs
<img width="1862" height="812" alt="files_logs" src="https://github.com/user-attachments/assets/55b5a3da-ba54-49c8-8621-c0f15ff16bb8" />

### S3 files after execution
<img width="1678" height="372" alt="files_a_1" src="https://github.com/user-attachments/assets/9418b0f4-2e6e-42d2-8571-4b6328218866" />

---



## Common Issues & Fixes

| Issue                        | Cause                          | Fix                                     |
| ---------------------------- | ------------------------------ | --------------------------------------- |
| No files deleted             | Files not older than threshold | Reduce time (e.g., minutes for testing) |
| Access denied                | Missing permissions            | Attach S3 + Lambda execution role       |
| No logs visible              | Missing logging policy         | Add `AWSLambdaBasicExecutionRole`       |
| Only partial files processed | API limit (1000 objects)       | Use paginator                           |

---
