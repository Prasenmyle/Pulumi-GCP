import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack


def create_cloud_run_services():
    env_name = get_stack()
    project_id = gcp.config.project
    region = gcp.config.region or "us-west1"

    services = [
        {
            "name": "air-image-resize",
            "image": f"",
            "memory": "512Mi",
            "cpu": "1",
            "port": 50184,
            "max_instances": 10,
            "service_account": f"yourserviceaccountname@{project_id}.iam.gserviceaccount.com",
        }
    ]

    created_services = []

    for svc in services:
        service = gcp.cloudrun.Service(
            f"{svc['name']}-{env_name}",
            name=f"{svc['name']}-{env_name}",
            location=region,
            metadata={
                "annotations": {
                        # internal + load balancer
                    "run.googleapis.com/ingress": "internal-and-cloud-load-balancing"
                    }
                },

            template={
                "spec": {
                    "serviceAccountName": svc["service_account"],
                    "containers": [
                        {
                            "image": svc["image"],
                            "ports": [
                                {
                                    "containerPort": svc["port"]
                                }
                            ],
                            "resources": {
                                "limits": {
                                    "cpu": svc["cpu"],
                                    "memory": svc["memory"],
                                }
                            }
                        }
                    ],
                }
            },
        )

        created_services.append(service)

    pulumi.export(
        "cloud_run_services",
        [svc.name for svc in created_services]
    )

    return created_services
