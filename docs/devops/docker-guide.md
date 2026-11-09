# Docker Commands Cheat Sheet

Docker packages an application and its dependencies into an image. A running instance of that image is a container. Images are stored in repositories, and repositories are hosted by a registry.

> **Modern Docker note:** Current Docker installations use the `docker compose` plugin. The older `docker-compose` binary still appears in existing documentation and scripts, but new examples should use `docker compose`. Compose file `version:` keys are obsolete in Compose v2.

## Registry and repository

- A **repository** is a hosted collection of related images, usually with multiple tags.
- A **registry** is the server that hosts repositories and exposes an HTTP API.
- Docker Hub is the default public registry.
- Verify image sources before using them in production. Prefer trusted, maintained images and pin versions.

### Registry commands

| Command | Description |
| --- | --- |
| `docker login` | Log in to a registry. |
| `docker logout` | Log out from a registry. |
| `docker search <term>` | Search a registry for images. |
| `docker pull <image[:tag]>` | Pull an image from a registry to the local machine. |
| `docker push <repository[:tag]>` | Push a local image to a registry. |

Examples:

```bash
docker login registry.example.test
docker search nginx
docker pull nginx:1.27
docker tag myapp:1.0 registry.example.test/team/myapp:1.0
docker push registry.example.test/team/myapp:1.0
docker logout registry.example.test
```

## Images

Images are read-only templates used to create containers. They are built from layers.

| Command | Description |
| --- | --- |
| `docker images` | List local images. |
| `docker image ls` | List local images using the newer command group. |
| `docker build -t <name:tag> <path>` | Build an image from a Dockerfile. |
| `docker history <image>` | Show the layer history of an image. |
| `docker tag <source> <target>` | Tag an image with a new name. |
| `docker rmi <image>` | Remove an image. |
| `docker import <file>` | Create an image from a tarball. |
| `docker save <image> > <file>` | Save an image, including its layers and tags, to a tar archive. |
| `docker load < <file>` | Load an image from a tar archive. |
| `docker commit <container> <image>` | Create an image from a container. |
| `docker export <container>` | Export a container filesystem as a tar stream. |

Examples:

```bash
docker images
docker build -t myapp:1.0 .
docker tag myapp:1.0 registry.example.test/team/myapp:1.0
docker history myapp:1.0
docker rmi myapp:1.0

docker save myapp:1.0 | gzip > myapp-1.0.tar.gz
docker load < myapp-1.0.tar.gz

docker export my_container | gzip > my_container.tar.gz
cat my_container.tar.gz | docker import - my_image:my_tag
```

`docker save` preserves image layers and history. `docker export` exports only a container filesystem, so the imported image does not retain the original build history.

## Containers

A container is an isolated process created from an image.

| Command | Description |
| --- | --- |
| `docker create <image>` | Create a container without starting it. |
| `docker run <image>` | Create and start a container. |
| `docker start <container>` | Start a stopped container. |
| `docker stop <container>` | Stop a running container. |
| `docker restart <container>` | Stop and start a container. |
| `docker pause <container>` | Pause a running container. |
| `docker unpause <container>` | Resume a paused container. |
| `docker rename <old> <new>` | Rename a container. |
| `docker rm <container>` | Remove a container. |
| `docker update <container>` | Update a container's resource limits. |
| `docker ps` | List running containers. |
| `docker ps -a` | List running and stopped containers. |
| `docker logs <container>` | Show container logs. |
| `docker inspect <container>` | Show detailed container information, including network settings. |
| `docker port <container>` | Show published ports for a container. |
| `docker top <container>` | Show processes running inside a container. |
| `docker stats` | Show live resource usage for running containers. |
| `docker diff <container>` | Show filesystem changes in a container. |
| `docker cp <source> <destination>` | Copy files between a container and the host. |
| `docker exec <container> <command>` | Run a command inside a running container. |
| `docker wait <container>` | Block until the container exits. |
| `docker kill <container>` | Send `SIGKILL` to a container. |
| `docker attach <container>` | Attach to a running container. |

Examples:

```bash
docker run -d --name web -p 8080:80 nginx:1.27
docker ps
docker ps -a
docker logs -f web
docker inspect web
docker exec -it web /bin/sh
docker stop web
docker rm web
```

### Common run options

```bash
# Keep a container running in the background with a pseudo-TTY
docker run -td <image>

# Remove the container automatically when it stops
docker run --rm <image>

# Mount a host directory into the container
docker run -v "$PWD/data:/app/data" <image>

# Remove the container and its anonymous volumes
docker rm -v <container>

# Use a specific logging driver
docker run --log-driver=syslog <image>

# Limit CPU shares (relative weight; 1024 is the default)
docker run -it -c 512 <image>

# Restrict the container to specific CPU cores
docker run -it --cpuset-cpus=0,4,6 <image>

# Set a memory limit
docker run -it -m 300M ubuntu:24.04 /bin/bash

# Add a Linux capability and device
docker run --rm -it --cap-add SYS_ADMIN --device /dev/fuse <image>

# Pass through a single device
docker run -it --device=/dev/ttyUSB0 debian bash
```

