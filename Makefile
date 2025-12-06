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
	terraform validate
	terraform fmt -check

format: ## Format Terraform files
	terraform fmt -recursive

clean: ## Clean generated files
	rm -f architecture.png
	rm -f *.zip

all: init apply readme ## Initialize, apply, and generate all documentation
