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
