from azure.servicebus import ServiceBusClient, ServiceBusMessage

CONNECTION_STR = "your connection string"
TOPIC_NAME = "your queue name"
SUBSCRIPTION_NAME = "your subscription name"


def send_single_message(sender):
    message = ServiceBusMessage("welcome")
    sender.send_messages(message)
    print("Sent welcome note")

def send_a_list_of_messages(sender):
    messages = [ServiceBusMessage("Here is the list") for _ in range(4)]
    sender.send_messages(messages)
    print("Sent a list of 4 messages")

def send_batch_of_messages(sender):
    batch_message = sender.create_message_batch()
    for _ in range(6):
        try:
            batch_message.add_message(ServiceBusMessage("Here is a batch of message"))
        except ValueError:
            break

    sender.send_messages(batch_message)
    print("Sent a batch of 6 messages")
print("starting here")
servicebus_client = ServiceBusClient.from_connection_string(conn_str=CONNECTION_STR, logging_enable=True)
with servicebus_client:
    sender = servicebus_client.get_topic_sender(topic_name=TOPIC_NAME)
    with sender:
        send_single_message(sender)
        send_a_list_of_messages(sender)
        send_batch_of_messages(sender)

print("Done Sending Messages")
print("----------------------")
	









