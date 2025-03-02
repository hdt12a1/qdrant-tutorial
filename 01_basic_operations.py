#!/usr/bin/env python3
"""
Qdrant Basic Operations Tutorial

This script demonstrates the fundamental operations with Qdrant:
1. Connecting to Qdrant
2. Creating a collection
3. Adding vectors
4. Basic search
5. Retrieving points
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
import numpy as np

print("Qdrant Basic Operations Tutorial")
print("================================\n")

# Step 1: Connect to Qdrant
print("Step 1: Connecting to Qdrant server...")

# Connect with API key authentication
# Use the admin key for full access
api_key = "my-secure-admin-key-123"  # Admin key with full access
client = QdrantClient(
    host="localhost", 
    port=6333, 
    api_key=api_key,
    https=False  # Explicitly use HTTP instead of HTTPS
)
print("Connected successfully with admin API key authentication!\n")

# Step 2: Create a collection
print("Step 2: Creating a collection...")
collection_name = "tutorial_collection"

# Define vector size
vector_size = 4  # Using a small size for demonstration

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
        distance=models.Distance.COSINE  # Using cosine similarity
    )
)
print(f"Collection '{collection_name}' created successfully!\n")

# Step 3: Add vectors to the collection
print("Step 3: Adding vectors to the collection...")

# Create some simple vectors for demonstration
vectors = [
    # Point 1: A vector representing "red apple"
    {
        "id": 1,
        "vector": [0.9, 0.1, 0.1, 0.2],
        "payload": {"name": "red apple", "category": "fruit", "color": "red"}
    },
    # Point 2: A vector representing "green apple"
    {
        "id": 2,
        "vector": [0.8, 0.1, 0.7, 0.2],
        "payload": {"name": "green apple", "category": "fruit", "color": "green"}
    },
    # Point 3: A vector representing "red car"
    {
        "id": 3,
        "vector": [0.1, 0.9, 0.1, 0.2],
        "payload": {"name": "red car", "category": "vehicle", "color": "red"}
    },
    # Point 4: A vector representing "blue car"
    {
        "id": 4,
        "vector": [0.1, 0.8, 0.1, 0.7],
        "payload": {"name": "blue car", "category": "vehicle", "color": "blue"}
    }
]

# Prepare points for insertion
points = [
    models.PointStruct(
        id=item["id"],
        vector=item["vector"],
        payload=item["payload"]
    )
    for item in vectors
]

# Insert points into the collection
client.upsert(
    collection_name=collection_name,
    points=points
)

print(f"Added {len(vectors)} vectors to the collection.\n")

# Step 4: Basic vector search
print("Step 4: Performing basic vector search...")

# Create a query vector (similar to "red apple")
query_vector = [0.9, 0.2, 0.1, 0.3]

# Search for similar vectors
search_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=2  # Return top 2 matches
)

print("Query: Vector similar to 'red apple'")
print("Results:")
for result in search_results:
    print(f"  - {result.payload['name']} (Score: {result.score:.4f})")
print()

# Step 5: Search with filtering
print("Step 5: Search with filtering...")

# Search for vectors in the "vehicle" category
filtered_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="category",
                match=models.MatchValue(value="vehicle")
            )
        ]
    ),
    limit=2
)

print("Query: Vector similar to 'red apple' but filtered to 'vehicle' category")
print("Results:")
for result in filtered_results:
    print(f"  - {result.payload['name']} (Score: {result.score:.4f})")
print()

# Step 6: Retrieve points by ID
print("Step 6: Retrieving points by ID...")

# Retrieve specific points by their IDs
retrieved_points = client.retrieve(
    collection_name=collection_name,
    ids=[1, 3]
)

print("Retrieved points with IDs 1 and 3:")
for point in retrieved_points:
    print(f"  - ID: {point.id}, Name: {point.payload['name']}")
print()

# Step 7: Get collection info
print("Step 7: Getting collection information...")

# Get information about the collection
collection_info = client.get_collection(collection_name=collection_name)

print(f"Collection: {collection_name}")  # Use the collection_name variable instead
print(f"Vector size: {collection_info.config.params.vectors.size}")
print(f"Distance function: {collection_info.config.params.vectors.distance}")
print(f"Number of vectors: {collection_info.vectors_count}")

print("\nBasic operations tutorial completed successfully!")
