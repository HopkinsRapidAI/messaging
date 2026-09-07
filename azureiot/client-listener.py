# Install: pip install azure-eventhub python-dotenv

import os
from pathlib import Path
from azure.eventhub import EventHubConsumerClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")
connection_str = os.environ["EVENTHUB_CONNECTION_STR"]
eventhub_name = os.environ["EVENTHUB_NAME"]

def on_event(partition_context, event):
    print("Received event: ", event.body_as_str())
    
    partition_context.update_checkpoint(event)

client = EventHubConsumerClient.from_connection_string(
    conn_str=connection_str,
    consumer_group="$Default",
    eventhub_name=eventhub_name
)

print("Listening for events...")
with client:
		client.receive(on_event=on_event, starting_position="-1")
