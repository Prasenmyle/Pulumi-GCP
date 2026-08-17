import pulumi
import pulumi_gcp as gcp
from pulumi import get_stack

def create_global_alb():
    env_name = get_stack()
    name = f"test-{env_name}".lower().replace("_", "-")

#alb backend buckets
    test_experience_backend = gcp.compute.BackendBucket("test_experience_backend",
    bucket_name="test-cdn-redefined",
    cdn_policy={
        "cache_mode": "CACHE_ALL_STATIC",
        "client_ttl": 3600,
        "default_ttl": 3600,
        "max_ttl": 86400,
        "request_coalescing": True,
    },
    compression_mode="DISABLED",
    enable_cdn=True,
    name=f"{name}-experience-resources",
    )

    #URLMap
    experience__url_map = gcp.compute.URLMap("experience_url_map",
        default_service=test_experience_backend.name,
        host_rules=[
            {
                "hosts": ["cdn.test.app"],
                "path_matcher": "path-matcher-1",
            },
        ],
        name="experience-",
        path_matchers=[
            {
                "default_service": "test_experience_backend.name",
                "name": "path-matcher-1",
            },
        ],
    )

    http_redirect_url_map = gcp.compute.URLMap("http_redirect_url_map",
        default_url_redirect={
            "https_redirect": True,
            "redirect_response_code": "MOVED_PERMANENTLY_DEFAULT",
            "strip_query": False,
        },
        name="http-redirect",
    )

    # HTTPS target proxies for experience-
    experience_target_proxy_2 = gcp.compute.TargetHttpsProxy("experience_target_proxy_2",
        name="experience-target-proxy-2",
        tls_early_data="DISABLED",
        url_map=experience__url_map.name,
    )

    experience_target_proxy_4 = gcp.compute.TargetHttpsProxy("experience_target_proxy_4",
        name="experience-target-proxy-4",
        tls_early_data="DISABLED",
        url_map=experience__url_map.name,
    )

    # HTTP target proxy for http-redirect
    http_redirect_proxy = gcp.compute.TargetHttpProxy("http_redirect_proxy",
        name="http-redirect-proxy",
        url_map=http_redirect_url_map.name,
    )

    #forwardingrule for experience- ALB
    experience_forwarding_rule = gcp.compute.GlobalForwardingRule("experience_forwarding_rule",
        ip_address="0.0.0.0", #update the ip address
        ip_protocol="TCP",
        load_balancing_scheme="EXTERNAL_MANAGED",
        name="experience-forwarding-rule",
        network_tier="PREMIUM",
        port_range="443-443",
        target=experience_target_proxy_2.name,
    )

    experience_forwarding_rule_4 = gcp.compute.GlobalForwardingRule("experience_forwarding_rule_4",
        ip_address="0:0:0:0::", #update the ip address
        ip_protocol="TCP",
        load_balancing_scheme="EXTERNAL_MANAGED",
        name="experience-forwarding-rule-4",
        network_tier="PREMIUM",
        port_range="443-443",
        target=experience_target_proxy_4.name,
    )

    #forwardingrule for http-redirect ALB
    http_redirect_rule = gcp.compute.GlobalForwardingRule("http_redirect_rule",
        ip_address="0.0.0.0", #update the ip address
        ip_protocol="TCP",
        load_balancing_scheme="EXTERNAL_MANAGED",
        name="http-redirect-rule",
        network_tier="PREMIUM",
        port_range="80-80",
        target=http_redirect_proxy.name,
    )

    http_redirect_rule_ipv6 = gcp.compute.GlobalForwardingRule("http_redirect_rule_ipv6",
        ip_address="0:0:0:0::", #update the ip address
        ip_protocol="TCP",
        load_balancing_scheme="EXTERNAL_MANAGED",
        name="http-redirect-rule-ipv6",
        network_tier="PREMIUM",
        port_range="80-80",
        target=http_redirect_proxy.name,
    )

    return
