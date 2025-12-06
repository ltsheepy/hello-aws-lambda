#!/bin/bash
# Create terraform-docs-toolkit repository

set -e

echo "🚀 Creating Terraform AWS Documentation Toolkit Repository"
echo ""

# Get current directory
CURRENT_DIR=$(pwd)
PARENT_DIR=$(dirname "$CURRENT_DIR")
TOOLKIT_DIR="$PARENT_DIR/terraform-docs-toolkit"

# Check if toolkit directory already exists
if [ -d "$TOOLKIT_DIR" ]; then
    echo "⚠️  Directory $TOOLKIT_DIR already exists"
    read -p "Remove and recreate? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$TOOLKIT_DIR"
    else
        echo "❌ Aborted"
        exit 1
    fi
fi

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$TOOLKIT_DIR"/{bin,lib,templates,examples}

# Copy scripts to bin/
echo "📋 Copying scripts..."
cp generate_diagram_dynamic.py "$TOOLKIT_DIR/bin/generate_diagram.py"
cp generate_security_report.py "$TOOLKIT_DIR/bin/generate_security.py"
cp update_readme.py "$TOOLKIT_DIR/bin/update_readme.py"

# Copy library files
cp compliance_mappings.py "$TOOLKIT_DIR/lib/"

# Copy toolkit configuration files
cp terraform-docs-toolkit/README.md "$TOOLKIT_DIR/"
cp terraform-docs-toolkit/requirements.txt "$TOOLKIT_DIR/"
cp terraform-docs-toolkit/setup.py "$TOOLKIT_DIR/"
cp terraform-docs-toolkit/Makefile.include "$TOOLKIT_DIR/"
cp terraform-docs-toolkit/install.sh "$TOOLKIT_DIR/"
cp terraform-docs-toolkit/.gitignore "$TOOLKIT_DIR/"

# Make install script executable
chmod +x "$TOOLKIT_DIR/install.sh"

# Create LICENSE file
cat > "$TOOLKIT_DIR/LICENSE" << 'EOF'
MIT License

Copyright (c) 2024 Terraform AWS Documentation Toolkit

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Create example project
echo "📝 Creating example project..."
mkdir -p "$TOOLKIT_DIR/examples/basic-ec2"

cat > "$TOOLKIT_DIR/examples/basic-ec2/main.tf" << 'EOF'
# Example Terraform configuration
# This demonstrates the documentation toolkit

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

# Example EC2 instance
resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "example-instance"
  }
}
EOF

cat > "$TOOLKIT_DIR/examples/basic-ec2/README.md" << 'EOF'
# Example: Basic EC2 Instance

This example demonstrates using the Terraform AWS Documentation Toolkit.

## Setup

1. Add the toolkit as a submodule:
   ```bash
   git submodule add https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git .terraform-docs
   ```

2. Include in your Makefile:
   ```makefile
   include .terraform-docs/Makefile.include
   ```

3. Generate documentation:
   ```bash
   make docs
   ```

## What Gets Generated

- `README.md` - Updated with costs and resources
- `SECURITY.md` - Security and compliance report
- `architecture.png` - Visual diagram
- `architecture-metadata.json` - Resource inventory
EOF

# Create CONTRIBUTING.md
cat > "$TOOLKIT_DIR/CONTRIBUTING.md" << 'EOF'
# Contributing to Terraform AWS Documentation Toolkit

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git
cd terraform-docs-toolkit

# Install dependencies
pip3 install -r requirements.txt

# Run tests
python3 -m pytest tests/
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Testing

Please add tests for new features:

```python
# tests/test_feature.py
def test_new_feature():
    # Your test here
    pass
```

## Documentation

Update README.md if you:
- Add new features
- Change configuration options
- Modify installation steps

## Questions?

Open an issue or start a discussion!
EOF

# Initialize git repository
echo "🔧 Initializing git repository..."
cd "$TOOLKIT_DIR"
git init

# Create .gitattributes for better diffs
cat > .gitattributes << 'EOF'
*.py diff=python
*.md diff=markdown
*.tf diff=terraform
EOF

git add .
git commit -m "Initial commit: Terraform AWS Documentation Toolkit

Features:
- 📊 Auto-generate architecture diagrams from Terraform state
- 💰 Real-time cost breakdown by resource
- 🔒 Security & compliance reports
- 📋 Compliance framework mapping (AWS WAF, CIS v8, NIST 800-53)
- 🔍 Patch compliance tracking
- 📝 Auto-updating README
- 🤖 Fully automated with make commands

Installation:
- Git submodule support
- One-line installer
- Works with any Terraform AWS project

Documentation:
- Comprehensive README
- Example projects
- Contributing guidelines
"

echo ""
echo "✅ Repository created at: $TOOLKIT_DIR"
echo ""
echo "📤 Next steps:"
echo ""
echo "1. Create GitHub repository:"
echo "   cd $TOOLKIT_DIR"
echo "   gh repo create terraform-docs-toolkit --public --source=. --remote=origin --push"
echo ""
echo "2. Or push to existing remote:"
echo "   cd $TOOLKIT_DIR"
echo "   git remote add origin https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git"
echo "   git push -u origin main"
echo ""
echo "3. Update URLs in README.md and install.sh with your GitHub username"
echo ""
echo "📚 Repository contents:"
ls -la "$TOOLKIT_DIR"
echo ""
echo "🎉 Ready to publish!"
