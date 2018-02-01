output "address" {
  value = "${element(openstack_networking_floatingip_v2.fip.*.address)}"
}
