import pulumi
import pulumi_gcp as gcp
from pulumi_gcp import container
from pulumi import get_stack

def create_gke_cluster_and_node_pool():
    env_name = get_stack()
    project_id = gcp.config.project

    # Generate a valid cluster name
    cluster_name = f"airxp-{env_name}-gke".lower().replace("_", "-")

    airxp_dev_gke = gcp.container.Cluster("airxp_dev_gke",
    default_max_pods_per_node=110,
    default_snat_status={
        "disabled": False,
    },
    location="us-west1",
    name=cluster_name,
    node_config={
        "advanced_machine_features": {
            "threads_per_core": 0,
        },
        "disk_size_gb": 64,
        "disk_type": "pd-balanced",
        "ephemeral_storage_local_ssd_config": {
            "local_ssd_count": 0,
        },
        "image_type": "COS_CONTAINERD",
        "kubelet_config": {
            "insecure_kubelet_readonly_port_enabled": "TRUE",
        },
        "labels": {
            "kubezero.zero-downtime.net/ingress.public": "true",
        },
        "linux_node_config": {
            "cgroup_mode": "CGROUP_MODE_V2",
            "sysctls": {
                "vm.max_map_count": "262144",
            },
        },
        "logging_variant": "DEFAULT",
        "machine_type": "c3-standard-4",
        "metadata": {
            "disable-legacy-endpoints": "true",
        },
        "oauth_scopes": [
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/logging.write",
            "https://www.googleapis.com/auth/monitoring",
            "https://www.googleapis.com/auth/service.management.readonly",
            "https://www.googleapis.com/auth/servicecontrol",
            "https://www.googleapis.com/auth/trace.append",
        ],
        "resource_labels": {
            "goog-gke-node-pool-provisioning-model": "on-demand",
        },
        "service_account": "default",
        "tags": ["ingress"],
        "workload_metadata_config": {
            "mode": "GKE_METADATA",
        },
    },
    node_locations=[
        "us-west1-a",
        "us-west1-b",
        "us-west1-c",
    ],
    node_pool_defaults={
        "node_config_defaults": {
            "insecure_kubelet_readonly_port_enabled": "TRUE",
            "logging_variant": "DEFAULT",
        },
    },
    node_pools=[
        {
            "autoscaling": {
                "location_policy": "BALANCED",
                "max_node_count": 3,
            },
            "initial_node_count": 1,
            "max_pods_per_node": 110,
            "name": "default-ingress2",
            "node_config": {
                "advanced_machine_features": {
                    "threads_per_core": 0,
                },
                "disk_size_gb": 64,
                "disk_type": "pd-balanced",
                "ephemeral_storage_local_ssd_config": {
                    "local_ssd_count": 0,
                },
                "image_type": "COS_CONTAINERD",
                "kubelet_config": {
                    "insecure_kubelet_readonly_port_enabled": "TRUE",
                },
                "labels": {
                    "kubezero.zero-downtime.net/ingress.public": "true",
                },
                "linux_node_config": {
                    "cgroup_mode": "CGROUP_MODE_V2",
                    "sysctls": {
                        "vm.max_map_count": "262144",
                    },
                },
                "logging_variant": "DEFAULT",
                "machine_type": "c3-standard-4",
                "metadata": {
                    "disable-legacy-endpoints": "true",
                },
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/trace.append",
                ],
                "resource_labels": {
                    "goog-gke-node-pool-provisioning-model": "on-demand",
                },
                "service_account": "default",
                "tags": ["ingress"],
                "workload_metadata_config": {
                    "mode": "GKE_METADATA",
                },
            },
            "node_count": 2,
            "node_locations": [
                "us-west1-a",
                "us-west1-b",
                "us-west1-c",
            ],
            "placement_policy": {
                "type": "",
            },
            "queued_provisioning": {
                "enabled": False,
            },
            "management": {
                "auto_repair": True,
                "auto_upgrade": False,
            },
            "upgrade_settings": {
                "max_surge": 1,
            },
            "version": "1.34.4-gke.1130000",
        },
        {
            "autoscaling": {
                "location_policy": "ANY",
                "max_node_count": 1,
            },
            "initial_node_count": 1,
            "max_pods_per_node": 110,
            "name": "gpu-t4-large",
            "node_config": {
                "advanced_machine_features": {
                    "threads_per_core": 0,
                },
                "disk_size_gb": 64,
                "disk_type": "pd-balanced",
                "ephemeral_storage_local_ssd_config": {
                    "local_ssd_count": 0,
                },
                "guest_accelerators": [{
                    "count": 1,
                    "gpu_driver_installation_config": {
                        "gpu_driver_version": "DEFAULT",
                    },
                    "gpu_sharing_config": {
                        "gpu_sharing_strategy": "TIME_SHARING",
                        "max_shared_clients_per_gpu": 2,
                    },
                    "type": "nvidia-tesla-t4",
                }],
                "image_type": "COS_CONTAINERD",
                "kubelet_config": {
                    "insecure_kubelet_readonly_port_enabled": "TRUE",
                },
                "logging_variant": "DEFAULT",
                "machine_type": "custom-8-20480",
                "metadata": {
                    "disable-legacy-endpoints": "true",
                },
                "oauth_scopes": [
                    "https://www.googleapis.com/auth/devstorage.read_only",
                    "https://www.googleapis.com/auth/logging.write",
                    "https://www.googleapis.com/auth/monitoring",
                    "https://www.googleapis.com/auth/service.management.readonly",
                    "https://www.googleapis.com/auth/servicecontrol",
                    "https://www.googleapis.com/auth/trace.append",
                ],
                "resource_labels": {
                    "goog-gke-accelerator-type": "nvidia-tesla-t4",
                    "goog-gke-node-pool-provisioning-model": "on-demand",
                },
                "service_account": "default",
                "workload_metadata_config": {
                    "mode": "GKE_METADATA",
                },
            },
            "node_count": 1,
            "node_locations": [
                "us-west1-a",
                "us-west1-b",
            ],
            "placement_policy": {
                "type": "",
            },
            "queued_provisioning": {
                "enabled": False,
            },
            "management": {
                "auto_repair": True,
                "auto_upgrade": False,
            },
            "upgrade_settings": {
                "max_surge": 1,
            },
            "version": "1.34.4-gke.1130000",
        },
    ],
    node_version="1.34.4-gke.1130000",
    notification_config={
        "pubsub": {
            "enabled": False,
        },
    },
    project=project_id,
    protect_config={
        "workload_config": {
            "audit_mode": "BASIC",
        },
        "workload_vulnerability_mode": "DISABLED",
    },
    min_master_version="1.34.3-gke.1444000",
    release_channel={
        "channel": "UNSPECIFIED",
    },
    secret_manager_config={
        "enabled": False,
    },
    security_posture_config={
        "mode": "BASIC",
        "vulnerability_mode": "VULNERABILITY_DISABLED",
    },
    service_external_ips_config={
        "enabled": False,
    },
    workload_identity_config={
        "workload_pool": f"{project_id}.svc.id.goog",
    },
    network_policy={
        "enabled": True,
        "provider": "CALICO",
    },
    addons_config={
        "network_policy_config": {
            "disabled": False,
        },
    },
    )
