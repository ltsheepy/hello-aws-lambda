.PHONY: help init plan apply destroy diagram clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## Initialize Terraform
	terraform init

plan: ## Show Terraform plan
	terraform plan

apply: ## Apply Terraform changes
	terraform apply

destroy: ## Destroy all resources
	terraform destroy

diagram: ## Generate architecture diagram and update README
	@echo "📊 Generating architecture diagram..."
	@python3 generate_diagram_dynamic.py
	@echo "📝 Updating README with costs and resources..."
	@python3 update_readme.py
	@echo "✅ Architecture documentation updated"

security-report: ## Generate security and compliance report
	@echo "🔒 Generating security report..."
	@python3 generate_security_report.py
	@echo "✅ Security report updated"

readme: diagram security-report ## Generate all reports and update README
	@echo ""
	@echo "✅ All documentation generated:"
	@echo "   - README.md (updated)"
	@echo "   - SECURITY.md"
	@echo "   - architecture.png"
	@echo "   - architecture-metadata.json"
	@echo ""
	@echo "📋 Summary:"
	@test -f architecture-metadata.json && cat architecture-metadata.json | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"   Resources: {d['resources']['instances']} instances, {d['resources']['vpc_endpoints']} endpoints\")" || echo "   No metadata available"
	@echo ""
	@echo "💡 Next steps:"
	@echo "   git add ."
	@echo "   git commit -m 'Update documentation'"
	@echo "   git push"

validate: ## Validate Terraform configuration
	@echo "🔍 Validating Terraform..."
	terraform validate
	terraform fmt -check
	@echo "✅ Validation passed"

format: ## Format Terraform files
	@echo "✨ Formatting Terraform files..."
	terraform fmt -recursive
	@echo "✅ Formatted"

lint: ## Run TFLint
	@echo "🔍 Running TFLint..."
	@command -v tflint >/dev/null 2>&1 || { echo "Installing tflint..."; brew install tflint; }
	tflint --init
	tflint --recursive
	@echo "✅ Linting passed"

security: ## Run security scans (tfsec)
	@echo "🔒 Running security scans..."
	@command -v tfsec >/dev/null 2>&1 || { echo "Installing tfsec..."; brew install tfsec; }
	tfsec . --minimum-severity MEDIUM
	@echo "✅ Security scan passed"

security-full: ## Run comprehensive security scans
	@echo "🔒 Running comprehensive security scans..."
	@command -v tfsec >/dev/null 2>&1 || { echo "Installing tfsec..."; brew install tfsec; }
	@command -v checkov >/dev/null 2>&1 || { echo "Installing checkov..."; pip3 install checkov; }
	@echo ""
	@echo "Running tfsec..."
	tfsec . --format default
	@echo ""
	@echo "Running checkov..."
	checkov -d . --framework terraform --quiet
	@echo ""
	@echo "✅ All security scans completed"

check: validate lint security ## Run all checks (validate, lint, security)

clean: ## Clean generated files
	rm -f architecture.png
	rm -f *.zip

all: init apply readme ## Initialize, apply, and generate all documentation
