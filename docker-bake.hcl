group "default" {
  targets = ["backend"]
}

target "backend" {
  context = "./"
  dockerfile = "Dockerfile"
  args = {
    NODE_VERSION = "1.0"
  }
  tags = ["app/backend:latest"]
}