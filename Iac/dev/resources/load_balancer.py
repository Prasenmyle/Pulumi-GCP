import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack

def create_global_network_load_balancer():
    env_name = get_stack()
    name = f"airxp-{env_name}".lower().replace("_", "-")

    default = gcp.compute.HealthCheck(
        "default",
        name=f"{name}-gke-ingress",
        http_health_check=gcp.compute.HealthCheckHttpHealthCheckArgs(
            port=30021,
            request_path="/healthz/ready",
        ),
        timeout_sec=2,
        check_interval_sec=10,
    )

    # Create a backend service for https
    airxp_dev_backend_service_https = gcp.compute.BackendService(
        "airxp_dev_backend_service_https",
        name=f"{name}-ingress-https",
        protocol="TCP",
        health_checks=default.id,
        timeout_sec=3600,
        load_balancing_scheme="EXTERNAL_MANAGED",
        ip_address_selection_policy="IPV4_ONLY",
        session_affinity="NONE",
        port_name="https",
        locality_lb_policy="ROUND_ROBIN",
        log_config=gcp.compute.BackendServiceLogConfigArgs(
           enable=False,  # Logging Disabled
           sample_rate=0  # Sample Rate: 0
        ),
    )

    # Create a Target TCP Proxy for https
    airxp_dev_ingress_https_target_proxy = gcp.compute.TargetTCPProxy(
        "airxp_dev_ingress_https_target_proxy",
        name=f"{name}-ingress-https-target-proxy",
        backend_service=airxp_dev_backend_service_https.self_link,
        proxy_header="PROXY_V1",
    )

    # Create a forwarding rule for https
    airxp_dev_forwarding_rule_https = gcp.compute.GlobalForwardingRule(
        "airxp_dev_forwarding_rule_https",
        name=f"{name}-ingress-https",
        network_tier="PREMIUM",
        # ip_address=static_ip.address,
        ip_protocol="TCP",
        port_range="443-443",
        load_balancing_scheme="EXTERNAL_MANAGED",
        target=airxp_dev_ingress_https_target_proxy.self_link,
    )

    # Create a backend service for http
    airxp_dev_backend_service = gcp.compute.BackendService(
        "airxp_dev_backend_service",
        name=f"{name}-ingress",
        protocol="TCP",
        health_checks=default.id,
        timeout_sec=60,
        load_balancing_scheme="EXTERNAL_MANAGED",
        ip_address_selection_policy="IPV4_ONLY",
        port_name="http",
        locality_lb_policy="ROUND_ROBIN",
        session_affinity="NONE",
        log_config=gcp.compute.BackendServiceLogConfigArgs(
           sample_rate=0  # Sample Rate: 0
        ),
    )

    # Create a Target TCP Proxy for http
    default = gcp.compute.TargetTCPProxy(
        "default",
        name=f"{name}-ingress-target-proxy",
        backend_service=airxp_dev_backend_service.self_link,
        proxy_header="PROXY_V1",
    )

    # Create a forwarding rule for http
    airxp_dev_forwarding_rule = gcp.compute.GlobalForwardingRule(
        "airxp_dev_forwarding_rule",
        name=f"{name}-ingress-forwarding-rule",
        # ip_address=static_ip.address,
        ip_protocol="TCP",
        port_range="80-80",
        network_tier="PREMIUM",
        load_balancing_scheme="EXTERNAL_MANAGED",
        target=default.self_link,
    )

    return