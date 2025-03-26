# AI-Powered Content Recommendation System

A microservice-based recommendation system that automatically generates content tags and provides related content suggestions using BERTopic and cosine similarity.

## 🚀 Key Features

- **Automated Content Tagging**: Leverages BERTopic model for intelligent tag generation
- **Content-Based Recommendation Engine**: Provides related content suggestions using cosine similarity
- **Scalable Architecture**: Built with microservices architecture using FastAPI and Pub/Sub
- **Real-time Processing**: Asynchronous processing of content using message queues

## 🛠️ Technology Stack

- **Backend**: Python, FastAPI
- **Machine Learning**: BERTopic, BERT
- **Database**: MongoDB
- **Caching**: Redis
- **API Testing**: Locust
- **Message Queue**: Google Pub/Sub
- **Architecture**: Microservices

## 📋 System Components

1. **Tag Generation Service**

   - Subscribes to Pub/Sub message queue
   - Processes incoming content using BERTopic
   - Automatically generates relevant tags
   - Updates content metadata in MongoDB

2. **Recommendation Service**
   - RESTful API endpoint for content recommendations
   - Content-based filtering using cosine similarity
   - Returns upto 10 most relevant content pieces

## Performance & Optimization Reports:

    - optimization.txt with the results of Locust Tests and Optimization Ideas

## 🔧 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-powered-recommendation-system.git
cd ai-powered-recommendation-system
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the application

```bash
uvicorn app.main:app --reload
```

Start the tagging service

```bash
python service_runner.py
```

## 🌟 Future Enhancements

- Integration of collaborative filtering
- Enhanced recommendation algorithms
- User preference learning
- Performance optimization for large-scale deployment
- Horizontal scaling of the recommendation service

## 📝 License

This project is licensed under a Custom Non-Commercial License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to use, copy, modify, and/or merge copies of the Software, subject to the following conditions:

1. The Software shall not be used for any commercial purposes, including but not limited to:

   - Selling the Software or derivatives of it
   - Using the Software as part of a commercial product or service
   - Monetizing the Software in any way

2. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

3. Any modifications or derivative works must also be released under these same license terms.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
