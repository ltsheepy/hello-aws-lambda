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
	python3 generate_diagram_dynamic.py
	python3 update_readme.py

validate: ## Validate Terraform configuration
	terraform validate
	terraform fmt -check

format: ## Format Terraform files
	terraform fmt -recursive

docs: diagram ## Generate all documentation
	@echo "✅ Documentation generated!"
	@echo "   - architecture.png"
	@echo "   - architecture-metadata.json"
	@echo "   - README.md (updated)"

clean: ## Clean generated files
	rm -f architecture.png
	rm -f *.zip

security-report: ## Generate security and compliance report
	python3 generate_security_report.py

all: init apply diagram security-report ## Initialize, apply, generate diagram and security report
