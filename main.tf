# Create a new Web Droplet in the nyc2 region
resource "digitalocean_droplet" "web" {
  for_each = var.droplet_iothub


  name   = each.key
  size   = each.value.size
  image  = var.image
  region = each.value.region
  tags   = each.value.tags

  backups = true
  backup_policy {
    plan    = "weekly"
    weekday = "TUE"
    hour    = 8
  }
}