# Qdrant Vector Database Tutorial

This repository contains a comprehensive tutorial for learning Qdrant vector database with Python.

## Prerequisites

- Python 3.7+
- Docker (for running Qdrant)
- Qdrant running on http://localhost:6333

## Getting Started with Qdrant

### Basic Setup (No Authentication)

If you want to start Qdrant without authentication for local development:

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

### Secure Setup with API Keys

For a more secure setup with API key authentication:

```bash
docker run -d --name qdrant-secured \
  -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  -e QDRANT__SERVICE__API_KEY=my-secure-admin-key-123 \
  -e QDRANT__SERVICE__READ_ONLY_API_KEY=my-secure-readonly-key-456 \
  qdrant/qdrant
```

This sets up:
- An admin API key (`my-secure-admin-key-123`) with full access
- A read-only API key (`my-secure-readonly-key-456`) for search operations only

## Required Python Packages

Install the required packages:

```bash
pip install qdrant-client numpy sentence-transformers
```

## Tutorial Structure

This tutorial is organized into several files:

1. **qdrant_basics.md** - Conceptual introduction to Qdrant and vector databases
2. **01_basic_operations.py** - Basic operations with Qdrant (connecting, creating collections, adding vectors, basic search)
3. **02_semantic_search.py** - Using Qdrant for semantic search with text embeddings
4. **03_advanced_features.py** - Advanced Qdrant features (batch operations, complex filtering, pagination, collection management)

### Security and API Key Authentication

5. **qdrant_security.md** - Guide to securing Qdrant with API keys and best practices
6. **api_key_authentication.md** - Comprehensive guide to API key authentication in Qdrant
7. **api_key_example.py** - Example of how to use API keys with Qdrant
8. **advanced_api_key_usage.py** - Advanced example of using different API keys with different permission levels
9. **test_api_keys.py** - Script to test API key authentication with Qdrant
10. **admin_vs_readonly.py** - Demonstration of the difference between admin and read-only API keys

## Running the Examples

Each Python file is a standalone script that you can run:

### Basic Operations
```bash
python 01_basic_operations.py
python 02_semantic_search.py
python 03_advanced_features.py
```

### Security and API Key Examples
```bash
# Start Qdrant with API key authentication first
docker run -d --name qdrant-secured \
  -p 6333:6333 -p 6334:6334 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  -e QDRANT__SERVICE__API_KEY=my-secure-admin-key-123 \
  -e QDRANT__SERVICE__READ_ONLY_API_KEY=my-secure-readonly-key-456 \
  qdrant/qdrant

# Then run the security examples
python test_api_keys.py
python admin_vs_readonly.py
python api_key_example.py
python advanced_api_key_usage.py
```

## What You'll Learn

### Vector Database Fundamentals
- Basic concepts of vector databases
- How to connect to Qdrant from Python
- Creating and managing collections
- Adding vectors with metadata (payload)
- Performing vector similarity search
- Filtering search results

### Advanced Operations
- Batch processing for efficient vector operations
- Pagination and scroll API for large result sets
- Collection management operations
- Updating and deleting vectors

### Security and Access Control
- Securing Qdrant with API key authentication
- Implementing admin and read-only permission levels
- Best practices for API key management
- Testing API key authentication
- Configuring Qdrant for secure deployments

## Additional Resources

- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Python Client](https://github.com/qdrant/qdrant-client)
- [Sentence Transformers Documentation](https://www.sbert.net/)

## Next Steps

After completing this tutorial, you can:

1. Integrate Qdrant into your own applications
2. Experiment with different embedding models
3. Explore more advanced features like quantization and clustering
4. Scale up to larger datasets
5. Deploy Qdrant in a production environment
