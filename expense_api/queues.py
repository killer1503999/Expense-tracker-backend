from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy
)
import base64
import os


# Retrieve the connection string from an environment
# variable named AZURE_STORAGE_CONNECTION_STRING

def sendMessage(message):

    queueConnect_str = os.getenv("queueConnectionString")
    q_name = os.getenv("storageQueueName")
    stringMessage = str(message)

    queue_client = QueueClient.from_connection_string(queueConnect_str, q_name)
    queue_client.message_encode_policy = BinaryBase64EncodePolicy()
    queue_client.message_decode_policy = BinaryBase64DecodePolicy()

    message_bytes = stringMessage.encode('ascii')

    try:
        queue_client.create_queue()
        queue_client.send_message(
            queue_client.message_encode_policy.encode(content=message_bytes)
        )

    except:
        queue_client.send_message(
            queue_client.message_encode_policy.encode(content=message_bytes)
        )
