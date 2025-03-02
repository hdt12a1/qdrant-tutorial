#!/usr/bin/env python3
"""
Test script to verify API key authentication with Qdrant
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.exceptions import UnexpectedResponse
import sys

def test_connection(api_key, key_name):
    print(f"\nTesting connection with {key_name}...")
    try:
        # Create client with the API key
        client = QdrantClient(
            host="localhost",
            port=6333,
            api_key=api_key,
            https=False  # Explicitly use HTTP instead of HTTPS
        )
        
        # Try to list collections (a read operation)
        try:
            collections = client.get_collections()
            print(f"✅ Read operation successful with {key_name}!")
            print(f"   Found {len(collections.collections)} collections")
        except Exception as e:
            print(f"❌ Read operation failed with {key_name}: {e}")
            return
        
        # Try to create a test collection (a write operation)
        collection_name = f"test_{key_name.replace('-', '_')}"
        try:
            # Delete if exists
            try:
                client.delete_collection(collection_name=collection_name)
            except:
                pass
                
            # Create collection
            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=4,
                    distance=models.Distance.COSINE
                )
            )
            print(f"✅ Write operation successful with {key_name}!")
            print(f"   Created collection '{collection_name}'")
            
            # Clean up
            client.delete_collection(collection_name=collection_name)
            print(f"   Deleted test collection")
            
        except Exception as e:
            print(f"❌ Write operation failed with {key_name}: {e}")
        
    except Exception as e:
        print(f"❌ Connection failed with {key_name}: {e}")

print("Qdrant API Key Authentication Test")
print("==================================")
print("Testing with both admin and read-only API keys")

if __name__ == "__main__":
    # Test with admin key (should have full access)
    test_connection("my-secure-admin-key-123", "admin-key")
    
    # Test with read-only key (should only have read access)
    test_connection("my-secure-readonly-key-456", "read-only-key")
    
    # Test with an invalid key (should be rejected)
    test_connection("invalid-key", "invalid-key")
