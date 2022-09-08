target "docker-metadata-action" {}

target "build" {
  inherits = ["docker-metadata-action"]
  args = {
    BUILDX_EXPERIMENTAL = 1
  }
  context = "./"
  dockerfile = "docker/Dockerfile"
  platforms = [
    "linux/amd64",
    "linux/arm/v6",
    "linux/arm/v7",
    "linux/arm64",
    "linux/386"
  ]
}