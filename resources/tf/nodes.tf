# Create a node server
resource "digitalocean_droplet" "node1" {
  image = "ubuntu-16-04-x64"
  name = "node1"
  region = "nyc1"
  size = "512mb"
}


