import docker


def before_all(context):
    context.client = docker.from_env()
    context.container_tag = "zmq_proxy:latest"
    context.container_name = "zmq_proxy"
    context.image = context.client.images.build(path=".",
                                                tag=context.container_tag)


def after_scenario(context, step):
    try:
        context.client.containers.get(context.container_name).kill()
    except docker.errors.NotFound:
        pass


# -- REGISTRY DATA SCHEMA 1: fixture_func
fixture_registry1 = {
    "fixture.browser.chrome":  browser_chrome,
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
