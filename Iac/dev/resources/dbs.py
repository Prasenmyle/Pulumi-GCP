import pulumi
from pulumi_gcp import firestore
from pulumi import get_stack

def create_firestore_databases():

    admin = firestore.Database(
        f"admin",
        name="admin-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    agent = firestore.Database(
        f"agent",
        name="agent-service-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    chat = firestore.Database(
        f"chat",
        name="air-chat-db",
        location_id="nam5",
        type="FIRESTORE_NATIVE",
    ),

    return [admin, agent, chat,]
