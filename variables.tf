
variable "do_token" {}

variable "droplet_iothub" {

  type = map(object({
    size   = string
    region = string
    tags   = list(string)
  }))

  default = {
    "vm_1" = {
      size   = "s-1vcpu-1gb"
      region = "nyc1"
      tags   = ["vm_1"]
    }
    "vm_2" = {
      size   = "s-1vcpu-1gb"
      region = "nyc1"
      tags   = ["vm_2"]
    }
  }

}

variable "image" {
  type        = string
  description = "so of the droplet"
  default     = "ubuntu-24-04-x64"
}