import kopf
import pykube

from .k8s_client import kubernetes_api, create_k8s_client

api = kubernetes_api()

k8s_client = create_k8s_client().CustomObjectsApi()
core_api = create_k8s_client().CoreV1Api()


def destroy_ds(template):
    kopf.adopt(template)
    ds = pykube.DaemonSet(api, template)
    ds.delete()
    return ds


def destroy_secret(template):
    kopf.adopt(template)
    secret = pykube.Secret(api, template)
    secret.delete()
    return secret
