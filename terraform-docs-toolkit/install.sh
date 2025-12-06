#!/bin/bash
# Install Terraform Documentation Toolkit into a project

set -e

echo "🚀 Installing Terraform Documentation Toolkit..."
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not in a git repository"
    echo "   Run this from your Terraform project root"
    exit 1
fi

# Check if Terraform files exist
if [ ! -f "*.tf" ] && [ -z "$(ls *.tf 2>/dev/null)" ]; then
    echo "⚠️  Warning: No Terraform files found in current directory"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Add as git submodule
echo "📦 Adding toolkit as git submodule..."
if [ -d ".terraform-docs" ]; then
    echo "⚠️  .terraform-docs directory already exists"
    read -p "Remove and reinstall? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .terraform-docs
    else
        exit 1
    fi
fi

git submodule add https://github.com/YOUR_USERNAME/terraform-docs-toolkit.git .terraform-docs

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
cd .terraform-docs
pip3 install -r requirements.txt
cd ..

# Install Graphviz if needed
if ! command -v dot &> /dev/null; then
    echo "📊 Installing Graphviz..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install graphviz
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y graphviz
    else
        echo "⚠️  Please install Graphviz manually: https://graphviz.org/download/"
    fi
fi

# Update Makefile
echo "📝 Updating Makefile..."
if [ ! -f "Makefile" ]; then
    cat > Makefile << 'EOF'
.PHONY: help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Include documentation toolkit
include .terraform-docs/Makefile.include

# Your Terraform targets
init: ## Initialize Terraform
	terraform init

plan: ## Show Terraform plan
	terraform plan

apply: ## Apply Terraform changes
	terraform apply

destroy: ## Destroy all resources
	terraform destroy
EOF
    echo "✅ Created Makefile"
else
    if ! grep -q "include .terraform-docs/Makefile.include" Makefile; then
        echo "" >> Makefile
        echo "# Include documentation toolkit" >> Makefile
        echo "include .terraform-docs/Makefile.include" >> Makefile
        echo "✅ Updated Makefile"
    else
        echo "ℹ️  Makefile already includes toolkit"
    fi
fi

# Update .gitignore
echo "🙈 Updating .gitignore..."
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Terraform
.terraform/
*.tfstate
*.tfstate.*
*.tfstate.backup
.terraform.lock.hcl
*.zip

# Generated documentation (optional - commit if you want)
# architecture.png
# architecture-metadata.json
EOF
    echo "✅ Created .gitignore"
else
    echo "ℹ️  .gitignore exists (not modified)"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📚 Next steps:"
echo ""
echo "1. Generate documentation:"
echo "   make docs"
echo ""
echo "2. View available commands:"
echo "   make help"
echo ""
echo "3. Commit the changes:"
echo "   git add ."
echo "   git commit -m 'Add documentation toolkit'"
echo "   git push"
echo ""
echo "📖 Full documentation: .terraform-docs/README.md"
