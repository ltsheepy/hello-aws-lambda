# GitHub Actions Workflows

This directory contains CI/CD workflows for automated Terraform deployments to AWS.

## Workflows

### 1. `terraform-deploy.yml` - Main Deployment Pipeline

**Triggers:**
- Push to `main` branch
- Pull requests to `main`
- Manual workflow dispatch

**Jobs:**

1. **security-checks** - Security scanning and linting
   - Terraform format check
   - TFLint (linting)
   - TFSec (security scanning)
   - Checkov (compliance checking)
   - Uploads results to GitHub Security tab

2. **terraform-plan** - Generate execution plan
   - Validates Terraform configuration
   - Creates plan and uploads as artifact
   - Comments plan on PRs
   - Shows changes in GitHub Actions summary

3. **terraform-apply** - Deploy to AWS (main branch only)
   - Requires manual approval (production environment)
   - Applies Terraform changes
   - Outputs instance details
   - Creates issue on failure

4. **update-documentation** - Auto-update docs
   - Generates architecture diagram
   - Updates README with costs
   - Creates security report
   - Commits changes back to repo

5. **terraform-destroy** - Destroy infrastructure (manual only)
   - Requires manual approval
   - Destroys all resources

### 2. `terraform-security.yml` - Security Scanning

**Triggers:**
- Push to any branch
- Pull requests

**Scans:**
- TFLint for best practices
- TFSec for security issues
- Checkov for compliance
- Terraform validate

### 3. `documentation.yml` - Documentation Updates

**Triggers:**
- Push to main with Terraform changes
- Manual workflow dispatch

**Updates:**
- Architecture diagrams
- Cost breakdowns
- Security reports

## Setup

### 1. Required Secrets

Add these secrets in GitHub Settings > Secrets and variables > Actions:

```
AWS_ACCESS_KEY_ID       - AWS access key
AWS_SECRET_ACCESS_KEY   - AWS secret key
```

**Recommended: Use OIDC instead of long-lived credentials**

### 2. OIDC Setup (Recommended)

Create an IAM role with trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:YOUR_ORG/YOUR_REPO:*"
        }
      }
    }
  ]
}
```

Then update workflows to use:
```yaml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::ACCOUNT_ID:role/GitHubActions
    aws-region: ap-southeast-2
```

### 3. Required IAM Permissions

Minimum IAM policy for deployment:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "vpc:*",
        "ssm:*",
        "iam:*",
        "s3:*",
        "cloudwatch:*",
        "dynamodb:*"
      ],
      "Resource": "*"
    }
  ]
}
```

### 4. Environment Protection Rules

Configure in GitHub Settings > Environments:

**production:**
- Required reviewers: 1+
- Wait timer: 0 minutes
- Deployment branches: main only

**production-destroy:**
- Required reviewers: 2+
- Wait timer: 5 minutes
- Deployment branches: main only

## Usage

### Deploy to AWS

**Automatic (on push to main):**
```bash
git add .
git commit -m "Update infrastructure"
git push origin main
```

**Manual:**
1. Go to Actions tab
2. Select "Terraform Deploy to AWS"
3. Click "Run workflow"
4. Choose action: plan/apply/destroy

### Review Changes (Pull Request)

1. Create PR with Terraform changes
2. Security checks run automatically
3. Plan is commented on PR
4. Review and approve
5. Merge to deploy

### Destroy Infrastructure

1. Go to Actions tab
2. Select "Terraform Deploy to AWS"
3. Click "Run workflow"
4. Choose action: "destroy"
5. Approve in production-destroy environment

## Workflow Outputs

### Plan Output
- Shows resources to be created/modified/destroyed
- Posted as PR comment
- Available in Actions summary

### Apply Output
- Instance ID
- SSM connect command
- Resource details

### Security Scan Results
- Available in Security tab
- SARIF format for GitHub integration
- Detailed findings in Actions logs

## Troubleshooting

### Plan fails with "Error: No valid credential sources"
- Check AWS secrets are configured
- Verify IAM permissions
- Check OIDC role trust policy

### Apply fails with "Error acquiring the state lock"
- Another workflow is running
- Wait for it to complete
- Or manually unlock: `terraform force-unlock LOCK_ID`

### Documentation not updating
- Check Python dependencies installed
- Verify AWS credentials for state access
- Check file permissions

### Security scan failures
- Review findings in Security tab
- Fix issues in code
- Re-run workflow

## Best Practices

1. **Always review plans** before applying
2. **Use OIDC** instead of long-lived credentials
3. **Enable branch protection** on main
4. **Require PR reviews** for infrastructure changes
5. **Use environments** for approval gates
6. **Monitor costs** via generated reports
7. **Review security findings** regularly
8. **Keep Terraform version** up to date

## Local Testing

Test workflows locally before pushing:

```bash
# Install act (GitHub Actions local runner)
brew install act

# Run workflow locally
act -j security-checks

# Run with secrets
act -j terraform-plan --secret-file .secrets
```

## Monitoring

### GitHub Actions
- View runs: Actions tab
- Check logs: Click on workflow run
- Download artifacts: Plan files, reports

### AWS Console
- CloudWatch Logs: `/aws/ssm/maintenance-windows/`
- Systems Manager: Patch compliance
- Security Hub: Security findings

## Support

For issues:
1. Check workflow logs
2. Review error messages
3. Consult Terraform documentation
4. Open an issue in this repository
