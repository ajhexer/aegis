# Aegis

![rag](https://github.com/user-attachments/assets/b29d3a5a-87cb-42fa-8296-a547343a4958)

A simple Retrieval-Augmented Generation (RAG) system built with Django, Celery, and PostgreSQL as a vector database. This system allows you to upload documents which are indexed using Celery workers. You can then interact with your documents via a chat interface using the OpenAI API.

## Features

- **Document Upload:** Easily upload new documents to be indexed.
- **Celery Workers:** Background processing for indexing documents.
- **Chat Interface:** Interact with your documents using a chat interface powered by the OpenAI API.
- **Docker Compose:** Simplified deployment and running with Docker Compose.

## Requirements

- Docker
- Docker Compose
- OpenAI API key

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/username/interview-chatbot.git
    cd interview-chatbot
    ```

2. **Set up environment variables:**

    Create a `.env` file in the root directory and add your OpenAI API key and base URL:

    ```env
    OPENAI_API_KEY=your-openai-api-key
    OPENAI_API_BASE_URL=your-openai-api-base-url
    ```

3. **Build and run the Docker containers:**

    ```bash
    docker-compose up --build
    ```

## Configuration

- The OpenAI API key and base URL should be set in the `config/settings.py` file or via environment variables as shown above.

## Usage

1. **Access the application:**

    Open your browser and go to `http://localhost:8000`.

2. **Upload documents:**

    Navigate to the document upload section to add new documents. The documents will be indexed by Celery workers.

3. **Chat with your documents:**

    Use the chat interface to interact with the indexed documents using the OpenAI API.

## Project Structure

```
interview-chatbot/
│
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
│
├── chat/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── template/
│   ├── chatbot-detail.html
│   ├── chatbot-list.html
│   ├── chat-details.html
│   ├── chat-list.html
│   ├── create-chat.html
│   ├── create-chatbot.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── search_results.html
│
├── deployments/
│   └── docker-compose.yaml
│
├── manage.py
├── main.py
├── requirements.txt
```
