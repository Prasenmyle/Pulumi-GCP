import pulumi
from pulumi_gcp import firestore
from pulumi import get_stack

def create_firestore_databases():

    admin = firestore.Database(
        f"admin",
        name="air-admin-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    agent = firestore.Database(
        f"agent",
        name="air-agent-service-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    # asset_processing = firestore.Database(
    #     f"asset-processing",
    #     name="air-asset-processing-db",
    #     location_id="nam5",
    #     type="FIRESTORE_NATIVE",
    # ),

    chat = firestore.Database(
        f"chat",
        name="air-chat-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    entity_graph = firestore.Database(
        f"entity-graph",
        name="air-entity-graph-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    feed = firestore.Database(
        f"feed",
        name="air-feed-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    itinerary = firestore.Database(
        f"itinerary",
        name="air-itinerary-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    moderation = firestore.Database(
        f"moderation",
        name="air-moderation-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    notification = firestore.Database(
        f"notification",
        name="air-notification-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    ugc = firestore.Database(
        f"ugc",
        name="air-ugc-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    user = firestore.Database(
        f"user",
        name="air-user-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    return [admin, agent, chat, entity_graph, feed, itinerary, moderation, notification, ugc, user]
