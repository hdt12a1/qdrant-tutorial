#!/usr/bin/env python3
"""
Qdrant API Key Authentication Example

This script demonstrates how to connect to Qdrant with API key authentication.
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models

# Method 1: Providing API key directly to the client
client = QdrantClient(
    host="localhost",
    port=6333,
    api_key="your-secret-api-key"  # Replace with your actual API key
)

# Method 2: Using environment variables (more secure)
# First, set the environment variable:
# export QDRANT_API_KEY=your-secret-api-key
# Then, in your code:
import os
from qdrant_client import QdrantClient

client = QdrantClient(
    host="localhost",
    port=6333,
    api_key=os.environ.get("QDRANT_API_KEY")
)

# Method 3: Using a configuration file
# Create a config.json file with your API key
# {
#     "api_key": "your-secret-api-key"
# }
# Then, in your code:
import json

def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        return json.load(f)

config = load_config()
client = QdrantClient(
    host="localhost",
    port=6333,
    api_key=config.get("api_key")
)

# Example of using the authenticated client
try:
    # This will only work if the API key is valid
    collections = client.get_collections()
    print(f"Successfully authenticated! Found {len(collections.collections)} collections.")
except Exception as e:
    print(f"Authentication failed: {e}")
