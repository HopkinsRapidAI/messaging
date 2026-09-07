#!/usr/bin/env python
# Kafka consumer - subscribes to a topic and prints every message it receives.
#
# GROUP_ID controls the fan-out:
#   Same group id in two copies  -> the messages are SPLIT between them (queue behavior).
#   Different group ids          -> each copy receives ALL the messages (topic behavior).
# Run kafkaTopicReceive2.py alongside this one to see the topic behavior.

from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "subscribetopic"
GROUP_ID = "listenSubscription"

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    group_id=GROUP_ID,
    auto_offset_reset="earliest",   # start at the beginning the first time this group runs
    value_deserializer=lambda v: v.decode("utf-8"),
)

print(f" [*] Waiting for messages on '{TOPIC_NAME}' as group '{GROUP_ID}'. To exit press CTRL+C")
try:
    for msg in consumer:
        print(f" [x] Received: {msg.value}  (partition {msg.partition}, offset {msg.offset})")
except KeyboardInterrupt:
    print("Interrupted")
finally:
    consumer.close()
