#!/bin/bash
source ./.ostackrc

TEST_SERVER=`nova list 2>/dev/null | grep $SERVER_NAME | awk -F '|' '{print $3}'`

if [ "$TEST_SERVER" != ""  ]; then
    echo "Test Server exists: $SERVER_NAME deleting.."
    openstack server delete --wait  $SERVER_NAME 
else
    echo "Test Server" $TEST_SERVER " not exists"
fi

openstack router remove subnet $SERVER_NAME-${SUBNET}-router $SUBNET
openstack router delete $SERVER_NAME-${SUBNET}-router
#neutron router-interface-delete $SERVER_NAME-${SUBNET}-router $SUBNET
#neutron router-delete $SERVER_NAME-${SUBNET}-router


openstack port delete $SERVER_NAME-$NET
openstack subnet delete $SUBNET

openstack router delete $SERVER_NAME-${SUBNET}-router 
openstack network delete $NET
openstack keypair delete $KEYNAME

openstack security group delete $SECGROUP


#neutron subnet-delete $SUBNET
#neutron port-delete $SERVER_NAME-$NET
#neutron router-delete $SERVER_NAME-${SUBNET}-router 
#neutron net-delete $NET 
#nova keypair-delete $KEYNAME