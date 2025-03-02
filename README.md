# Qdrant Vector Database Tutorial

This repository contains a comprehensive tutorial for learning Qdrant vector database with Python.

## Prerequisites

- Python 3.7+
- Docker (for running Qdrant)
- Qdrant running on http://localhost:6333

## Getting Started with Qdrant

If you haven't already started Qdrant with Docker, you can do so with:

```bash
docker pull qdrant/qdrant
docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

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
5. **qdrant_security.md** - Guide to securing Qdrant with API keys and best practices
6. **api_key_example.py** - Example of how to use API keys with Qdrant
7. **advanced_api_key_usage.py** - Advanced example of using different API keys with different permission levels

## Running the Examples

Each Python file is a standalone script that you can run:

```bash
python 01_basic_operations.py
python 02_semantic_search.py
python 03_advanced_features.py
python api_key_example.py
python advanced_api_key_usage.py
```

## What You'll Learn

- Basic concepts of vector databases
- How to connect to Qdrant from Python
- Creating and managing collections
- Adding vectors with metadata (payload)
- Performing vector similarity search
- Filtering search results
- Advanced operations like batch processing, pagination, and the scroll API
- Collection management operations
- Updating and deleting vectors
- Securing Qdrant with API keys
- Implementing different permission levels for API keys

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
