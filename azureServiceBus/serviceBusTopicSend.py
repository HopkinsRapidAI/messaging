import asyncio
import os
from pathlib import Path
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from dotenv import load_dotenv
import time

load_dotenv(Path(__file__).resolve().parent / ".env")
NAMESPACE_CONNECTION_STR = os.environ["SERVICEBUS_CONNECTION_STR"]
TOPIC_NAME = "testtopic"
msgCount = 1

async def send_single_message(sender,msgCount):
    # Create a Service Bus message
    message = ServiceBusMessage(f"Single Message {msgCount}")
    # send the message to the topic
    await sender.send_messages(message)
    print("Sent message " ,msgCount)
    #msgCount = msgCount + 1
    
async def send_a_list_of_messages(sender,msgCount):
        # Create a list of messages
        messages = [ServiceBusMessage(f"Message in list {i+msgCount}")for i in range(5)]
        # send the list of messages to the topic
        await sender.send_messages(messages)
        print("Sent a list of 5 messages")
        msgCount = msgCount + 5
        
async def send_batch_message(sender,msgCount):
        # Create a batch of messages
        async with sender:
            batch_message = await sender.create_message_batch()
            for i in range(10):
                try:
                    # Add a message to the batch
                    batch_message.add_message(ServiceBusMessage(f"Message inside a ServiceBusMessageBatch {i+msgCount}"))
                except ValueError:
                    # ServiceBusMessageBatch object reaches max_size.
                    # New ServiceBusMessageBatch object can be created here to send more data.
                    break
            # Send the batch of messages to the topic
            await sender.send_messages(batch_message)
        print("Sent a batch of 10 messages")
        msgCount = msgCount + 10
    
async def run(msgCount):
        # create a Service Bus client using the connection string
        while(True):
           
            async with ServiceBusClient.from_connection_string(
                conn_str=NAMESPACE_CONNECTION_STR,
                logging_enable=True) as servicebus_client:
                # Get a Topic Sender object to send messages to the topic
                sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
                async with sender:
                    # Send one message
                    await send_single_message(sender,msgCount)
                    print("sent single message")
                    time.sleep(1)
                    # Send a list of messages
                    #await send_a_list_of_messages(sender,msgCount)
                    # Send a batch of messages
                    #await send_batch_message(sender,msgCount)
                    msgCount = msgCount + 1
asyncio.run(run(msgCount))
print("Done sending messages")
print("-----------------------")

