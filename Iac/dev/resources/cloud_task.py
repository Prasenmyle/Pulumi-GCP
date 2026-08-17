import pulumi
import pulumi_gcp as gcp

def create_cloud_tasks_queue():
    env_name = pulumi.get_stack()

    # Define the Cloud Tasks queue
    post_creation = gcp.cloudtasks.Queue(
        f"post_creation",
        name=f"post-creation",
        location="us-west1",
        rate_limits={
            "max_concurrent_dispatches": 1000,
            "max_dispatches_per_second": 500,
        },
        retry_config={
            "max_attempts": 1,
            "max_backoff": "2s",
            "max_doublings": 2,
            "min_backoff": "0.100s",
        },
        stackdriver_logging_config={
        "sampling_ratio": 1,
        },
    )

    pulumi.export("queue_name", post_creation.name)
    return post_creation