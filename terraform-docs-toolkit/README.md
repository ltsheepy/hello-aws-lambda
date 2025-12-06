# Terraform AWS Documentation Toolkit

Automatically generate comprehensive documentation for your Terraform AWS infrastructure.

## Features

- 📊 **Architecture Diagrams** - Auto-generated from Terraform state with official AWS icons
- 💰 **Cost Breakdown** - Real-time cost analysis by resource
- 🔒 **Security Reports** - Patch compliance, Security Hub findings
- 📋 **Compliance Mapping** - AWS WAF, CIS Controls v8, NIST 800-53
- 📝 **Auto-updating README** - Always in sync with infrastructure

## Installation

### Option 1: Git Submodule (Recommended)

```bash
# Add to your Terraform project
git submodule add https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git .terraform-docs
cd .terraform-docs
pip3 install -r requirements.txt
```

### Option 2: Direct Clone

```bash
# Clone into your project
git clone https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git .terraform-docs
cd .terraform-docs
pip3 install -r requirements.txt
```

### Option 3: Copy Files

```bash
# Download and extract
curl -L https://github.com/YOUR_USERNAME/terraform-docs-toolkit/archive/main.zip -o docs-toolkit.zip
unzip docs-toolkit.zip -d .terraform-docs
```

## Quick Start

### 1. Add to Your Project

```bash
# In your Terraform project root
git submodule add https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git .terraform-docs
```

### 2. Create Makefile

Add this to your project's `Makefile`:

```makefile
include .terraform-docs/Makefile.include

# Your existing targets...
```

### 3. Generate Documentation

```bash
make docs
```

That's it! Your documentation is generated.

## Usage

### Generate All Documentation

```bash
make docs
```

This creates:
- `README.md` (updated with costs and resources)
- `SECURITY.md` (security and compliance report)
- `architecture.png` (visual diagram)
- `architecture-metadata.json` (resource inventory)

### Individual Reports

```bash
make docs-diagram        # Architecture diagram only
make docs-security       # Security report only
make docs-costs          # Cost breakdown only
```

### Configuration

Create `.terraform-docs/config.yaml` in your project:

```yaml
# Optional configuration
region: ap-southeast-2
project_name: my-project

# Cost estimation
pricing_region: ap-southeast-2

# Diagram settings
diagram:
  format: png
  show_costs: true
  
# Security settings
security:
  enable_security_hub: true
  enable_compliance_mapping: true
  frameworks:
    - aws_waf
    - cis_v8
    - nist_800_53
```

## What Gets Generated

### Architecture Diagram
- Visual representation of your infrastructure
- Official AWS icons
- VPC layout, subnets, instances
- Security groups and endpoints
- Auto-generated from Terraform state

### Cost Breakdown
- Per-resource cost analysis
- Hourly, monthly, and annual costs
- Cost by category (compute, storage, networking)
- Optimization recommendations
- Free services highlighted

### Security Report
- Patch compliance status
- Security Hub findings by severity
- Compliance framework mappings:
  - AWS Well-Architected Framework
  - CIS Controls v8
  - NIST 800-53 Rev 5
- Remediation guidance
- Quick action commands

### Architecture Metadata
- Machine-readable JSON
- Resource inventory
- Instance details
- VPC configuration
- Timestamps

## Requirements

- Python 3.9+
- Terraform
- AWS CLI configured
- Graphviz (for diagrams)

```bash
# macOS
brew install python3 graphviz
pip3 install diagrams boto3 pyyaml

# Linux
apt-get install python3 python3-pip graphviz
pip3 install diagrams boto3 pyyaml
```

## Project Structure

```
your-terraform-project/
├── .terraform-docs/          # This toolkit (submodule)
│   ├── bin/
│   │   ├── generate_diagram.py
│   │   ├── generate_security.py
│   │   ├── generate_costs.py
│   │   └── update_readme.py
│   ├── lib/
│   │   ├── compliance_mappings.py
│   │   ├── cost_calculator.py
│   │   └── terraform_parser.py
│   ├── templates/
│   │   ├── README.template.md
│   │   └── SECURITY.template.md
│   ├── Makefile.include
│   └── requirements.txt
├── main.tf
├── variables.tf
├── Makefile                  # Include .terraform-docs/Makefile.include
├── README.md                 # Auto-updated
├── SECURITY.md               # Auto-generated
└── architecture.png          # Auto-generated
```

## Examples

### Basic Usage

```bash
# After infrastructure changes
terraform apply
make docs
git add .
git commit -m "Update infrastructure and docs"
git push
```

### CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Update Documentation

on:
  push:
    paths:
      - '**.tf'

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r .terraform-docs/requirements.txt
          sudo apt-get install graphviz
      
      - name: Generate docs
        run: make docs
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Commit docs
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add README.md SECURITY.md architecture.png architecture-metadata.json
          git commit -m "docs: Update documentation [skip ci]" || exit 0
          git push
```

## Customization

### Custom Templates

Override default templates by creating:
- `docs/README.template.md`
- `docs/SECURITY.template.md`

### Custom Cost Pricing

Create `docs/pricing.yaml`:

```yaml
# Custom pricing (overrides defaults)
ec2:
  t3.micro: 0.015
  t3.small: 0.030

ebs:
  gp3_per_gb: 0.096

vpc_endpoint:
  hourly: 0.01
```

### Custom Compliance Mappings

Extend `docs/compliance.yaml`:

```yaml
# Add custom compliance mappings
custom_findings:
  CUSTOM.1:
    title: "Custom security check"
    waf: ["SEC-01"]
    cis_v8: ["1.1"]
    nist_800_53: ["AC-1"]
```

## Troubleshooting

### Diagram not generating
```bash
# Check Graphviz installation
dot -V

# Reinstall if needed
brew reinstall graphviz  # macOS
```

### Security report empty
```bash
# Ensure Security Hub is enabled
aws securityhub enable-security-hub --region YOUR_REGION

# Run initial patch scan
aws ssm send-command \
  --document-name AWS-RunPatchBaseline \
  --targets Key=tag:PatchGroup,Values=production \
  --parameters Operation=Scan
```

### Cost calculation incorrect
```bash
# Update pricing data
python3 .terraform-docs/bin/update_pricing.py
```

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests
4. Submit a pull request

## License

MIT License - see LICENSE file

## Support

- 📖 [Documentation](https://github.com/YOUR_USERNAME/terraform-docs-toolkit/wiki)
- 🐛 [Issues](https://github.com/YOUR_USERNAME/terraform-docs-toolkit/issues)
- 💬 [Discussions](https://github.com/YOUR_USERNAME/terraform-docs-toolkit/discussions)

---

**Made with ❤️ for the Terraform community**
