#!/usr/bin/env python3
"""
Qdrant API Key Management Script

This script allows you to create, list, and delete API keys for a running Qdrant instance
using the REST API.
"""

import requests
import json
import argparse
import uuid

# Default Qdrant endpoint
QDRANT_HOST = "http://localhost:6333"

def create_api_key(name, actions=None, collections=None, host=QDRANT_HOST):
    """
    Create a new API key with specified permissions.
    
    Args:
        name: Name for the API key
        actions: List of allowed actions (e.g., ["read", "write"])
        collections: List of allowed collections (None for all collections)
        host: Qdrant host URL
    
    Returns:
        The created API key information
    """
    url = f"{host}/api/v1/api-keys"
    
    # Prepare the request body
    body = {
        "name": name,
    }
    
    # Add actions if specified
    if actions:
        body["actions"] = actions
    
    # Add collections if specified
    if collections:
        body["collections"] = collections
    
    # Make the request
    response = requests.post(url, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error creating API key: {response.status_code}")
        print(response.text)
        return None

def list_api_keys(host=QDRANT_HOST):
    """
    List all API keys.
    
    Args:
        host: Qdrant host URL
    
    Returns:
        List of API keys
    """
    url = f"{host}/api/v1/api-keys"
    
    # Make the request
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error listing API keys: {response.status_code}")
        print(response.text)
        return None

def delete_api_key(key_id, host=QDRANT_HOST):
    """
    Delete an API key.
    
    Args:
        key_id: ID of the API key to delete
        host: Qdrant host URL
    
    Returns:
        True if successful, False otherwise
    """
    url = f"{host}/api/v1/api-keys/{key_id}"
    
    # Make the request
    response = requests.delete(url)
    
    if response.status_code == 200:
        return True
    else:
        print(f"Error deleting API key: {response.status_code}")
        print(response.text)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage Qdrant API keys")
    parser.add_argument("--host", default=QDRANT_HOST, help="Qdrant host URL")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create API key command
    create_parser = subparsers.add_parser("create", help="Create a new API key")
    create_parser.add_argument("--name", default=f"key-{uuid.uuid4().hex[:8]}", help="Name for the API key")
    create_parser.add_argument("--read", action="store_true", help="Allow read access")
    create_parser.add_argument("--write", action="store_true", help="Allow write access")
    create_parser.add_argument("--collections", nargs="+", help="Allowed collections (space-separated)")
    
    # List API keys command
    list_parser = subparsers.add_parser("list", help="List all API keys")
    
    # Delete API key command
    delete_parser = subparsers.add_parser("delete", help="Delete an API key")
    delete_parser.add_argument("key_id", help="ID of the API key to delete")
    
    args = parser.parse_args()
    
    if args.command == "create":
        # Determine actions based on flags
        actions = []
        if args.read:
            actions.append("read")
        if args.write:
            actions.append("write")
        
        # Create the API key
        result = create_api_key(
            name=args.name,
            actions=actions if actions else None,
            collections=args.collections,
            host=args.host
        )
        
        if result:
            print("API key created successfully:")
            print(f"Name: {result['name']}")
            print(f"Key: {result['key']}")
            print(f"ID: {result['id']}")
            if "actions" in result:
                print(f"Actions: {', '.join(result['actions'])}")
            if "collections" in result:
                print(f"Collections: {', '.join(result['collections'])}")
    
    elif args.command == "list":
        # List all API keys
        result = list_api_keys(host=args.host)
        
        if result and "keys" in result:
            print(f"Found {len(result['keys'])} API keys:")
            for key in result["keys"]:
                print(f"\nName: {key['name']}")
                print(f"ID: {key['id']}")
                if "actions" in key:
                    print(f"Actions: {', '.join(key['actions'])}")
                if "collections" in key:
                    print(f"Collections: {', '.join(key['collections'])}")
    
    elif args.command == "delete":
        # Delete an API key
        success = delete_api_key(key_id=args.key_id, host=args.host)
        
        if success:
            print(f"API key {args.key_id} deleted successfully")
    
    else:
        parser.print_help()
