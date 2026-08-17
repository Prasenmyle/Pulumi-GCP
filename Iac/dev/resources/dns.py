import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack

def create_dns_resources():
    env_name = get_stack()

    # Fetch the existing static IP directly from GCP
    static_ip = gcp.compute.GlobalAddress.get("static-ip", f"airxp-{env_name}-ingress").address

    # Define a managed DNS zone
    default = gcp.dns.ManagedZone(
        "default",
        name=f"airxp-app-{env_name}",
        dns_name=f"{env_name}.airxp.app.",
        description=f"Managed DNS zone for {env_name}",
        # description="Development Environment",
        cloud_logging_config={
        "enable_logging": False,
        },
    )

    # List of DNS records to create
    dns_records = [
        {
            "dns_name": f"admin-grpc.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"admin.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"api.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"agent.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"analytics.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
         {
            "dns_name": f"argocd.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"chat.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"connection.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],
        },
        {
            "dns_name": f"content-agent.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"entity-graph.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"feed.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"flux.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"litmus.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"itinerary.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"mcp-gateway.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"media-upload.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"moderation.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"notification.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"open-graph.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"search.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"parasoul.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"transcode.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"ugc.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
        {
            "dns_name": f"user.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
         {
            "dns_name": f"lora-builder.{env_name}.airxp.app.",
            "record_type": "A",
            "ttl": 300,
            "rrdatas": [static_ip],

        },
    ]

    # Create DNS records dynamically
    created_records = []
    for record in dns_records:
        # Validate required fields
        required_keys = {"dns_name", "record_type", "ttl", "rrdatas"}
        missing_keys = required_keys - record.keys()
        if missing_keys:
            raise ValueError(f"Missing required keys in DNS record: {missing_keys}")

        # Generate a unique resource name
        resource_name = f"{record['dns_name'].strip('.').replace('.', '-')}"

        # Create the DNS record
        dns_record = gcp.dns.RecordSet(
            resource_name,
            managed_zone=default.name,
            name=record["dns_name"],
            type=record["record_type"],
            ttl=record["ttl"],
            rrdatas=record["rrdatas"],
        )
        created_records.append(dns_record)

    # Export the DNS records and zone details
    pulumi.export("dns_zone_name", default.name)


    return {
        "dns_zone": default,
    }