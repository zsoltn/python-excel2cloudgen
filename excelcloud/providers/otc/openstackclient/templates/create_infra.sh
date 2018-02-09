#!/bin/bash
source ./.ostackrc

TEST_KEYPAIR=`openstack keypair list 2>/dev/null | grep $KEYNAME | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_KEYPAIR" = ""  ]; then
    nova keypair-add $KEYNAME>$KEYNAME.pem
fi
{% for  dict_item in secgroups%}
 
TEST_SECUGROUP=`openstack security group list 2>/dev/null | grep {{key}} | awk -F ' | ' '{print $2}'|head -n 1`

if [ "$TEST_SECUGROUP" = ""  ]; then
    openstack security group create {{ dict_item['SECURITYGROUPNAME'] }}
    {% set PPS = (dict_item['PORTS'] |string ).split(',') %}
    {{ PPS[1] }}
    {% for  P in PPS %}
        openstack security group rule create {{ dict_item['SECURITYGROUPNAME'] }}  --protocol {{ dict_item['SECURITYGROUPNAME'] }} --dst-port {{ P }} --remote-ip {{ dict_item['SOURCEIP'] }}
     {% endfor %}
    openstack security group rule create {{ dict_item['SECURITYGROUPNAME'] }}  --protocol {{ dict_item['SECURITYGROUPNAME'] }} --dst-port {{ dict_item['PORTS'] }} --remote-ip {{ dict_item['SOURCEIP'] }}
fi
       
{% endfor %}


TEST_SECUGROUP=`openstack security group list 2>/dev/null | grep $SECGROUP | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_SECUGROUP" = ""  ]; then
    openstack security group create $SECGROUP
    openstack security group rule create $SECGROUP --protocol $SECGROUPTYPE --dst-port $PORTS --remote-ip $SOURCEIP
fi

TEST_NET=`openstack network list 2>/dev/null | grep $NET | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_NET" = ""  ]; then
    echo "Create Network: $NET"
    openstack network create $NET
fi

TEST_SUBNET=`openstack subnet list 2>/dev/null | grep $SUBNET | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_SUBNET" = ""  ]; then
    echo "Create Subnet: $SUBNET"
    openstack subnet create --network $NET --subnet-range $CIDR  $SUBNET
fi
 
TEST_ROUTER=`openstack router list 2>/dev/null | grep $SERVER_NAME-${SUBNET}-router | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_ROUTER" = ""  ]; then
    echo "create router..."
    openstack router create $SERVER_NAME-${SUBNET}-router
    echo "add subnet to router..."
    openstack router add subnet $SERVER_NAME-${SUBNET}-router $SUBNET    
fi

TEST_SERVER=`nova list 2>/dev/null | grep $SERVER_NAME | awk -F '|' '{print $3}'`
if [ "$TEST_SERVER" = ""  ]; then 
        echo "Test Server does not exists.. creating.."
        #NIC_BOOT=`neutron net-list | grep $NET | awk -F ' | ' '{print $2}'|head -n 1`
        NIC_BOOT=`openstack network list 2>/dev/null | grep $NET | awk -F ' | ' '{print $2}'|head -n 1`
        #echo openstack server create --flavor $FLAVOR --image $IMAGE --nic net-id=$NIC_BOOT --key-name $KEYNAME  $SERVER_NAME                
        echo nova boot --flavor $FLAVOR --image $IMAGE --nic net-id=$NIC_BOOT --key-name $KEYNAME  $SERVER_NAME        
        nova boot --flavor $FLAVOR --image $IMAGE --nic net-id=$NIC_BOOT --key-name $KEYNAME  $SERVER_NAME        
fi