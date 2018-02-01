resource "openstack_compute_keypair_v2" "keypair" {
  name       = "${var.project}-pubkey-2"
  public_key = "${file("${var.ssh_pub_key}")}"
  lifecycle {
        ignore_changes = ["ami"]
    }
}
