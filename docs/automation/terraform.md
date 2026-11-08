# Terraform Foundations

Terraform is an infrastructure-as-code tool. Configuration describes desired resources; providers translate that configuration into API operations for a platform.

## Core concepts

- **Provider:** plugin that communicates with a platform or service API.
- **Resource:** an object Terraform manages, such as a network, VM, or DNS record.
- **Variable:** an input used to parameterize configuration.
- **Output:** a value exposed after planning or applying, such as an assigned address.
- **Plan:** a proposed set of changes for review.
- **State:** Terraform's record of managed resources and their relationship to configuration.
- **Module:** reusable Terraform configuration with inputs and outputs.

## Typical workflow

```text
terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

Review the plan before applying changes. State may contain sensitive values, so use an approved remote backend with access control, encryption, and locking for shared environments. Do not commit secrets or production state files to a public repository.

## Safe learning exercise

Start with a local-only or sandbox configuration, add one small resource, inspect the plan, apply it, verify the result, and destroy the learning resource when finished. Confirm the target account and region before every apply or destroy operation.

## Further reading

- [Terraform language documentation](https://developer.hashicorp.com/terraform/language)
- [Terraform CLI documentation](https://developer.hashicorp.com/terraform/cli)
