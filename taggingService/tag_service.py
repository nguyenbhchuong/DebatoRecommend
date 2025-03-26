from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from bertopic import BERTopic
from pymongo import MongoClient
import json
import config
from bson import ObjectId
from app.schemas.topic import TopicModel  # Import the new Pydantic model

class TaggingService:
    def __init__(self):
        # Initialize Pub/Sub subscriber
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(
            config.PROJECT_ID, 
            config.SUBSCRIPTION_ID
        )
        print("Done initializing Pub/Sub subscriber")
        # Initialize MongoDB client
        self.mongo_client = MongoClient(config.MONGODB_URI)
        self.db = self.mongo_client[config.MONGODB_DB]
        self.posts_collection = self.db['topics']
        
        print("Done initializing MongoDB client")
        # Load BERTopic model
        self.model = BERTopic.load(config.BERTOPIC_MODEL_PATH)
        self.model.get_topic_info()
        print("Done initializing BERTopic model")

    def _split_long_paragraphs(self, paragraphs, max_words=250):
        """Split paragraphs that exceed max_words into smaller chunks"""
        result = []
        for paragraph in paragraphs:
            words = paragraph.split()
            if len(words) > max_words:
                # Split into chunks of approximately max_words
                chunks = []
                current_chunk = []
                word_count = 0
                
                for word in words:
                    current_chunk.append(word)
                    word_count += 1
                    
                    if word_count >= max_words:
                        chunks.append(' '.join(current_chunk))
                        current_chunk = []
                        word_count = 0
                
                # Add any remaining words as the last chunk
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                
                result.extend(chunks)
            else:
                result.append(paragraph)
        return result

    def _combine_weighted_topics(self, paragraph_topics, max_tags=10):
        """
        Combine weighted topics from multiple paragraphs into a single dictionary of tags with weights.
        Each topic in paragraph_topics is a tuple of (topic_name, weight).
        """
        # Create a dictionary to store combined weights
        topic_weights = {}
        
        # For each paragraph's topics
        for topics in paragraph_topics:
            # Add weights, giving slightly more importance to topics that appear multiple times
            for topic, weight in topics:
                if topic in topic_weights:
                    # Take the maximum weight if topic appears again
                    topic_weights[topic] = max(topic_weights[topic], weight)
                else:
                    topic_weights[topic] = weight

        # Sort topics by their combined weights and take top N
        sorted_topics = sorted(
            topic_weights.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:max_tags]

        # Convert to dictionary format
        return dict(sorted_topics)

    def generate_tags(self, text):
        """Generate tags with weights for the given text using BERTopic"""
        # print("text", text)
        initial_paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # Break long paragraphs into smaller chunks
        paragraphs = self._split_long_paragraphs(initial_paragraphs)
        
        # print("Paragraphs:", paragraphs)
        topics, probs = self.model.transform(paragraphs)
        
        # Get top 10 topics for each paragraph
        paragraph_topics = []
        for i, topic_ids in enumerate(topics):
            if topic_ids == -1:  # Skip outlier topics
                continue
    
            topic_info = self.model.get_topic(topic_ids)
            paragraph_topics.append(topic_info[:10])
            
        # Combine topics from all paragraphs into a dictionary
        final_topics = self._combine_weighted_topics(paragraph_topics)
        
        print("Final topics with weights:", final_topics)
        return final_topics

    def process_message(self, message):
        """Process a single message from Pub/Sub"""
        try:
            print(f"Received message: {message}")
            topic_id = message.attributes.get('post_id')
            
            if not topic_id:
                print("No post_id in message attributes")
                message.ack()
                return

            topic_id = ObjectId(topic_id)

            # Fetch the topic from MongoDB
            topic_dict = self.posts_collection.find_one({'_id': topic_id})
            
            if not topic_dict:
                print(f"Topic not found: {topic_id}")
                message.ack()
                return

            # Convert to Pydantic model
            topic = TopicModel.from_dict(topic_dict)

            content = f"{topic.title} {topic.description or ''}"
            
            if not content.strip():
                print(f"No content to generate tags for topic: {topic_id}")
                message.ack()
                return

            # Generate tags with weights
            tags_with_weights = self.generate_tags(content)

            # Update MongoDB
            self.posts_collection.update_one(
                {'_id': topic_id},
                {'$set': {'tags': tags_with_weights}},
                upsert=False
            )

            print(f"Successfully processed topic {topic_id} with weighted tags: {tags_with_weights}")
            message.ack()

        except Exception as e:
            print(f"Error processing message: {e}")
            message.ack()  # Acknowledge to prevent redelivery

    def start(self, timeout=None):
        """Start listening for messages"""
        print("Starting Tagging Service")
        streaming_pull_future = self.subscriber.subscribe(
            self.subscription_path, 
            callback=self.process_message
        )
        print(f"Listening for messages on {self.subscription_path}")

        try:
            streaming_pull_future.result(timeout=timeout)
        except TimeoutError:
            streaming_pull_future.cancel()
            streaming_pull_future.result()
        finally:
            self.subscriber.close() 