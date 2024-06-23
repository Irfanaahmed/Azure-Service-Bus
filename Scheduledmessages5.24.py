from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient
import threading
import time

# Azure Service Bus connection string
CONNECTION_STR = "your connection string"

# Topic name
topic_name = "your topic name"
subscription_name = "your subscription name"

# List of messages to send
messages = [
    {"id": 1, "content": "message 1"},
    {"id": 2, "content": "message 2"},
    {"id": 3, "content": "message 3"}
]

def ensure_topic_exists(connection_str, topic_name):
    admin_client = ServiceBusAdministrationClient.from_connection_string(connection_str)
    try:
        admin_client.get_topic(topic_name)
        print(f"Topic '{topic_name}' already exists.")
    except:
        admin_client.create_topic(topic_name)
        print(f"Topic '{topic_name}' created.")

def ensure_subscription_exists(connection_str, topic_name, subscription_name):
    admin_client = ServiceBusAdministrationClient.from_connection_string(connection_str)
    try:
        admin_client.get_subscription(topic_name, subscription_name)
        print(f"Subscription '{subscription_name}' already exists.")
    except:
        admin_client.create_subscription(topic_name, subscription_name)
        print(f"Subscription '{subscription_name}' created.")

def send_messages(messages, topic_name, connection_str):
    with ServiceBusClient.from_connection_string(connection_str) as client:
        sender = client.get_topic_sender(topic_name)
        with sender:
            for message in messages:
                servicebus_message = ServiceBusMessage(message["content"])
                sender.send_messages(servicebus_message)
                print(f"Message {message['id']} sent")

def receive_messages(connection_str, topic_name, subscription_name):
    with ServiceBusClient.from_connection_string(connection_str) as client:
        receiver = client.get_subscription_receiver(topic_name, subscription_name)
        with receiver:
            for message in receiver:
                print("Received:", message)
                message.complete()

def schedule_messages_repeatedly(messages, topic_name, connection_str, interval):
    while True:
        send_messages(messages, topic_name, connection_str)
        time.sleep(interval)

# Ensure the topic exists
ensure_topic_exists(connection_str, topic_name)

# Ensure the subscription exists
ensure_subscription_exists(connection_str, topic_name, subscription_name)

# Start the thread to send messages at regular intervals
interval_minutes = 5
thread_send = threading.Thread(target=schedule_messages_repeatedly, args=(messages, topic_name, connection_str, interval_minutes * 60))
thread_send.daemon = True  # Daemonize the thread so it exits when the main program exits
thread_send.start()

# Start the thread to receive messages
thread_receive = threading.Thread(target=receive_messages, args=(connection_str, topic_name, subscription_name))
thread_receive.daemon = True
thread_receive.start()

# Keep the main thread alive
while True:
    time.sleep(1)
