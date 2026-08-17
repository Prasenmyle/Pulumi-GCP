import pulumi
from pulumi_gcp import compute

def create_cloud_nat():
    env_name = pulumi.get_stack()
    # Define the Cloud Router
    test = compute.Router(
        f"test-{env_name}",
        name=f"test-{env_name}",
        network="default",
        region="us-west1",
    )

    # Define the Cloud NAT Gateway
    cloud_nat = compute.RouterNat(
        f"test-{env_name}",
        name=f"test-{env_name}",
        router=test.name,
        endpoint_types=["ENDPOINT_TYPE_VM"],
        log_config={
            "enable": False,
            "filter": "ALL",
        },
        min_ports_per_vm=64,
        nat_ip_allocate_option="AUTO_ONLY",
        region="us-west1",
        source_subnetwork_ip_ranges_to_nat="ALL_SUBNETWORKS_ALL_IP_RANGES",
    )

    # Export output values
    pulumi.export("cloud_router_name", test.name)
    # pulumi.export("cloud_nat_name", cloud_nat.name)

