env = input("Enter environment (dev/prod): ").strip().lower()

if env == "prod":
    server_count = 3
    instance_type = "t3.medium"
    allowed_ports = [22, 80, 443]
else:
    server_count = 1
    instance_type = "t3.micro"
    allowed_ports = [22]

tags = {
    "Owner": "amit",
    "Project": "tfvars-engine",
    "Environment": env
}

with open("../terraform/terraform.tfvars", "w") as f:
    f.write(f'env = "{env}"\n\n')
    f.write(f'server_count = {server_count}\n')
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
print(f"Instance type   : {instance_type}")
print(f"Allowed ports   : {allowed_ports}")
print(f"Tags            : {tags}")
