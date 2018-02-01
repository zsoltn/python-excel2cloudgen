export OS_USERNAME="{{ username }}"
export OS_USER_DOMAIN_NAME="{{ domain_name }}"
export OS_USER_ID=
export OS_PASSWORD="{{ password }}"
export OS_TENANT_NAME=eu-de
export OS_PROJECT_NAME=eu-de
export OS_AUTH_URL=https://iam.eu-de.otc.t-systems.com/v3
export OS_PROJECT_DOMAIN_NAME=
export OS_TENANT_NAME=eu-de
export OS_PROJECT_NAME=eu-de
export OS_IDENTITY_API_VERSION=3
export OS_VOLUME_API_VERSION=2
export OS_IMAGE_API_VERSION=2
export OS_ENDPOINT_TYPE=publicURL
export NOVA_ENDPOINT_TYPE=publicURL
export CINDER_ENDPOINT_TYPE=publicURL

export SERVER_NAME={{ project }}
export FLAVOR={{ flavor_name }}
export IMAGE={{ image_name }}
{% set net_subnet = NETWORK.split('/') %}export NET={{ net_subnet[0] }}
export SUBNET={{ net_subnet[1] }}
export KEYNAME={{ project }}-key
export CIDR={{ CIDR }}
export AZ={{ az }}
export SECGROUP={{ SECURITYGROUPNAME }}
export SECGROUPTYPE={{ SECGROUPTYPE }}
export PORTS={{ PORTS }}
export SOURCEIP={{ SOURCEIP }}






