import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack

def create_storage_bucket():
    project_id = gcp.config.project

    basic = gcp.storage.Bucket("basic",
        hierarchical_namespace={
            "enabled": False,
        },
        location="US",
        name="basic",
        project=project_id,
        public_access_prevention="inherited",
        rpo="DEFAULT",
        uniform_bucket_level_access=True,
    )

    return basic

