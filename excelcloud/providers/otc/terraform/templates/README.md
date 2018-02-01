# Terraform for Hack Zurich

## Quickstart

1. Install Terraform from https://www.terraform.io
2. Clone this repository via `git clone https://github.com/OpenTelekomCloud/hack_zurich.git`
3. Switch to terraform directory `cd hack_zurich/terraform`
4. Initialize Terraform provider via `terraform init`
5. Insert your login information into `parameter.tvars`
6. Check if everything looks good with `terraform plan -var-file=parameter.tvars`
7. Apply the changes via `terraform apply -var-file=parameter.tvars`
