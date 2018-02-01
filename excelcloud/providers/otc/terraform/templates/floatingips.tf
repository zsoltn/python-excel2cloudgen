resource "openstack_networking_floatingip_v2" "fip" {
  count = "${var.jumphost_count}"
  pool  = "${var.external_network}"
}