Use `--privileged` only when absolutely necessary. It gives the container broad access to host devices and kernel capabilities.

```bash
docker run -it --privileged -v /dev/bus/usb:/dev/bus/usb debian bash
```

## Dockerfile instructions

A Dockerfile is a text file that defines how an image is built. Use a code editor with Dockerfile syntax highlighting, such as VS Code, Vim, Emacs, Sublime Text, or TextMate.

| Instruction | Purpose |
| --- | --- |
| `FROM` | Set the base image for the build. |
| `LABEL` | Add metadata such as maintainer, version, or description. Use this instead of the deprecated `MAINTAINER`. |
| `RUN` | Execute a command in a new layer and commit the result. |
| `CMD` | Provide the default command or arguments for the container. |
| `ENTRYPOINT` | Configure the container to run as an executable. |
| `EXPOSE` | Document the port the container listens on. It does not publish the port. |
| `COPY` | Copy files or directories from the build context. |
| `ADD` | Copy files, directories, or remote URLs. Prefer `COPY` unless `ADD` behavior is needed. |
| `ENV` | Set environment variables for the build and runtime. |
| `ARG` | Define a build-time variable. |
| `WORKDIR` | Set the working directory for later instructions. |
| `USER` | Set the user for later instructions and the container process. |
| `VOLUME` | Declare a mount point for external or persistent data. |
| `HEALTHCHECK` | Define a command that checks container health. |
| `SHELL` | Change the default shell used by `RUN`, `CMD`, and `ENTRYPOINT`. |
| `STOPSIGNAL` | Set the signal used to stop the container. |
| `ONBUILD` | Register an instruction to run when the image is used as a base. |

Example Dockerfile:

```dockerfile
FROM python:3.12-slim

LABEL org.opencontainers.image.title="example-api"
LABEL org.opencontainers.image.version="1.0"

ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"

ENTRYPOINT ["python", "-m", "app"]
```

Keep images small by using multi-stage builds, a `.dockerignore` file, and minimal base images. Pin base-image versions and run the application as a non-root user where possible.

## Networks

Docker networks let containers communicate. The modern built-in driver types include `bridge`, `host`, `none`, `overlay`, `macvlan`, and `ipvlan`.

By default, a new container is attached to the bridge network. Containers on the same user-defined bridge network can communicate by container name.

| Command | Description |
| --- | --- |
| `docker network create <name>` | Create a network. The default driver is `bridge`. |
| `docker network ls` | List networks. |
| `docker network inspect <name>` | Show detailed network information. |
| `docker network connect <network> <container>` | Connect a container to a network. |
| `docker network disconnect <network> <container>` | Disconnect a container from a network. |
| `docker network rm <name>` | Remove a network. Remove connected containers first. |
| `docker network prune` | Remove unused networks. |

Examples:

```bash
docker network create app-net
docker run -d --name app --network app-net example/app:1.0
docker run -d --name redis --network app-net redis:7
docker network inspect app-net
docker network disconnect app-net app
docker network rm app-net
```

## Volumes

Volumes provide persistent storage managed by Docker. Named volumes are independent of a container's lifecycle.

| Command | Description |
| --- | --- |
| `docker volume create <name>` | Create a volume. |
| `docker volume ls` | List volumes. |
| `docker volume inspect <name>` | Show volume details. |
| `docker volume rm <name>` | Remove a volume. |
| `docker volume prune` | Remove unused volumes. |

Examples:

```bash
docker volume create app-data
docker run -d --name app -v app-data:/var/lib/app example/app:1.0
docker volume ls
docker volume inspect app-data
docker volume rm app-data
```

Bind mounts map an existing host path into a container:

```bash
docker run --rm -v "$PWD/config:/app/config:ro" example/app:1.0
```

Use bind mounts for local development and named volumes for persistent application data. Back up important volumes before pruning.

## Container interaction

```bash
# Run a command in a running container
docker exec -ti <container> /bin/bash

# Follow container logs with timestamps
docker logs -ft <container>

# Save a running container as an image
docker commit -m "commit message" -a "author" <container> <username>/<image>:<tag>
```

## Build commands

```bash
# Build and tag an image
docker build -t myapp:1.0 .

# Build without using the cache
docker build --no-cache -t myapp:1.0 .

# List local images
docker images

# Remove an image
docker rmi alpine:3.20
```

## Cleanup

Cleanup commands can delete data. Review the target resources first.

```bash
# Remove dangling images
docker image prune

# Remove all unused images, not just dangling images
docker image prune -a

# Remove unused containers, networks, images, and build cache
docker system prune

# Include unused volumes
docker system prune --volumes

# Remove all stopped containers
docker rm $(docker ps -a -q)

# Remove all local images
docker rmi $(docker images -q)

# Stop all running containers
docker kill $(docker ps -q)
```

Use `docker system df` to review disk usage before cleaning up.

## Docker Swarm

