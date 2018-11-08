NAME?=		stoned/tstampapp
VERSION?=	1.2

DOCKER?=	docker
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

build: FORCE
	$(DOCKER) build $(build_args) -t $(NAME):$(VERSION) .
	$(DOCKER) tag $(NAME):$(VERSION) $(NAME):latest

dev:
	FLASK_APP=tstamp.py flask run

run:
	$(DOCKER) run -ti --rm -P $(NAME):latest

Pipfile.lock: Pipfile
	$(PIPENV) lock

requirements.txt: Pipfile.lock
	$(PIPENV) lock -r > $@ || { rm -f $@; exit 1; }

FORCE:
