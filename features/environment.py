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


fixture_registry = {
    "fixture.browser.chrome":  browser_chrome,
}


def before_tag(context, tag):
    if tag.startswith("fixture."):
        return use_fixture_by_tag(tag, context, fixture_registry)
