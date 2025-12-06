# AWS Cost Estimate - CIS Hardened Infrastructure

## Monthly Cost Breakdown (Sydney Region - ap-southeast-2)

### Compute
| Service | Details | Monthly Cost |
|---------|---------|--------------|
| EC2 t3.micro | 730 hours/month | **$10.95** |
| EBS gp3 30GB | Root volume | **$2.88** |

### Networking
| Service | Details | Monthly Cost |
|---------|---------|--------------|
| NAT Gateway | 730 hours | **$48.18** |
| NAT Gateway Data | ~10GB/month | **$0.59** |
| VPC Endpoints (3x) | SSM, SSMMessages, EC2Messages | **$21.90** |
| VPC Endpoint Data | ~5GB/month | **$0.05** |

### Storage & Logs
| Service | Details | Monthly Cost |
|---------|---------|--------------|
| S3 Storage | ~1GB logs | **$0.025** |
| S3 Requests | ~10k PUT/GET | **$0.05** |
| CloudWatch Logs | ~500MB ingested | **$0.25** |
| CloudWatch Logs Storage | ~1GB stored | **$0.03** |

### Systems Manager
| Service | Details | Monthly Cost |
|---------|---------|--------------|
| SSM Session Manager | Free | **$0.00** |
| SSM Patch Manager | Free | **$0.00** |
| SSM Inventory | Free | **$0.00** |
| SSM Maintenance Windows | Free | **$0.00** |

---

## Total Monthly Cost: **~$85/month**

### Cost Breakdown by Category:
- **Compute & Storage**: $13.83 (16%)
- **Networking**: $70.72 (83%)
- **Logs & Monitoring**: $0.33 (1%)

---

## Cost Optimization Options

### Option 1: Remove NAT Gateway (Recommended for Dev)
**Savings: -$48.77/month (-57%)**

If you don't need outbound internet access:
- Remove NAT Gateway
- Keep VPC endpoints for SSM access
- **New Total: ~$36/month**

```hcl
# In networking.tf
enable_nat_gateway = false
```

### Option 2: Use NAT Instance Instead
**Savings: -$40/month (-47%)**

Replace NAT Gateway with t4g.nano NAT instance:
- NAT Gateway: $48.18 → NAT Instance: $3.07
- **New Total: ~$45/month**

### Option 3: Remove VPC Endpoints (Not Recommended)
**Savings: -$21.95/month (-26%)**

Use NAT Gateway for SSM traffic instead:
- Less secure (traffic goes through internet)
- Increases NAT Gateway data charges
- **New Total: ~$63/month**

### Option 4: Stop Instance When Not in Use
**Savings: Variable**

If running 8 hours/day (business hours only):
- EC2: $10.95 → $3.65 (-$7.30)
- NAT Gateway: $48.18 → $16.06 (-$32.12)
- **New Total: ~$45/month**

---

## Annual Cost Comparison

| Configuration | Monthly | Annual | Savings |
|---------------|---------|--------|---------|
| **Current (Full)** | $85 | $1,020 | - |
| Without NAT Gateway | $36 | $432 | $588 |
| With NAT Instance | $45 | $540 | $480 |
| Part-time (8hrs/day) | $45 | $540 | $480 |

---

## Free Tier Benefits (First 12 Months)

If you're on AWS Free Tier:
- EC2 t2.micro: 750 hours/month free (switch from t3.micro)
- EBS: 30GB free
- **Savings: ~$13/month for first year**

To use Free Tier, change in `variables.tf`:
```hcl
instance_type = "t2.micro"
```

---

## Cost Monitoring

### Set Up Billing Alerts

```bash
# Create SNS topic for alerts
aws sns create-topic --name billing-alerts --region us-east-1

# Subscribe your email
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:ACCOUNT_ID:billing-alerts \
  --protocol email \
  --notification-endpoint your-email@example.com

# Create billing alarm (alert at $50)
aws cloudwatch put-metric-alarm \
  --alarm-name monthly-billing-alert \
  --alarm-description "Alert when monthly charges exceed $50" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 21600 \
  --evaluation-periods 1 \
  --threshold 50 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:ACCOUNT_ID:billing-alerts \
  --region us-east-1
```

### View Current Costs

```bash
# Get month-to-date costs
aws ce get-cost-and-usage \
  --time-period Start=$(date -u -d "$(date +%Y-%m-01)" +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
  --granularity MONTHLY \
  --metrics UnblendedCost \
  --region us-east-1
```

---

## Recommendations

**For Production**: Keep current setup ($85/month)
- High availability with NAT Gateway
- Secure with VPC endpoints
- Full monitoring and patching

**For Development**: Remove NAT Gateway ($36/month)
- Still secure with VPC endpoints
- SSM access maintained
- 57% cost savings

**For Learning**: Use Free Tier + no NAT ($23/month after free tier)
- Switch to t2.micro
- Remove NAT Gateway
- Keep VPC endpoints for SSM

---

*Prices based on Sydney (ap-southeast-2) region as of December 2024*
*Actual costs may vary based on usage patterns*
