# Kafka using Topics

Kafka has only one primitive: the **topic**. Queue-like behavior versus topic-like
(publish/subscribe) behavior is decided by the **consumer group id**, not by the broker.

1. kafkaTopicSend.py - Sends out a sequence of numbered messages to the topic.
1. kafkaTopicReceive.py - Receives ALL the topic messages for group `listenSubscription`.
1. kafkaTopicReceive2.py - Same thing under a different group id, so it also receives ALL the messages.

Run both receivers at once: each one sees every message, the same way the Azure Service Bus
topic subscriptions do. Run two copies of the *same* receiver and Kafka splits the messages
between them instead - that is the queue behavior.

## Setup
```
pip install kafka-python
docker compose up -d          # starts a single-node broker on localhost:9092
```

## Run
```
python kafkaTopicReceive.py   # terminal 1
python kafkaTopicReceive2.py  # terminal 2
python kafkaTopicSend.py      # terminal 3
```

The topic `subscribetopic` is created automatically on first send. Shut the broker down with
`docker compose down` when you are finished.
