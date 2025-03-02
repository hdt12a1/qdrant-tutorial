#!/usr/bin/env python3
"""
Qdrant Admin vs Read-Only API Key Example

This script demonstrates the difference between using an admin API key and a read-only API key.
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
import time

# Define API keys
ADMIN_KEY = "my-secure-admin-key-123"
READONLY_KEY = "my-secure-readonly-key-456"

# Collection name for testing
COLLECTION_NAME = "api_key_test_collection"

print("Qdrant Admin vs Read-Only API Key Example")
print("========================================\n")

# Connect with admin key
print("Connecting with admin key...")
admin_client = QdrantClient(
    host="localhost",
    port=6333,
    api_key=ADMIN_KEY,
    https=False  # Set to True if using HTTPS
)

# Connect with read-only key
print("Connecting with read-only key...")
readonly_client = QdrantClient(
    host="localhost",
    port=6333,
    api_key=READONLY_KEY,
    https=False  # Set to True if using HTTPS
)

# Clean up any existing test collection
try:
    admin_client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Deleted existing collection '{COLLECTION_NAME}'")
except:
    pass

print("\n--- Testing Admin Key ---")

# 1. Create collection with admin key
try:
    admin_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=4,
            distance=models.Distance.COSINE
        )
    )
    print(f"✅ Admin key: Created collection '{COLLECTION_NAME}'")
except Exception as e:
    print(f"❌ Admin key: Failed to create collection: {e}")

# 2. Add vectors with admin key
try:
    admin_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=1,
                vector=[0.1, 0.2, 0.3, 0.4],
                payload={"name": "Point 1"}
            ),
            models.PointStruct(
                id=2,
                vector=[0.2, 0.3, 0.4, 0.5],
                payload={"name": "Point 2"}
            )
        ]
    )
    print(f"✅ Admin key: Added vectors to collection")
except Exception as e:
    print(f"❌ Admin key: Failed to add vectors: {e}")

# 3. Search with admin key
try:
    results = admin_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=[0.1, 0.2, 0.3, 0.4],
        limit=2
    )
    print(f"✅ Admin key: Searched collection and found {len(results)} results")
except Exception as e:
    print(f"❌ Admin key: Failed to search: {e}")

print("\n--- Testing Read-Only Key ---")

# 1. Try to create collection with read-only key (should fail)
try:
    readonly_client.create_collection(
        collection_name=f"{COLLECTION_NAME}_readonly",
        vectors_config=models.VectorParams(
            size=4,
            distance=models.Distance.COSINE
        )
    )
    print(f"❌ Read-only key: Created collection (unexpected success)")
except Exception as e:
    print(f"✅ Read-only key: Failed to create collection as expected: {e}")

# 2. Try to add vectors with read-only key (should fail)
try:
    readonly_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=3,
                vector=[0.3, 0.4, 0.5, 0.6],
                payload={"name": "Point 3"}
            )
        ]
    )
    print(f"❌ Read-only key: Added vectors (unexpected success)")
except Exception as e:
    print(f"✅ Read-only key: Failed to add vectors as expected: {e}")

# 3. Search with read-only key (should succeed)
try:
    results = readonly_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=[0.1, 0.2, 0.3, 0.4],
        limit=2
    )
    print(f"✅ Read-only key: Searched collection and found {len(results)} results")
except Exception as e:
    print(f"❌ Read-only key: Failed to search: {e}")

# Clean up
print("\n--- Cleaning Up ---")
try:
    admin_client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"✅ Admin key: Deleted test collection '{COLLECTION_NAME}'")
except Exception as e:
    print(f"❌ Admin key: Failed to delete collection: {e}")

print("\nExample completed!")
