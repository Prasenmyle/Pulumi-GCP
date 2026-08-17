import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack

def create_storage_bucket():
    project_id = gcp.config.project

    user_data = gcp.storage.Bucket("user_data",
        hierarchical_namespace={
            "enabled": False,
        },
        location="US",
        name="user-data",
        project=project_id,
        public_access_prevention="inherited",
        rpo="DEFAULT",
        uniform_bucket_level_access=True,
    )

    return user_data

