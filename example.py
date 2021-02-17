import os
import kopf
import kubernetes
import yaml

@kopf.on.create('machines')
def create_controller(spec, name, namespace, logger, **kwargs):

    switch_pos = spec.get('SwitchPosition')
    if not switch_pos:
        raise kopf.PermanentError(f"SwitchPosition must be set. Got {switch_pos!r}.")

    machine_patch = {'spec': {'SwitchPosition': 'down'}}

    api = kubernetes.client.CoreV1Api()
    crds = kubernetes.client.CustomObjectsApi()
    obj =  crds.patch_namespaced_custom_object("useless.container.training", 
                                        "v1alpha1", 
                                        namespace, 
                                        "machines", 
                                        name, 
                                        machine_patch)

    logger.info(f"Switch is flipped: %s", obj)
