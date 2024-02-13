help:
	@echo 'Usage: make COMMAND'
	@echo 'Commands :'
	@grep -E '[a-zA-Z\.\-]+:.*?@ .*$$' $(MAKEFILE_LIST)| tr -d '#' | awk 'BEGIN {FS = ':.*?@ '}; {printf '\033[32m%-34s\033[0m - %s\n', $$1, $$2}'

#create-kind-cluster-arm: @ Create kind cluster for MacOS ARM
create-kind-cluster-arm:
	DOCKER_DEFAULT_PLATFORM='linux/arm64' kind create cluster --config tests/kind.yml

#create-kind-cluster: @ Create kind cluster X86
create-kind-cluster:
	kind create cluster --config tests/kind.yml

#delete-kind-cluster: @ Create kind cluster
delete-kind-cluster:
	kind delete cluster -n wazuh-agent

#build-kind-node-image: @ Create kind cluster
build-kind-node-image:
	kind build node-image

#run-operator: @ Run operator locally
run-operator:
	kopf run -v --dev  main.py

#e2e-tests: @ Run operator locally
e2e-tests:
	docker build -t wazuh-operator .
	DOCKER_DEFAULT_PLATFORM='linux/arm64' kubectl kuttl test --config tests/kind.yml -v 1
