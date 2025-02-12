# Career Match Cloud Infrastructure

## Overview

This cloud infrastructure setup for the **Career Match App** is designed to be **scalable, secure, and resilient**, leveraging **AWS services** and **Terraform** for Infrastructure as Code (IaC). The architecture includes components for **job recommendation processing**, **data storage**, and **APIs** to interact with the frontend and AI-driven backend systems.

## **Architecture Overview**

Key cloud components:
- **Compute Layer:** EC2 instances and Lambda functions for job recommendation logic.
- **Data Storage:** RDS (PostgreSQL) and S3 buckets for user data, job listings, and logs.
- **Networking:** VPC setup with subnets, security groups, and IAM roles.
- **AI & ML:** OpenAI embeddings integrated with Pinecone for job recommendations.
- **Monitoring & Logging:** CloudWatch and AWS X-Ray for observability.

---

## **Terraform Modules**

The infrastructure is modularized with the following Terraform modules:

- **S3 Buckets:** Stores resumes, job descriptions, and logs.
- **VPC:** Network setup for secure communication between backend services.
- **RDS:** PostgreSQL database for storing user profiles and job data.
- **EC2 & Lambda:** Compute layer to run recommendation services.
- **IAM:** Role-based access control to manage AWS permissions.

---

## **Prerequisites**
Before deploying this infrastructure, ensure you have:
- **Terraform v1.0+** installed.
- AWS credentials configured with permissions to create and manage AWS resources.
- A valid AWS account (recommended region: **ap-southeast-2, Sydney**).

---

## **Deployment Steps**

### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd career-match-cloud
```

### **Step 2: Initialize Terraform**
```bash
terraform init
```

### **Step 3: Validate Configuration**
```bash
terraform validate
```

### **Step 4: Plan Deployment**
```bash
terraform plan
```

### **Step 5: Deploy Infrastructure**
```bash
terraform apply
```
- Confirm by typing `yes` when prompted.

---

## **Destroying the Infrastructure**
To remove all created resources:
```bash
terraform destroy
```
- Confirm by typing `yes` when prompted.

---

## **Folder Structure**

```plaintext
eCommerce_DEproject/
├── modules/
│   ├── s3-buckets/
│   ├── vpc/
│   ├── rds/
│   ├── ec2/
│   ├── iam/
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
├── destroy.tf
├── README.md  # (this file)
```

---

## **Key Features**

### **1. Secure & Scalable Architecture**
- **VPC with private and public subnets** for networking security.
- **IAM roles and policies** to enforce access control.

### **2. AI-Powered Job Matching**
- **OpenAI embeddings & Pinecone vector search** for job recommendations.
- **EC2 instances & Lambda functions** to process candidate-job matches.

### **3. Resilient Data Storage & Processing**
- **S3 Buckets** for resumes, job postings, and logging.
- **RDS PostgreSQL** to store structured job and user data.

### **4. Observability & Monitoring**
- **CloudWatch** for log aggregation and monitoring.
- **AWS X-Ray** for tracing and debugging service interactions.

---

## **Future Enhancements**
- Implement **autoscaling** for EC2 instances.
- Integrate **AWS Glue** for batch ETL processing.
- Enhance **monitoring dashboards** with CloudWatch Insights.

---

## **Contact**
For questions or contributions, reach out to the project maintainers.

---

