#!/bin/bash

if [ $# -lt 2 ]; then
    echo "usage: $0 <action> <credentialsfile> <options>"
    exit 1
fi

ACTION=$1
CREDENTIALS=$2
OPTIONS=$3

while read line; do
    username=$(echo ${line} | cut -f2 -d:)
    password=$(echo ${line} | cut -f3 -d:)
    domain=$(echo ${line} | cut -f1 -d:)
    terraform  ${ACTION} ${OPTIONS} -var="username=${username}" -var="password=${password}" -var="domain_name=${domain}"  -state="${username}-${domain}.state" -var="ssh_pub_key=sshkeys/id_rsa.${username:4:6}.pub"  -var="user_no=${username:4:6}"
done < ${CREDENTIALS}
