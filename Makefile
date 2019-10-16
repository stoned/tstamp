NAME?=		stoned/tstampapp
VERSION?=	1.6
IMAGE?=		$(NAME):$(VERSION)
DOCKER_HUB_TAG?=	$(VERSION)

POD?=		$(notdir $(CURDIR))

PODMAN?=	podman
COMPOSE?=	podman-compose
PIPENV?=	pipenv

ifneq (,$(HTTP_PROXY))
build_args+=	--build-arg HTTP_PROXY=$(HTTP_PROXY)
endif
ifneq (,$(HTTPS_PROXY))
build_args+=	--build-arg HTTPS_PROXY=$(HTTPS_PROXY)
endif
ifneq (,$(http_proxy))
build_args+=	--build-arg http_proxy=$(http_proxy)
endif
ifneq (,$(https_proxy))
build_args+=	--build-arg https_proxy=$(https_proxy)
endif

all: build

build: FORCE requirements.txt
	$(PODMAN) build $(build_args) -t $(NAME):$(VERSION) .

dev: FORCE
	FLASK_APP=tstamp.py flask run

up: FORCE
	$(COMPOSE) up -d

down: FORCE
	$(COMPOSE) down

podrm:
	set -e; $(PODMAN) pod exists $(POD) && { \
	  pods=$$($(PODMAN) ps -f label=io.podman.compose.project=$(POD) -a --format='{{.ID}}'); \
	  test -n "$$pods" && $(PODMAN) stop $$pods; \
	  test -n "$$pods" && $(PODMAN) rm $$pods; \
	  $(PODMAN) pod rm $(POD); \
	}

run: FORCE
	$(PODMAN) run -ti --rm -P $(IMAGE)

push-to-docker:
	podman push $(IMAGE) docker://docker.io/$(NAME):$(DOCKER_HUB_TAG)

Pipfile.lock: Pipfile
	$(PIPENV) lock

requirements.txt: Pipfile.lock
	$(PIPENV) lock -r > $@ || { rm -f $@; exit 1; }

clean: FORCE
	find . -name "*.pyc" -delete

FORCE:
