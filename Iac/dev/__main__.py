from pulumi import get_stack, export
from resources.cluster import create_gke_cluster_and_node_pool
from resources.dbs import create_firestore_databases
from resources.load_balancer import create_global_network_load_balancer
from resources.dns import create_dns_resources
from resources.cloud_scheduler import create_cloud_scheduler_job
from resources.cloud_nat import create_cloud_nat
from resources.cloud_task import create_cloud_tasks_queue
from resources.alb import create_global_alb
from resources.sa import create_service_account_with_bindings
from resources.storage_bucket import create_storage_bucket

env_name = get_stack()
export("env_name", env_name)


# Create resources
gke_cluster = create_gke_cluster_and_node_pool()

firestore_dbs = create_firestore_databases()

load_balancer = create_global_network_load_balancer()

dns_resources = create_dns_resources()

cloud_nat = create_cloud_nat()

queue = create_cloud_tasks_queue()

scheduler_job = create_cloud_scheduler_job()

alb = create_global_alb()

sa = create_service_account_with_bindings()

storage_bucket = create_storage_bucket()
