import os
from behave.fixture import use_fixture_by_tag

import docker

from features.fixtures import browser_chrome


def before_all(context):
    context.client = docker.from_env()
    context.container_tag = "zmq_proxy:latest"
    context.container_name = "zmq_proxy"
    context.image = context.client.images.build(path=".",
                                                platform="linux/arm/v6",
                                                tag=context.container_tag)


def after_scenario(context, step):
    try:
        # TODO: figure out why I can't .get with the python binding
        # context.client.containers.get(context.container_name).kill()
        os.system(f"docker kill {context.container_name} > /dev/null 2>&1")
    except docker.errors.NotFound:
        pass


fixture_registry = {
    "fixture.browser.chrome":  browser_chrome,
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
