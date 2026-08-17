import pulumi
import pulumi_gcp as gcp


def create_cloud_scheduler_job():
    env_name = pulumi.get_stack()
    project_id = gcp.config.project


    # Define the Cloud Scheduler job
    default = gcp.cloudscheduler.Job(
        f"default",
        name="stories-schedule",
        description= "scheduled task to push message to post-trigger pub/sub queue",
        region="us-west1",
        schedule="0 0 * * *",
        time_zone="America/Hermosillo",
        retry_config=gcp.cloudscheduler.JobRetryConfigArgs(
            max_retry_duration="300s",
            min_backoff_duration="5s",
            max_backoff_duration="60s",
            max_doublings=2
        ),
        pubsub_target=gcp.cloudscheduler.JobPubsubTargetArgs(
            topic_name=f"projects/{project_id}/topics/post-trigger-{env_name}",
            data="eyJhZ2VudElkcyI6W119",
        )
    )

    pulumi.export("cloud_scheduler_job", default.name)
