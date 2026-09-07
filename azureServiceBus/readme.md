# Azure Service Bus using Queues
## Queue
1. serviceBusQueueReceive.py - Waits to receive a message off the queue.  Run multiple copies of this to see that each receiver gets different messages.
1. serviceBusQueueSend.py - Sends out a sequence of numbered messages.
## Topic
1. serviceBusTopicReceive.py - Receives ALL the topic messages even if multiple versions are run.  Each on will receive all the mssages for that topic from this subscription.
1. serviceBusTopicReceive2.py - Receives ALL the topic messages even if multiple versions are run.  Each on will receive all the mssages for that topic from this subscription.
1. serviceBusTopicSend.py - Sends out sequence of messages to the given topic.
