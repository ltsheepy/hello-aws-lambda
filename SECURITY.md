# Security & Compliance Report

*Last updated: 2025-12-06 06:19:34 UTC*

## Overview

This report provides real-time security and compliance status for the infrastructure.

## Patch Compliance Status

| Instance ID | Patch Group | Installed | Missing | Failed | Status |
|-------------|-------------|-----------|---------|--------|--------|
| `i-095c4728f457489ba` | production | 199 | 0 | 0 | ✅ Compliant |

### Patch Summary

- **Total Patches Installed:** 199
- **Total Patches Missing:** 0
- **Total Patches Failed:** 0

## Security Hub Findings

### Summary by Severity

| Severity | Count | Status |
|----------|-------|--------|
| 🔴 **CRITICAL** | 3 | Action Required |
| 🟠 **HIGH** | 4 | Action Required |
| 🟡 **MEDIUM** | 20 | Review |
| 🟢 **LOW** | 23 | Review |
| 🟢 **INFORMATIONAL** | 0 | Review |
| **TOTAL** | **50** | |

### CRITICAL Severity Findings

#### 1. SSM documents should have the block public sharing setting enabled

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether the block public sharing setting is enabled for AWS Systems Manager documents. The control fails if the block public sharing setting is disabled for Systems Manager documen...

**Resource:** `AWS::::Account:916270395448`

**Compliance Status:** FAILED

**First Observed:** 2025-07-20T04:18:36.362Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 2. IAM root user access key should not exist

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This AWS control checks whether the root user access key is available....

**Resource:** `AWS::::Account:916270395448`

**Compliance Status:** FAILED

**First Observed:** 2024-12-30T01:26:36.737Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 3. Hardware MFA should be enabled for the root user

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This AWS control checks whether your AWS account is enabled to use a hardware multi-factor authentication (MFA) device to sign in with root user credentials....

**Resource:** `AWS::::Account:916270395448`

**Compliance Status:** FAILED

**First Observed:** 2024-08-11T13:11:33.354Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

### HIGH Severity Findings

#### 1. S3 general purpose buckets should block public access

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether an Amazon S3 general purpose bucket blocks public access at the bucket level. The control fails if any of the following settings are set to false: ignorePublicAcls, blockPu...

**Resource:** `arn:aws:s3:::elasticbeanstalk-ap-southeast-2-916270395448`

**Compliance Status:** FAILED

**First Observed:** 2024-10-19T21:28:24.758Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 2. S3 general purpose buckets should block public access

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether an Amazon S3 general purpose bucket blocks public access at the bucket level. The control fails if any of the following settings are set to false: ignorePublicAcls, blockPu...

**Resource:** `arn:aws:s3:::migrationhub-strategy-report-ap-southeast-2-fzj0fqypyvj8rnd1hi`

**Compliance Status:** FAILED

**First Observed:** 2025-08-24T04:54:57.430Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 3. Amazon Inspector Lambda code scanning should be enabled

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether Amazon Inspector Lambda code scanning is enabled. For a standalone account, the control fails if Amazon Inspector Lambda code scanning is disabled in the account. In a mult...

**Resource:** `AWS::::Account:916270395448`

**Compliance Status:** FAILED

**First Observed:** 2024-08-11T13:11:28.464Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 4. Amazon Inspector EC2 scanning should be enabled

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether Amazon Inspector EC2 scanning is enabled. For a standalone account, the control fails if Amazon Inspector EC2 scanning is disabled in the account. In a multi-account enviro...

**Resource:** `AWS::::Account:916270395448`

**Compliance Status:** FAILED

**First Observed:** 2024-08-11T13:11:34.020Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

### MEDIUM Severity Findings

#### 1. S3 general purpose buckets should require requests to use SSL

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether an Amazon S3 general purpose bucket has a policy that requires requests to use SSL. The control fails if the bucket policy doesn't require requests to use SSL....

**Resource:** `arn:aws:s3:::cis-hardened-ssm-logs-916270395448`

**Compliance Status:** FAILED

**First Observed:** 2025-12-06T05:18:39.046Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 2. S3 general purpose buckets should have server access logging enabled

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether server access logging is enabled for an Amazon S3 general purpose bucket. The control fails if server access logging isn't enabled. When logging is enabled, Amazon S3 deliv...

**Resource:** `arn:aws:s3:::cis-hardened-ssm-logs-916270395448`

**Compliance Status:** FAILED

**First Observed:** 2025-12-06T05:18:38.971Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 3. EC2 VPC Block Public Access settings should block internet gateway traffic

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether Amazon EC2 VPC Block Public Access (BPA) settings are configured to block internet gateway traffic for all Amazon VPCs in the AWS account. The control fails if EC2 VPC BPA ...

**Resource:** `arn:aws:ec2:ap-southeast-2:916270395448:vpcblockpublicaccessoptions/916270395448`

**Compliance Status:** FAILED

**First Observed:** 2025-01-17T13:29:56.145Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 4. S3 general purpose buckets should require requests to use SSL

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether an Amazon S3 general purpose bucket has a policy that requires requests to use SSL. The control fails if the bucket policy doesn't require requests to use SSL....

**Resource:** `arn:aws:s3:::m365backups-may2024`

**Compliance Status:** FAILED

**First Observed:** 2024-08-11T13:11:34.032Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

#### 5. S3 general purpose buckets should require requests to use SSL

**Finding ID:** `Software and Configuration Checks/Industry and Regulatory Standards`

