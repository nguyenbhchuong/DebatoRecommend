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
    B.1. Create a API endpoint to get the related posts. INPUT: tags, OUTPUT: list of post ids
        - Return maximum top 10 posts.
    B.2. Write a service using cosine similarity to find the most similar posts. This service will be used by the API in B.1.
        - Access to the vectorized data in MongoDB
        - Use the vectorized data to find the most similar posts using cosine similarity
        - Return the list of post ids



python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn main:app --reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
python main.py

RUN THE TAG SERVICE:
python service_runner.py






