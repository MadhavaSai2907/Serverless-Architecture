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
* `AWSLambdaBasicExecutionRole` 

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
* `AWSLambdaBasicExecutionRole`  

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

# Task-3 Automated EBS Snapshot & Cleanup using AWS Lambda and Boto3

## Overview

This project automates the **backup and lifecycle management of EBS volumes** using **AWS Lambda** and **Boto3**.

It performs two key operations:

* Creates snapshots of specified EBS volumes
* Deletes snapshots older than a defined retention period (e.g., 30 days)

---

##  Architecture

```text
AWS Lambda (Python + Boto3)
        ↓
Create Snapshot (EBS Volume)
        ↓
List Existing Snapshots
        ↓
Delete Old Snapshots (Retention Policy)
        ↓
Logs → CloudWatch
```

---

##  Services Used

* Amazon EC2
* AWS Lambda
* AWS Identity and Access Management
* Amazon CloudWatch
* Amazon EventBridge
* Boto3

---

##  Setup Instructions

###  Create / Identify EBS Volume

* Navigate to EC2 → Volumes
* Create or select an existing volume
* Copy the **Volume ID** (my volume - vol-0da6698869ef41c53)

<img width="1892" height="687" alt="image" src="https://github.com/user-attachments/assets/eb78bda2-4130-49d5-a47a-1d7a789c8b90" />

---

### Create IAM Role for Lambda

Attach the following policies:

* `AmazonEC2FullAccess`
* `AWSLambdaBasicExecutionRole`

<img width="1900" height="731" alt="image" src="https://github.com/user-attachments/assets/22813025-1d57-41c7-98b0-7d936ca48568" />

---

### Create Lambda Function
* Create Lambda Fucntion (my lambda function - ebs-snapshot-manager)
* Runtime: Python 3.x
* Assign IAM role created above

<img width="1847" height="736" alt="image" src="https://github.com/user-attachments/assets/2b5f001f-1726-4462-9cb9-d4ca80adbec9" />

---

## Lambda Code

Attached in `EBS snapshot and cleanup.py` file

**Note:** For testing purpose i have taken time as 5 minutes. Only condition replaced is ```timedelta(days=30)``` with ``` timedelta(minutes=5) ```

---

## Execution Steps

1. Deploy the Lambda function
2. Click **Test** to invoke manually
3. Navigate to EC2 → Snapshots
4. Verify:

   * New snapshot created 
   * Old snapshots deleted
   
# old Snapshot
<img width="1915" height="467" alt="snapshot_new" src="https://github.com/user-attachments/assets/fd47d260-682a-45db-ace6-27f355387cba" />

# New Snapshot
<img width="1918" height="250" alt="created_snapshot" src="https://github.com/user-attachments/assets/10538c04-0976-4932-94b4-4429d7e54299" />

---

## Logs & Monitoring

Logs available in:

```text
/aws/lambda/ebs-snapshot-manager
```

via **CloudWatch Logs**

---

##  Sample Output

```text
Created Snapshot: snap-0842b772694a284d7
Deleted Snapshots: ['snap-078177fb5f6e20fb6']
```

<img width="1907" height="655" alt="image" src="https://github.com/user-attachments/assets/1adf0c16-4d1d-49f4-b13b-02f80f4dfc02" />

---

## Scheduling

* Now we have to run this function every week. So we are using EventBridge to create Cron Job for weekly execution of this Function
  To create EventBride 
  - Go to EventBride click on **Schedules**
  - Fill the schedule details and select Schedule pattern (Recurring schedule in our case)
  - Select Cron or Rate based Schedule (Cron Schedule in our case). Click Next.
  - Select Target (Lambda function). Select Lambda function to invoke.
  - COnfigure if any settings and review details and click on create Schedule. 
  
Automate using **EventBridge**:

# Weekly execution

```text
cron(0 2 ? * SUN *)
```

<img width="1901" height="802" alt="image" src="https://github.com/user-attachments/assets/de3eb9fb-6f49-47a1-9fdb-3df834a2ea48" />

---


##  Common Issues & Fixes

| Issue                 | Cause               | Fix                            |
| --------------------- | ------------------- | ------------------------------ |
| Snapshot not deleted  | Used by AMI         | Deregister AMI or skip in code |
| Access denied         | Missing permissions | Attach EC2 + Lambda role       |
| No snapshots found    | Region mismatch     | Use same region                |
| All snapshots deleted | No filter           | Add description/tag filter     |

---


