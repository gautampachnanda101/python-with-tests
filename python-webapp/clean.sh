#!/bin/sh

# Stop and remove any existing containers
docker-compose down --remove-orphans || true

# Prune unused Docker volumes
docker volume prune -f --all
