---
name: infrastructure-as-code
description: >
  PLACEHOLDER SKILL: Use this skill when implementing infrastructure using
  Terraform, Pulumi, or other IaC tools. Currently a placeholder for future
  expansion when IaC is adopted in this project.
  Trigger keywords: Terraform, Pulumi, IaC, infrastructure as code, HCL,
  state management, provider, module.
---

# Infrastructure as Code

> **PLACEHOLDER**: This skill will be expanded when Infrastructure as Code
> (Terraform/Pulumi) is adopted in this project.

---

## Expansion Triggers

This skill should be expanded when:

- Terraform files (`*.tf`) are added to the repository
- Pulumi projects are created (`Pulumi.yaml`)
- Cloud provider infrastructure is required (AWS, GCP, Azure)
- Infrastructure provisioning becomes part of the deployment pipeline

---

## Future Content Outline

When expanded, this skill will include:

| Section | Content |
|---------|---------|
| Provider Configuration | AWS, GCP, Azure setup patterns |
| State Management | Remote backends, locking, workspaces |
| Module Structure | Reusable module design guidelines |
| Resource Naming | Naming conventions and tagging standards |
| Security | Secret handling, IAM policies, least privilege |
| CI/CD Integration | Plan/apply workflows, drift detection |

---

## Basic IaC Principles

Core concepts for future reference:

1. **Declarative Configuration** - Define desired end-state, not procedures
2. **State Tracking** - Infrastructure state stored and versioned
3. **Idempotent Operations** - Same input produces same result
4. **Version Control** - All infrastructure code in Git
5. **Immutable Infrastructure** - Replace rather than modify resources
6. **Blast Radius Limitation** - Scope changes to minimize risk

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [kubernetes-deployment](../kubernetes-deployment/SKILL.md) | IaC provisions the cluster K8s deploys to |
| [deployment-strategies](../deployment-strategies/SKILL.md) | IaC enables blue-green infrastructure |
