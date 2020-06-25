#!/bin/bash
# docker login ascdso-gitlab.local:4567
set -xe

declare -a images=("consul"
    "postgres:alpine"
    "vault"
    "secfigo/bandit"
    "secfigo/retirejs"
    "secfigo/trufflehog"
    "sonarqube:alpine"
    "hadolint/hadolint"
    "williamyeh/ansible:alpine3"
    "owasp/dependency-check"
    "owasp/zap2docker-stable"
    "arminc/clair-db:latest"
    "arminc/clair-local-scan:v2.0.1"
    "docker/docker-bench-security"
    )

for image in "${images[@]}"
do
    echo "Processing image: $image"
    docker pull "$image"
    sleep 2
    docker image tag "$image" ascdso.gitlab.local:4567/root/django.nv/"$image"
    docker push ascdso.gitlab.local:4567/root/django.nv/"$image"
done
