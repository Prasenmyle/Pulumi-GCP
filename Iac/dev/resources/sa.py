import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack
from typing import Dict, List

# Configuration
config = pulumi.Config()
project_id = gcp.config.project
env_name = get_stack()

# Define service accounts with their roles
def create_service_account_with_bindings():

    service_accounts = [
    {
        "sa_name": "admin-role",
        "roles": [
            "roles/firebase.developAdmin",
            "roles/pubsub.editor",
            "roles/iam.serviceAccountTokenCreator",
        ],
    },
        {
        "sa_name": "poweruser-role",
        "roles": [
            "roles/firebase.developAdmin",
        ],
    },

        {
        "sa_name": "cicd-role",
        "roles": [
            # Compute & GKE
            "roles/container.admin",
            "roles/compute.admin",
            # IAM
            "roles/iam.serviceAccountAdmin",
            "roles/iam.serviceAccountUser",
            "roles/iam.securityAdmin",
            "roles/iam.workloadIdentityPoolAdmin",
            # Storage & Artifact Registry
            "roles/storage.admin",
            "roles/artifactregistry.admin",
            # Databases
            "roles/datastore.owner",
            "roles/firebase.admin",
            # Networking
            "roles/compute.networkAdmin",
            "roles/dns.admin",
            # Serverless & Scheduling
            "roles/cloudfunctions.developer",
            "roles/run.admin",
            "roles/cloudscheduler.admin",
            "roles/cloudtasks.admin",
            # Messaging
            "roles/pubsub.admin",
            # Monitoring & Logging
            "roles/monitoring.admin",
            "roles/logging.admin",
            # Secrets
            "roles/secretmanager.secretAccessor",
            ],
    },

   ]

    created_service_accounts = []

    for sa in service_accounts:
        # Validate required fields
        required_keys = {"sa_name", "roles"}
        missing_keys = required_keys - sa.keys()
        if missing_keys:
            raise ValueError(f"Missing required keys in service account config: {missing_keys}")

        sa_name = sa["sa_name"]
        roles = sa["roles"]

    # Create GCP Service Account
        sa_resource = gcp.serviceaccount.Account(
            f"{sa_name}",
            account_id=sa_name,
            display_name=f"{sa_name}-{env_name}",
            project=project_id
        )

    # Add IAM role bindings to project
        for role in roles:
            gcp.projects.IAMMember(
                f"{sa_name}-{role.replace('.', '-').replace('/', '-')}",
                project=project_id,
                role=role,
                member=pulumi.Output.concat("serviceAccount:", sa_resource.email),
            )

        # Create Workload Identity Binding
        gcp.serviceaccount.IAMBinding(
            f"{sa_name}-wi-binding",
            service_account_id=sa_resource.name,
            role="roles/iam.workloadIdentityUser",
            members=f"serviceAccount:{project_id}.svc.id.goog[{env_name}/{sa_name}]"
        )

        created_service_accounts.append(sa_resource)
