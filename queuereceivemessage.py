from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "your connection string"
QUEUE_NAME = "your queue name"

# Send Messages
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR)
with servicebus_client:
    sender = servicebus_client.get_queue_sender(queue_name=QUEUE_NAME)
    with sender:
        message = ServiceBusMessage("Message content")
        sender.send_messages(message)

print("Done Sending Messages")
print("----------------------")

# Receive Messages
with servicebus_client:
    receiver = servicebus_client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5)
    with receiver:
        for msg in receiver:
            print("Received:", str(msg))
            receiver.complete_message(msg)
	









