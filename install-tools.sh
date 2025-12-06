#!/bin/bash
# Install security and linting tools for Terraform

set -e

echo "🔧 Installing Terraform Security & Linting Tools"
echo "================================================"
echo ""

# Check OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    PKG_MGR="brew"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    PKG_MGR="apt"
else
    echo "❌ Unsupported OS"
    exit 1
fi

# Install tflint
echo "📦 Installing tflint..."
if command -v tflint &> /dev/null; then
    echo "✅ tflint already installed ($(tflint --version))"
else
    if [ "$PKG_MGR" = "brew" ]; then
        brew install tflint
    else
        curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash
    fi
    echo "✅ tflint installed"
fi

# Install tfsec
echo "📦 Installing tfsec..."
if command -v tfsec &> /dev/null; then
    echo "✅ tfsec already installed ($(tfsec --version))"
else
    if [ "$PKG_MGR" = "brew" ]; then
        brew install tfsec
    else
        curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
    fi
    echo "✅ tfsec installed"
fi

# Install checkov
echo "📦 Installing checkov..."
if command -v checkov &> /dev/null; then
    echo "✅ checkov already installed ($(checkov --version))"
else
    pip3 install checkov
    echo "✅ checkov installed"
fi

# Install terraform-docs (optional but useful)
echo "📦 Installing terraform-docs..."
if command -v terraform-docs &> /dev/null; then
    echo "✅ terraform-docs already installed"
else
    if [ "$PKG_MGR" = "brew" ]; then
        brew install terraform-docs
    else
        curl -sSLo ./terraform-docs.tar.gz https://terraform-docs.io/dl/v0.16.0/terraform-docs-v0.16.0-$(uname)-amd64.tar.gz
        tar -xzf terraform-docs.tar.gz
        chmod +x terraform-docs
        sudo mv terraform-docs /usr/local/bin/
        rm terraform-docs.tar.gz
    fi
    echo "✅ terraform-docs installed"
fi

# Initialize tflint plugins
echo "🔌 Initializing tflint plugins..."
tflint --init

echo ""
echo "✅ All tools installed successfully!"
echo ""
echo "📋 Installed tools:"
echo "   - tflint: $(tflint --version | head -n1)"
echo "   - tfsec: $(tfsec --version)"
echo "   - checkov: $(checkov --version)"
echo "   - terraform-docs: $(terraform-docs --version 2>/dev/null || echo 'installed')"
echo ""
echo "🚀 Usage:"
echo "   make lint          # Run TFLint"
echo "   make security      # Run tfsec"
echo "   make security-full # Run tfsec + checkov"
echo "   make check         # Run all checks"
echo ""
