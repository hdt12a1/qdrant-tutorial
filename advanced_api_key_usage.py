#!/usr/bin/env python3
"""
Qdrant Advanced API Key Usage Example

This script demonstrates how to use Qdrant with different API keys
for different permission levels and collections.

Note: This is a demonstration script. In a real application, you would
typically use only one API key per client instance, based on the
specific needs of that client.
"""

import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
import json
from dotenv import load_dotenv

# Load environment variables from .env file (if available)
load_dotenv()

# Function to create a client with a specific API key
def create_client(api_key, name="Unnamed"):
    client = QdrantClient(
        host="localhost",
        port=6333,
        api_key=api_key
    )
    return client, name

# Example API keys with different permission levels
# In a real application, these would be stored securely
# and not hardcoded in the script
API_KEYS = {
    "admin": os.environ.get("QDRANT_ADMIN_KEY", "admin-key"),
    "read_only": os.environ.get("QDRANT_READ_KEY", "read-only-key"),
    "products_only": os.environ.get("QDRANT_PRODUCTS_KEY", "products-key"),
}

# Create clients with different API keys
clients = [
    create_client(API_KEYS["admin"], "Admin"),
    create_client(API_KEYS["read_only"], "Read-Only"),
    create_client(API_KEYS["products_only"], "Products-Only"),
]

# Function to test operations with different clients
def test_operation(operation_name, operation_func):
    print(f"\n--- Testing: {operation_name} ---")
    
    for client, name in clients:
        print(f"\nTrying with {name} client:")
        try:
            result = operation_func(client)
            print(f"✅ Success! {result if result else ''}")
        except Exception as e:
            print(f"❌ Failed: {e}")

# Define test operations

def list_collections(client):
    collections = client.get_collections()
    return f"Found {len(collections.collections)} collections"

def create_test_collection(client):
    collection_name = "test_collection"
    try:
        client.delete_collection(collection_name=collection_name)
    except:
        pass
    
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=4,
            distance=models.Distance.COSINE
        )
    )
    return f"Created collection '{collection_name}'"

def add_point_to_collection(client):
    collection_name = "test_collection"
    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=1,
                vector=[0.1, 0.2, 0.3, 0.4],
                payload={"name": "test point"}
            )
        ]
    )
    return "Added point to collection"

def search_in_collection(client):
    collection_name = "test_collection"
    results = client.search(
        collection_name=collection_name,
        query_vector=[0.1, 0.2, 0.3, 0.4],
        limit=1
    )
    return f"Found {len(results)} results"

def delete_point(client):
    collection_name = "test_collection"
    client.delete(
        collection_name=collection_name,
        points_selector=models.PointIdsList(
            points=[1]
        )
    )
    return "Deleted point"

# Main demonstration
if __name__ == "__main__":
    print("Qdrant Advanced API Key Usage Example")
    print("=====================================")
    
    print("\nThis script demonstrates how different API keys with different")
    print("permission levels affect what operations can be performed.")
    print("\nNote: For this script to work correctly, you need to have Qdrant")
    print("configured with multiple API keys with different permissions.")
    
    # Run tests
    test_operation("List Collections", list_collections)
    test_operation("Create Collection", create_test_collection)
    test_operation("Add Point", add_point_to_collection)
    test_operation("Search", search_in_collection)
    test_operation("Delete Point", delete_point)
    
    print("\nDemo completed! In a real Qdrant setup with properly configured API keys:")
    print("- Admin key should succeed on all operations")
    print("- Read-only key should only succeed on list_collections and search_in_collection")
    print("- Collection-specific key should only work on its allowed collections")
    
    print("\nIf all operations succeeded in this demo, it means your Qdrant instance")
    print("is not configured with API key restrictions, or the keys used have full access.")
