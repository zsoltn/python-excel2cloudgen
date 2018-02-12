#!/bin/bash
source ./.ostackrc

TEST_KEYPAIR=`openstack keypair list 2>/dev/null | grep {{ cloudconfig.ssh_pub_key }} | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_KEYPAIR" = ""  ]; then
    nova keypair-add {{ cloudconfig.ssh_pub_key }}>{{ cloudconfig.ssh_pub_key }}.pem
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


# GYURIIIIIIIIIIIIIIIIIIIIIIIIIIIII EZ A PELDA !!!!!!
# GHODI + NZS temaplteing  
{% for  dict_item in secgroups%}
 
TEST_SECUGROUP=`openstack security group list 2>/dev/null | grep {{ dict_item['SECURITYGROUPNAME'] }} | awk -F ' | ' '{print $2}'|head -n 1`

if [ "$TEST_SECUGROUP" = ""  ]; then
    openstack security group create {{ dict_item['SECURITYGROUPNAME'] }}
    {% set PPS = (dict_item['PORTS'] |string ).split(',') %}
    #{{ PPS[1] }}
    {% for  P in PPS %}
        openstack security group rule create {{ dict_item['SECURITYGROUPNAME'] }}  --protocol {{ dict_item['SECURITYGROUPNAME'] }} --dst-port {{ P }} --remote-ip {{ dict_item['SOURCEIP'] }}
     {% endfor %}
    # openstack security group rule create {{ dict_item['SECURITYGROUPNAME'] }}  --protocol {{ dict_item['SECURITYGROUPNAME'] }} --dst-port {{ dict_item['PORTS'] }} --remote-ip {{ dict_item['SOURCEIP'] }}
fi
       
{% endfor %}

# {% for  key,dict_item in full["secgroups"].items()%}

# TEST_SECUGROUP=`openstack security group list 2>/dev/null | grep {{key}} | awk -F ' | ' '{print $2}'|head -n 1`

# if [ "$TEST_SECUGROUP" = ""  ]; then
    # openstack security group create {{ dict_item['SECURITYGROUPNAME'] }}
    # {% set PPS = (dict_item['PORTS'] |string ).split(',') %}
    # {{ PPS[1] }}
    # {% for  P in PPS %}
        # openstack security group rule create {{ dict_item['SECURITYGROUPNAME'] }}  --protocol {{ dict_item['SECURITYGROUPNAME'] }} --dst-port {{ P }} --remote-ip {{ dict_item['SOURCEIP'] }}
     # {% endfor %}
# fi
       
# {% endfor %}

{% for  dict_item in networks%}
#{% for  key,dict_item in full["networks"].items()%}

{% set LNETSUB = (dict_item['#NETWORK/SUBNET'] |string ).split('/') %}
{% set NNET = LNETSUB[0] %}
{% set NSUB = LNETSUB[1] %}

TEST_NET=`openstack network list 2>/dev/null | grep {{NNET}} | awk -F ' | ' '{print $2}'|head -n 1`

if [ "$TEST_NET" = ""  ]; then
    echo "Create Network: $NET"
    openstack network create {{NNET}}
fi

TEST_SUBNET=`openstack subnet list 2>/dev/null | grep {{NSUB}}  | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_SUBNET" = ""  ]; then
    echo "Create Subnet: $SUBNET"
    openstack subnet create --network {{NNET}} --subnet-range {{ dict_item['CIDR'] }}  {{NSUB}}
fi 

{% for  dict_item in instances%}
TEST_ROUTER=`openstack router list 2>/dev/null | grep {{ dict_item['#PROJECT NAME'] }}-{{NSUB}}-router | awk -F ' | ' '{print $2}'|head -n 1`
if [ "$TEST_ROUTER" = ""  ]; then
    echo "create router..."
    openstack router create {{ dict_item['#PROJECT NAME'] }}-{{NSUB}}-router
    echo "add subnet to router..."
    openstack router add subnet {{ dict_item['#PROJECT NAME'] }}-{{NSUB}}-router {{NSUB}}    
fi
{% endfor %}
 
{% endfor %}

# [{u'#PROJECT NAME': u'backendteam3',
                # u'#TEMPLATE': u'General - Python',
                # u'CLOUD': u'OTC',
                # u'CLOUD-INIT': u'# here the  cloud init code ',
                # u'ENGINE': u'TERRAFORM',
                # u'IP/NAME(s)': u'',
                # u'NETWORK': u'appnet1/mysubnet2',
                # u'PASSWORD(s)': u'',
                # u'SECGROUP': u'jump',
                # u'SIZE': 1.0,
                # u'TEMPLATE': u'General - Python',
                # u'USERNAME(s)': u'',
                # u'flavor_name': u'm1.large',
                # u'image_name': u'Standard_CentOS_7.3_latest'}]

{% for  dict_item in instances%}

{% set LNETSUB = (dict_item['NETWORK'] |string ).split('/') %}
{% set NNET = LNETSUB[0] %}
{% set NSUB = LNETSUB[1] %}


TEST_SERVER=`nova list 2>/dev/null | grep {{ dict_item['#PROJECT NAME'] }} | awk -F '|' '{print $3}'`
if [ "$TEST_SERVER" = ""  ]; then 
        echo "Test Server does not exists.. creating.."
        #NIC_BOOT=`neutron net-list | grep $NET | awk -F ' | ' '{print $2}'|head -n 1`
        NIC_BOOT=`openstack network list 2>/dev/null | grep {{NNET}} | awk -F ' | ' '{print $2}'|head -n 1`
        #echo openstack server create --flavor $FLAVOR --image $IMAGE --nic net-id=$NIC_BOOT --key-name $KEYNAME  $SERVER_NAME                
        echo nova boot --flavor {{ dict_item['flavor_name'] }}  --image {{ dict_item['image_name'] }} --nic net-id=$NIC_BOOT --key-name {{ cloudconfig.ssh_pub_key }} {{ dict_item['#PROJECT NAME'] }}        
        nova boot --flavor {{ dict_item['flavor_name'] }}  --image {{ dict_item['image_name'] }}  --nic net-id=$NIC_BOOT --key-name {{ cloudconfig.ssh_pub_key }}  {{ dict_item['#PROJECT NAME'] }}        
fi
{% endfor %}