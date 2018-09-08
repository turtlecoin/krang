# Use a test key generated in ~./ssh. Be sure to delete and script the generation and checking
resource "digitalocean_ssh_key" "do_ssh_keys" {
  name       = "tfkey"
  public_key = "${file("~/.ssh/tfkey.pub")}"
}

# Create a TRTL daemon server - Start with one then figure out how to increment the name and use the same info - also use more variables for changing values in furture
resource "digitalocean_droplet" "trtldmn1" {
  image = "docker-16-04"
  name = "trtldmn1"
  region = "nyc1"
  size = "512mb"
  ssh_keys = ["43:68:ff:14:66:20:d0:e3:cd:89:09:a2:51:71:98:74"]
  provisioner "remote-exec" {
    inline = [ "apt-get -y update && apt-get install -y python-minimal python-pip && pip install 'docker-py>=1.7.0' 'docker-compose>=1.7.0'" ]
    connection {
      type = "ssh"
      user = "root"
      private_key = "${file("~/.ssh/tfkey")}"
    }
  }
}

# OUTPUT THE IP ADDRESS FOR ANSIBLE TO WORK ON 
output "address_web" { 
  value = "${digitalocean_droplet.trtldmn1.ipv4_address}"
  }
