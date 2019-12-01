dockerhub-url = <SOME DOCKERHUB URL>
container-name := <SOME CONTAINER NAME>
container-tag := $(container-name):$(shell date -u +%Y%m%d_%H%M%SZ)

build:
	docker build -t $(container-name) -t $(container-tag) -t $(dockerhub-url)/$(container-tag) .
push: build
	docker push $(dockerhub-url)/$(container-tag)
