from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "your connection string"
TOPIC_NAME = "your queue name"
SUBSCRIPTION_NAME = "your subscription name"

servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR,logging_enable=True)

# Receive Messages
with servicebus_client:
    receiver = servicebus_client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5)
    with receiver:
        for msg in receiver:
            print("Received:" + str(msg))
            receiver.complete_message(msg)
	









