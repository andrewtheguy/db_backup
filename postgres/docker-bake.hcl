variable "TAG" {
}

variable "IMAGE_NAME" {
    default="ghcr.io/andrewtheguy/pg_backup"
}


group "default" {
    targets = ["worker"]
}

target "worker" {
    dockerfile = "Dockerfile"
    # both the tag and latest
    tags = ["${IMAGE_NAME}:${TAG}","${IMAGE_NAME}"]
}

target "worker_multi" {
    inherits = ["worker"]
    platforms = ["linux/amd64", "linux/arm64"]
}


group "image-all" {
    targets = ["worker_multi"]
}