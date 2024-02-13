import logging
import time

import yaml
from jinja2 import Environment, FileSystemLoader
import os
from helpers import create_ds, create_secret, destroy_secret, destroy_ds
import kopf

root_directory = os.path.dirname(os.path.abspath(__file__))
path = root_directory + "/templates"
env = Environment(
    loader=FileSystemLoader(f"{path}"),
    trim_blocks=True,
    autoescape=True,
    lstrip_blocks=True,
)


def get_agent(
    namespace,
    name,
    image_url,
    image_tag,
    manager_host,
    worker_host,
    memory_limits,
    cpu_limits,
    group,
    logger: logging.Logger,
):
    logger.info("Preparing Wazuh agent DaemonSet in %s", namespace)
    ds_template = env.get_template("ds.jinja2")
    agent = ds_template.render(
        namespace=namespace,
        name=name,
        image_url=image_url,
        image_tag=image_tag,
        manager_host=manager_host,
        worker_host=worker_host,
        memory_limits=memory_limits,
        cpu_limits=cpu_limits,
        group=group,
    )
    return agent


def get_secret(namespace, name, api_user, api_password, logger: logging.Logger):
    logger.info("Preparing Wazuh credentials in %s", namespace)
    secret_template = env.get_template("secret.jinja2")
    secret = secret_template.render(
        namespace=namespace,
        name=name,
        api_user=api_user,
        api_password=api_password,
    )
    return secret


@kopf.on.startup()
def configure(settings: kopf.OperatorSettings, **_):
    settings.persistence.progress_storage = kopf.SmartProgressStorage()
    settings.watching.connect_timeout = 1 * 60
    settings.watching.server_timeout = 10 * 60


@kopf.on.login()
def login(**kwargs):
    return kopf.login_via_client(**kwargs)


@kopf.on.cleanup()
def cleanup(logger: logging.Logger, **kwargs):
    logger.info("Cleaning up in 3s...", kwargs)
    time.sleep(3)


@kopf.on.create("opennix.io", "v1", "wazuh-agent")
def create_resources(spec, namespace, logger: logging.Logger, **kwargs):
    logger.info(
        "Starting deployment process for Wazuh resources in %s for creation event",
        namespace,
    )
    logger.debug("Wazuh Agent operator kwargs %s", kwargs)
    image_url = spec["image_url"] or None
    image_tag = spec["image_tag"] or None
    manager_host = spec["manager_host"] or None
    worker_host = spec["worker_host"] or manager_host
    api_user = spec["api_username"] or None
    api_password = spec["api_password"] or None
    name = spec["name"] or None
    memory_limits = spec["memory_limits"] or None
    cpu_limits = spec["cpu_limits"] or None
    group = spec["group"]
    generate_agent = get_agent(
        namespace=namespace,
        name=name,
        image_url=image_url,
        image_tag=image_tag,
        manager_host=manager_host,
        worker_host=worker_host,
        memory_limits=memory_limits,
        cpu_limits=cpu_limits,
        group=group,
        logger=logger,
    )
    generate_secret = get_secret(
        namespace=namespace,
        name=name,
        api_user=api_user,
        api_password=api_password,
        logger=logger,
    )
    agent = create_ds(yaml.safe_load(generate_agent))
    logger.info(
        "Wazuh Agent DaemonSet has been created in %s. resource name %s.",
        namespace,
        agent,
    )
    secret = create_secret(yaml.safe_load(generate_secret))
    logger.info(
        "Wazuh Agent Secret has been created in %s. resource name %s.",
        namespace,
        secret,
    )


@kopf.on.update("opennix.io", "v1", "wazuh-agent")
def update_fn(spec, old, new, namespace, diff, status, logger, **kwargs):
    logger.debug("Wazuh Agent operator kwargs %s. for update event", kwargs)
    image_url = spec["image_url"] or None
    image_tag = spec["image_tag"] or None
    manager_host = spec["manager_host"] or None
    worker_host = spec["worker_host"] or manager_host
    name = spec["name"] or None
    api_user = spec["api_username"] or None
    api_password = spec["api_password"] or None
    memory_limits = spec["memory_limits"] or None
    cpu_limits = spec["cpu_limits"] or None
    group = spec["group"] or None
    logger.info(
        "Got an update request: %s. Diff: %s. Status: %s.", new, list(diff), status
    )
    if not (
        old["spec"]["api_password"] == new["spec"]["api_password"]
        and old["spec"]["api_username"] == new["spec"]["api_username"]
    ):
        generate_secret = get_secret(
            namespace=namespace,
            name=name,
            api_user=api_user,
            api_password=api_password,
            logger=logger,
        )
        destroy_secret(yaml.safe_load(generate_secret))
        create_secret(yaml.safe_load(generate_secret))

    else:
        generate_agent = get_agent(
            namespace=namespace,
            name=name,
            image_url=image_url,
            image_tag=image_tag,
            manager_host=manager_host,
            worker_host=worker_host,
            memory_limits=memory_limits,
            cpu_limits=cpu_limits,
            group=group,
            logger=logger,
        )
        destroy_ds(yaml.safe_load(generate_agent))
        create_ds(yaml.safe_load(generate_agent))


@kopf.on.delete("opennix.io", "v1", "wazuh-agent")
def delete(body, spec, namespace, logger, **kwargs):
    logger.debug("Wazuh Agent operator kwargs %s. for destroy event", kwargs)
    msg = "Operator {} and its children deleted".format(body["metadata"]["name"])
    image_url = spec["image_url"] or None
    image_tag = spec["image_tag"] or None
    manager_host = spec["manager_host"] or None
    worker_host = spec["worker_host"] or manager_host
    name = spec["name"] or None
    api_user = spec["api_username"] or None
    api_password = spec["api_password"] or None
    memory_limits = spec["memory_limits"] or None
    cpu_limits = spec["cpu_limits"] or None
    group = spec["group"] or None
    generate_agent = get_agent(
        namespace=namespace,
        name=name,
        image_url=image_url,
        image_tag=image_tag,
        manager_host=manager_host,
        worker_host=worker_host,
        memory_limits=memory_limits,
        cpu_limits=cpu_limits,
        group=group,
        logger=logger,
    )
    generate_secret = get_secret(
        namespace=namespace,
        name=name,
        api_user=api_user,
        api_password=api_password,
        logger=logger,
    )
    agent = destroy_ds(yaml.safe_load(generate_agent))
    logger.info(
        "Wazuh Agent DaemonSet has been deleted in %s. resource name %s.",
        namespace,
        agent,
    )
    secret = destroy_secret(yaml.safe_load(generate_secret))
    logger.info(
        "Wazuh Agent Secret has been created in %s. resource name %s.",
        namespace,
        secret,
    )
    return {"message": msg}
