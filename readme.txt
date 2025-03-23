This is a recommendation microservice for a social media platform. We have 2 main functions: 
1. Generate tags for a post
2. Generate recommendations of related posts based on a given set of tags

In this first iteration, we start with Content-Based Filtering.

A. For the first function, we will use a pre-trained BERTopic model to generate tags for a given post.
https://huggingface.co/docs/hub/en/bertopic
    A.1. Subscribe to the Google Pub/Sub message queue
    A.2. Receive a post from the message queue
    A.3. Generate tags for the post using BERTopic
    A.4. Update the post with the tags in MongoDB

B. For the second function, we will use the tags to find related posts. We leave this for the next iteration.


Subscribe to the Google Pub/Sub message queue example:
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

# TODO(developer)
# project_id = "your-project-id"
# subscription_id = "your-subscription-id"
# Number of seconds the subscriber should listen for messages
# timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_id}`
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    print(f"Received {message}.")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"Listening for messages on {subscription_path}..\n")

# Wrap subscriber in a 'with' block to automatically call close() when done.
with subscriber:
    try:
        # When `timeout` is not set, result() will block indefinitely,
        # unless an exception is encountered first.
        streaming_pull_future.result(timeout=timeout)
    except TimeoutError:
        streaming_pull_future.cancel()  # Trigger the shutdown.
        streaming_pull_future.result()  # Block until the shutdown is complete.


python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn

uvicorn main:app --reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
python main.py

RUN THE TAG SERVICE:
python service_runner.py
