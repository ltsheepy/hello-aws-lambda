# Hello AWS Lambda

A simple serverless API using AWS Lambda, API Gateway, and Terraform.

## What This Does

- Creates a Python Lambda function that returns "Hello from AWS Lambda! 🚀"
- Sets up API Gateway to give it a public URL
- Manages everything with Terraform

## Deploy to AWS

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Preview what will be created:**
   ```bash
   terraform plan
   ```

3. **Deploy to AWS:**
   ```bash
   terraform apply
   ```
   Type `yes` when prompted.

4. **Get your API URL:**
   After deployment, Terraform will output your API URL. Copy it and open in your browser!

## Test It

```bash
curl <your-api-url>
```

You should see: `Hello from AWS Lambda! 🚀`

## Clean Up

When you're done, destroy everything to avoid AWS charges:
```bash
terraform destroy
```

## What You're Learning

- **Lambda:** Serverless functions (no servers to manage)
- **API Gateway:** Gives your Lambda a public HTTP endpoint
- **Terraform:** Infrastructure as code (repeatable, version-controlled)
- **IAM:** Permissions for Lambda to run and log
