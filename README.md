# Terraform tfvars Generation Engine

> Automating Terraform inputs using a Python-based decision engine

---

## Overview

Terraform is excellent at provisioning infrastructure, but managing
`terraform.tfvars` manually becomes repetitive, error-prone, and hard to
scale as environments grow.

This project demonstrates a **clean, automated approach** where:

- Terraform remains **pure and declarative**
- A Python engine dynamically **generates Terraform inputs**
- Infrastructure decisions are **environment-aware and reproducible**

This is **not** a “create EC2” demo.  
It focuses on **automation, separation of concerns, and real DevOps patterns**.

---

## Problem Statement

In real-world Terraform projects:

- Teams manually edit `terraform.tfvars`
- Different environments (dev / prod) need different configurations
- Complex variables (lists, maps, tags, ports) are common
- Logic slowly leaks into Terraform code

This leads to:
- Duplication
- Human error
- Poor automation
- Hard-to-maintain infrastructure code

---

## Solution Approach

This project introduces a **tfvars generation engine**:

- User provides **high-level input** (environment)
- Python decides **infrastructure parameters**
- Python generates a **valid `terraform.tfvars` file**
- Terraform consumes the file without knowing how it was created

Terraform does **only one job**: provisioning infrastructure.



