reason = {}
env = input("Enter environment (dev/prod): ").strip().lower()
reason["environment"] = f"user selected {env} environment"

if env == "prod":
    server_count = 3
    ami_id = "ami-0abcdef1234567890"
    instance_type = "t3.medium"
    allowed_ports = [22, 80, 443]
    reason["server_count"] = "Production requires high availability (minimum 3 servers)"
    reason["instance_type"] = "Production workloads need more resources"
    reason["ami_id"] = "Using a specific AMI for production stability"
    reason["allowed_ports"] = "Production servers need to allow HTTP and HTTPS traffic"
elif env == "dev":
    server_count = 1
    instance_type = "t3.micro"
    allowed_ports = [22]
    reason["server_count"] = "Development can run on a single server"
    reason["instance_type"] = "Development workloads are lightweight"
    reason["allowed_ports"] = "Development only needs SSH access"
    reason["ami_id"] = "Using default AMI for development flexibility"
else:
    print("Invalid environment. Please enter 'dev' or 'prod'.")
    exit(1)

tags = {
    "Owner": "amit",
    "Project": "tfvars-engine",
    "Environment": env
}
reason["tags"] = "Standardized tagging for resource management"

with open("../terraform/terraform.tfvars", "w") as f:
    f.write(f'env = "{env}"\n\n')
    f.write(f'server_count = {server_count}\n')
    f.write(f'ami_id = "{ami_id}"\n\n')
    f.write(f'instance_type = "{instance_type}"\n\n')

    # list
    f.write("allowed_ports = [")
    f.write(", ".join(str(p) for p in allowed_ports))
    f.write("]\n\n")

    # map
    f.write("tags = {\n")
    for k, v in tags.items():
        f.write(f'  {k} = "{v}"\n')
    f.write("}\n")

print("\nterraform.tfvars generated successfully")
print(f"Environment     : {env}")
print(f"Server count    : {server_count}")
print(f"AMI ID         : {ami_id}")
print(f"Instance type   : {instance_type}")
print(f"Allowed ports   : {allowed_ports}")
print(f"Tags            : {tags}")

with open("../EXPLANATION.md", "w") as f:
    f.write("# Infrastructure Explanation\n\n")
    f.write("This file explains **why** the infrastructure was configured this way.\n\n")

    for key, reason in reason.items():
        f.write(f"## {key}\n")
        f.write(f"{reason}\n\n")