Swarm is Docker's built-in orchestration mode. Kubernetes is more common for large production platforms, but Swarm commands are still useful to learn.

```bash
# Initialize a swarm on the manager node
docker swarm init --advertise-addr <manager-ip>

# Join as a manager
docker swarm join --token <manager-token> <manager-ip>:2377

# Join as a worker
docker swarm join --token <worker-token> <manager-ip>:2377

# List nodes
docker node ls
```

### Services

```bash
# Create a service with three replicas
docker service create --replicas 3 -p 80:80 --name web nginx:1.27

# List services
docker service ls

# Inspect service tasks
docker service ps web

# Scale a service
docker service scale web=5

# Show service logs
docker service logs web
```

### Stacks

```bash
# Deploy a stack from a Compose file
docker stack deploy -c compose.yaml mystack

# List stack services
docker stack services mystack

# Remove a stack
docker stack rm mystack

# Leave a swarm
docker swarm leave
```

Remove all containers from a node before attempting to leave a swarm where the node is a manager.

## Docker Compose

Compose defines and runs multi-container applications from a YAML file. Current Docker uses `docker compose`; the legacy command was `docker-compose`.

| Command | Description |
| --- | --- |
| `docker compose up` | Create and start services in the foreground. |
| `docker compose up -d` | Start services in detached mode. |
| `docker compose down` | Stop and remove containers, networks, and default resources created by `up`. |
| `docker compose start` | Start existing containers. |
| `docker compose stop` | Stop running containers without removing them. |
| `docker compose restart` | Restart services. |
| `docker compose pause` | Pause services. |
| `docker compose unpause` | Resume paused services. |
| `docker compose ps` | List project containers. |
| `docker compose logs` | Show service logs. |
| `docker compose logs -f` | Follow service logs. |
| `docker compose build` | Build service images. |
| `docker compose pull` | Pull service images. |
| `docker compose -f <file> up` | Use a specific Compose file. |

Examples:

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose stop
docker compose down
```

`docker compose down -v` also removes named volumes declared by the project. Use it only when you intend to delete persistent data.

### Basic Compose example

```yaml
services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    depends_on:
      - redis

  redis:
    image: redis:7
```

The Compose `version:` key from older examples is obsolete in Compose v2. Omit it in new files.

### Compose reference

#### Build or image

```yaml
services:
  web:
    build: .
    # build using a custom Dockerfile
    build:
      context: ./dir
      dockerfile: Dockerfile.dev
    # or use an image instead
    image: ubuntu:24.04
```

#### Ports

```yaml
services:
  web:
    ports:
      - "3000"
      - "8000:80"
    # expose to linked services without publishing to the host
    expose:
      - "3000"
```

#### Commands

```yaml
services:
  web:
    command: bundle exec thin -p 3000
    # or exec-form
    command: ["bundle", "exec", "thin", "-p", "3000"]
    # override the entrypoint
    entrypoint: /app/start.sh
```

#### Environment variables

```yaml
services:
  web:
    environment:
      RACK_ENV: development
      APP_MODE: test
    env_file:
      - .env
      - .development.env
```

Do not commit files containing real credentials. Use a secret manager or an untracked local environment file.

#### Dependencies

```yaml
services:
  web:
    links:
      - db:database
      - redis
    depends_on:
      - db

  db:
    image: postgres:16
```

`links` is a legacy feature. Prefer Compose service names and shared networks for service discovery. `depends_on` controls startup order but does not guarantee application readiness; use health checks or retry logic.

#### Volumes and extension

```yaml
services:
  web:
    extends:
      file: common.yml
      service: webapp
    volumes:
      - /var/lib/mysql
      - ./_data:/var/lib/mysql
```

## Best practices

- Pin image tags instead of using `latest` for reproducible deployments.
- Verify image sources and scan images for vulnerabilities.
- Use multi-stage builds and `.dockerignore` to reduce image size.
- Run containers as a non-root user.
- Add health checks and resource limits.
- Keep secrets out of Dockerfiles, image layers, Compose files, and Git.
- Prefer named volumes for persistent data and bind mounts for development.
- Review cleanup commands before running them; `prune` and `rm` operations can delete data.
- Use the modern `docker compose` command in new documentation.
- Back up volumes before upgrades or destructive changes.

## Quick reference

```bash
# Images
docker images
docker build -t myapp:1.0 .
docker pull nginx:1.27
docker push registry.example.test/team/myapp:1.0
docker rmi myapp:1.0

# Containers
docker run -d --name web -p 8080:80 nginx:1.27
docker ps
docker ps -a
docker logs -f web
docker exec -it web /bin/sh
docker stop web
docker rm web

# Networks
docker network create app-net
docker network ls
docker network inspect app-net

# Volumes
docker volume create app-data
docker volume ls
docker volume inspect app-data

# Compose
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down

# Cleanup
docker system df
docker image prune
docker system prune
```

## Further reading

- [Docker documentation](https://docs.docker.com/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Docker Compose reference](https://docs.docker.com/compose/)
- [Docker Hub](https://hub.docker.com/)
