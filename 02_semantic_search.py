#!/usr/bin/env python3
"""
Qdrant Semantic Search Tutorial

This script demonstrates how to use Qdrant for semantic search with text embeddings:
1. Generating embeddings from text using sentence-transformers
2. Storing text documents with their embeddings in Qdrant
3. Performing semantic search to find relevant documents
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import time

print("Qdrant Semantic Search Tutorial")
print("===============================\n")

# Step 1: Connect to Qdrant
print("Step 1: Connecting to Qdrant server...")
client = QdrantClient(host="localhost", port=6333)
print("Connected successfully!\n")

# Step 2: Load the embedding model
print("Step 2: Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')  # A small but effective model
vector_size = model.get_sentence_embedding_dimension()
print(f"Loaded model with vector size: {vector_size}\n")

# Step 3: Create a collection for documents
print("Step 3: Creating a collection for documents...")
collection_name = "documents"

# Check if collection exists and recreate it
collections = client.get_collections()
collection_names = [collection.name for collection in collections.collections]

if collection_name in collection_names:
    print(f"Collection '{collection_name}' already exists. Recreating it...")
    client.delete_collection(collection_name=collection_name)

# Create the collection with specified parameters
client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    )
)
print(f"Collection '{collection_name}' created successfully!\n")

# Step 4: Prepare sample documents
print("Step 4: Preparing sample documents...")
documents = [
    {
        "id": 1,
        "title": "What is a Vector Database?",
        "content": "A vector database is a type of database that stores data as high-dimensional vectors and provides efficient similarity search capabilities.",
        "category": "Database Technology",
        "tags": ["vectors", "database", "similarity search"]
    },
    {
        "id": 2,
        "title": "Introduction to Qdrant",
        "content": "Qdrant is a vector similarity search engine and vector database. It provides a production-ready service with a convenient API to store, search, and manage points - vectors with an optional payload.",
        "category": "Database Technology",
        "tags": ["Qdrant", "vector database", "similarity search"]
    },
    {
        "id": 3,
        "title": "Machine Learning Basics",
        "content": "Machine learning is a branch of artificial intelligence that focuses on building systems that learn from data, identify patterns, and make decisions with minimal human intervention.",
        "category": "Artificial Intelligence",
        "tags": ["machine learning", "AI", "data science"]
    },
    {
        "id": 4,
        "title": "Natural Language Processing",
        "content": "Natural Language Processing (NLP) is a field of AI that gives machines the ability to read, understand, and derive meaning from human languages.",
        "category": "Artificial Intelligence",
        "tags": ["NLP", "AI", "language"]
    },
    {
        "id": 5,
        "title": "Vector Embeddings Explained",
        "content": "Vector embeddings are numerical representations of objects like words, sentences, or images. They capture semantic meaning in a way that similar items have similar vector representations.",
        "category": "Machine Learning",
        "tags": ["embeddings", "vectors", "representation learning"]
    },
    {
        "id": 6,
        "title": "Semantic Search Systems",
        "content": "Semantic search systems understand the intent and contextual meaning of search queries rather than just matching keywords, providing more relevant results to users.",
        "category": "Search Technology",
        "tags": ["semantic search", "NLP", "information retrieval"]
    },
    {
        "id": 7,
        "title": "Python Programming Language",
        "content": "Python is a high-level, interpreted programming language known for its readability and versatility. It's widely used in data science, machine learning, web development, and more.",
        "category": "Programming",
        "tags": ["Python", "programming", "coding"]
    },
    {
        "id": 8,
        "title": "Data Structures and Algorithms",
        "content": "Data structures are ways of organizing and storing data, while algorithms are step-by-step procedures for solving problems or performing computations.",
        "category": "Computer Science",
        "tags": ["algorithms", "data structures", "computer science"]
    }
]

print(f"Prepared {len(documents)} sample documents.\n")

# Step 5: Convert documents to vectors and upload to Qdrant
print("Step 5: Converting documents to vectors and uploading to Qdrant...")
points = []

for doc in documents:
    # Generate embedding from document content
    content_text = f"{doc['title']}. {doc['content']}"
    vector = model.encode(content_text)
    
    # Create payload with document metadata
    payload = {
        "title": doc["title"],
        "content": doc["content"],
        "category": doc["category"],
        "tags": doc["tags"]
    }
    
    # Create point
    point = models.PointStruct(
        id=doc["id"],
        vector=vector.tolist(),
        payload=payload
    )
    
    points.append(point)

# Upload all points to Qdrant
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Uploaded {len(points)} document vectors to Qdrant.\n")

# Step 6: Perform semantic search
print("Step 6: Performing semantic search...")

# Define search queries
search_queries = [
    "What is Qdrant?",
    "How do vector databases work?",
    "Tell me about artificial intelligence",
    "Python programming examples"
]

# Perform search for each query
for query in search_queries:
    print(f"\nQuery: '{query}'")
    
    # Convert query to vector
    query_vector = model.encode(query)
    
    # Search in Qdrant
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=3  # Return top 3 matches
    )
    
    # Display results
    print("Results:")
    for i, result in enumerate(search_results, 1):
        print(f"  {i}. {result.payload['title']} (Score: {result.score:.4f})")
        print(f"     Category: {result.payload['category']}")
        print(f"     Tags: {', '.join(result.payload['tags'])}")
        print(f"     Summary: {result.payload['content'][:100]}...")

# Step 7: Search with category filtering
print("\nStep 7: Search with category filtering...")
query = "vector technology"
query_vector = model.encode(query)

# Search only in the "Database Technology" category
filtered_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="Database Technology")
            )
        ]
    ),
    limit=2
)

print(f"\nQuery: '{query}' (filtered to 'Database Technology' category)")
print("Results:")
for i, result in enumerate(filtered_results, 1):
    print(f"  {i}. {result.payload['title']} (Score: {result.score:.4f})")
    print(f"     Category: {result.payload['category']}")
    print(f"     Summary: {result.payload['content'][:100]}...")

# Step 8: Search with tag filtering
print("\nStep 8: Search with tag filtering...")
query = "artificial intelligence"
query_vector = model.encode(query)

# Search for documents with the "NLP" tag
tag_filtered_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="tags",
                match=models.MatchValue(value="NLP")
            )
        ]
    ),
    limit=2
)

print(f"\nQuery: '{query}' (filtered to documents with 'NLP' tag)")
print("Results:")
for i, result in enumerate(tag_filtered_results, 1):
    print(f"  {i}. {result.payload['title']} (Score: {result.score:.4f})")
    print(f"     Tags: {', '.join(result.payload['tags'])}")
    print(f"     Summary: {result.payload['content'][:100]}...")

print("\nSemantic search tutorial completed successfully!")
