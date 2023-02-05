DOCKER_CONTAINER_LIST := $(shell docker ps -a -q)
DOCKER_IMAGES_LIST := $(shell docker images -a -q)


run:
	docker compose up

## Remove dependencies created when running the application.
clear:
	@echo 'Deletando buckets MinIO'
	@sudo rm -rf minio/data
	@echo 'Deletando containers e imagens do projeto'
	@if [ -n "$(DOCKER_CONTAINER_LIST)" ]; then \
		docker stop "$(DOCKER_CONTAINER_LIST)"; \
        docker rm "$(DOCKER_CONTAINER_LIST)"; \
		docker rmi "$(DOCKER_IMAGES_LIST)"; \
    fi
	