**Description:** This control checks whether an Amazon S3 general purpose bucket has a policy that requires requests to use SSL. The control fails if the bucket policy doesn't require requests to use SSL....

**Resource:** `arn:aws:s3:::aws-cloudtrail-logs-916270395448-09bf1008`

**Compliance Status:** FAILED

**First Observed:** 2024-08-11T13:11:34.033Z

**Compliance Framework Mappings:**

**AWS WAF:** `SEC-01: Security Foundations`
**CIS v8:** `General Security Controls`
**NIST 800-53:** `General Security Controls`

**Remediation:** For information on how to correct this issue, consult the AWS Security Hub controls documentation....

*...and 15 more MEDIUM findings*

## Security Configuration

### ✅ Implemented Security Controls

| Control | Status | Details |
|---------|--------|---------|
| SSM Session Manager | ✅ Enabled | No SSH keys required |
| IMDSv2 | ✅ Enforced | Instance metadata protection |
| EBS Encryption | ✅ Enabled | All volumes encrypted at rest |
| S3 Encryption | ✅ Enabled | Logs encrypted with AES256 |
| Private Subnets | ✅ Enabled | No public IP addresses |
| VPC Endpoints | ✅ Enabled | Private AWS service access |
| Security Groups | ✅ Locked | VPC-only traffic |
| IAM Roles | ✅ Least Privilege | Minimal permissions |
| Automated Patching | ✅ Enabled | Tag-based maintenance windows |
| CloudWatch Logging | ✅ Enabled | All actions logged |

### 🔒 Security Recommendations

1. **Enable Security Hub** - Automated security assessments
2. **Enable GuardDuty** - Threat detection
3. **Enable AWS Config** - Configuration compliance
4. **Enable CloudTrail** - API activity logging
5. **Set up SNS Alerts** - Real-time security notifications

## Compliance Framework Coverage

### AWS Well-Architected Framework (Security Pillar)

| Pillar | Controls Implemented | Status |
|--------|---------------------|--------|
| SEC-01: Security Foundations | Security Hub, IAM roles | ✅ Implemented |
| SEC-02: Identity & Access Management | IAM roles, no root access, SSM | ✅ Implemented |
| SEC-03: Detective Controls | CloudWatch Logs, SSM Inventory | ✅ Implemented |
| SEC-04: Infrastructure Protection | VPC, Security Groups, Private Subnets | ✅ Implemented |
| SEC-05: Data Protection | EBS encryption, S3 encryption, IMDSv2 | ✅ Implemented |
| SEC-06: Incident Response | CloudWatch Logs, SSM Session Manager | ✅ Implemented |

### CIS Controls v8

| Control | Description | Status |
|---------|-------------|--------|
| 3: Data Protection | Encryption at rest (EBS, S3) | ✅ Implemented |
| 4: Secure Configuration | IMDSv2, Security Groups | ✅ Implemented |
| 5: Account Management | IAM roles, no root access | ✅ Implemented |
| 6: Access Control | Least privilege IAM | ✅ Implemented |
| 7: Vulnerability Management | Automated patching via SSM | ✅ Implemented |
| 8: Audit Log Management | CloudWatch Logs, S3 logs | ✅ Implemented |
| 12: Network Infrastructure | VPC, Private subnets, VPC endpoints | ✅ Implemented |

### NIST 800-53 Rev 5

| Family | Controls | Status |
|--------|----------|--------|
| AC: Access Control | AC-2, AC-3, AC-6 (Least Privilege) | ✅ Implemented |
| AU: Audit & Accountability | AU-2, AU-3, AU-9, AU-12 | ✅ Implemented |
| CM: Configuration Management | CM-2, CM-3, CM-6, CM-8 | ✅ Implemented |
| IA: Identification & Authentication | IA-2, IA-5 | ✅ Implemented |
| SC: System & Communications Protection | SC-7, SC-8, SC-13, SC-28 | ✅ Implemented |
| SI: System & Information Integrity | SI-2, SI-4 | ✅ Implemented |

### Compliance Gaps & Recommendations

| Framework | Gap | Recommendation |
|-----------|-----|----------------|
| CIS v8 | 6.3: MFA not enforced | Enable MFA for IAM users |
| NIST 800-53 | IA-2(1): MFA | Implement MFA for all access |
| AWS WAF | SEC-04: GuardDuty not enabled | Enable GuardDuty for threat detection |
| CIS v8 | 8.2: CloudTrail not enabled | Enable CloudTrail for API logging |
| NIST 800-53 | AU-2: Comprehensive audit | Enable AWS Config for change tracking |

## Quick Actions

### View Patch Compliance
```bash
aws ssm describe-instance-patch-states \
  --instance-ids $(terraform output -raw instance_id) \
  --region ap-southeast-2
```

### Run Patch Scan
```bash
aws ssm send-command \
  --document-name AWS-RunPatchBaseline \
  --targets Key=tag:PatchGroup,Values=production \
  --parameters Operation=Scan \
  --region ap-southeast-2
```

### View Security Hub Findings
```bash
aws securityhub get-findings \
  --filters 'RecordState=[{Value=ACTIVE,Comparison=EQUALS}]' \
  --region ap-southeast-2
```

### Check SSM Agent Status
```bash
aws ssm describe-instance-information \
  --filters Key=InstanceIds,Values=$(terraform output -raw instance_id) \
  --region ap-southeast-2
```

---

*This report is automatically generated. Run `make security-report` to update.*