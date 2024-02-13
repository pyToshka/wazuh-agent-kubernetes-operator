import os

import kubernetes
import pykube
from kubernetes.config import ConfigException


def kubernetes_api():
    try:
        config = pykube.KubeConfig.from_env()
    except FileNotFoundError:
        config = pykube.KubeConfig.from_file(os.getenv("KUBECONFIG", "~/.kube/config"))
    api = pykube.HTTPClient(config)
    return api


def create_k8s_client():
    try:
        kubernetes.config.load_incluster_config()
    except ConfigException:
        kubernetes.config.load_kube_config()
    kubernetes.client.configuration.assert_hostname = False
    return kubernetes.client
