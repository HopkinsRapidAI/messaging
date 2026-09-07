#!/usr/bin/env python
# Kafka producer - sends a sequence of numbered messages to a topic.
# Every consumer group subscribed to this topic gets its own copy of every message.

import time
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "subscribetopic"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: v.encode("utf-8"),
)

msgCount = 1
try:
    while True:
        message = f"Single Message {msgCount}"
        # send() is asynchronous; flush() waits until the broker has it
        producer.send(TOPIC_NAME, message)
        producer.flush()
        print(" [x] Sent", message)
        msgCount = msgCount + 1
        time.sleep(1)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    producer.close()
