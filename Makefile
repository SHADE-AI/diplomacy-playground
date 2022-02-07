REPO_ORG ?= tacc
GAMESERVER_REPO ?= diplomacy_server
WEBUI_REPO ?= diplomacy_webui

GAMESERVER_REPO_DOCKER ?= $(REPO_ORG)/$(GAMESERVER_REPO)
WEBUI_REPO_DOCKER ?= $(REPO_ORG)/$(WEBUI_REPO)

build: webui gameserver

gameserver:
	docker build -f Dockerfile.server -t $(GAMESERVER_REPO_DOCKER) .

webui:
	docker build -f Dockerfile.webui -t $(WEBUI_REPO_DOCKER) .

images:
	docker push $(GAMESERVER_REPO_DOCKER) && \
	docker push $(WEBUI_REPO_DOCKER)
