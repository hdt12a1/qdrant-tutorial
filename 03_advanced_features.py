#!/usr/bin/env python3
"""
Qdrant Advanced Features Tutorial

This script demonstrates more advanced operations with Qdrant:
1. Batch operations
2. Complex filtering with multiple conditions
3. Pagination
4. Collection management
5. Working with scroll API
6. Deleting points
"""

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
import time

print("Qdrant Advanced Features Tutorial")
print("=================================\n")

# Step 1: Connect to Qdrant
print("Step 1: Connecting to Qdrant server...")
client = QdrantClient(host="localhost", port=6333)
print("Connected successfully!\n")

# Step 2: Load embedding model
print("Step 2: Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
vector_size = model.get_sentence_embedding_dimension()
print(f"Loaded model with vector size: {vector_size}\n")

# Step 3: Create a new collection for this tutorial
print("Step 3: Creating a collection...")
collection_name = "articles"

# Check if collection exists and recreate it
collections = client.get_collections()
collection_names = [collection.name for collection in collections.collections]

if collection_name in collection_names:
    print(f"Collection '{collection_name}' already exists. Recreating it...")
    client.delete_collection(collection_name=collection_name)

# Create the collection
client.create_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE,
    )
)
print(f"Collection '{collection_name}' created successfully!\n")

# Step 4: Prepare sample articles data
print("Step 4: Preparing sample data...")
articles = [
    {
        "id": 101,
        "title": "Introduction to Machine Learning",
        "content": "Machine learning is a branch of artificial intelligence that focuses on building systems that learn from data.",
        "author": "Jane Smith",
        "date": "2023-01-15",
        "tags": ["AI", "ML", "technology"],
        "read_time": 5,
        "popularity": 0.85
    },
    {
        "id": 102,
        "title": "Deep Learning Fundamentals",
        "content": "Deep learning is a subset of machine learning that uses neural networks with many layers.",
        "author": "John Doe",
        "date": "2023-02-20",
        "tags": ["AI", "deep learning", "neural networks"],
        "read_time": 8,
        "popularity": 0.92
    },
    {
        "id": 103,
        "title": "Python for Data Science",
        "content": "Python has become the most popular programming language for data science due to its simplicity and powerful libraries.",
        "author": "Jane Smith",
        "date": "2023-03-10",
        "tags": ["Python", "data science", "programming"],
        "read_time": 6,
        "popularity": 0.78
    },
    {
        "id": 104,
        "title": "Natural Language Processing Techniques",
        "content": "NLP combines linguistics, computer science, and AI to help computers understand human language.",
        "author": "Mike Johnson",
        "date": "2023-04-05",
        "tags": ["NLP", "AI", "linguistics"],
        "read_time": 10,
        "popularity": 0.81
    },
    {
        "id": 105,
        "title": "Introduction to Vector Databases",
        "content": "Vector databases are specialized systems designed to store and query high-dimensional vectors efficiently.",
        "author": "Sarah Williams",
        "date": "2023-05-12",
        "tags": ["databases", "vectors", "similarity search"],
        "read_time": 7,
        "popularity": 0.75
    },
    {
        "id": 106,
        "title": "Qdrant: A Modern Vector Database",
        "content": "Qdrant is a vector similarity search engine that provides a production-ready service with a convenient API.",
        "author": "Alex Brown",
        "date": "2023-06-18",
        "tags": ["Qdrant", "vectors", "similarity search"],
        "read_time": 9,
        "popularity": 0.88
    },
    {
        "id": 107,
        "title": "Building Recommendation Systems",
        "content": "Recommendation systems use collaborative filtering and content-based methods to suggest items to users.",
        "author": "John Doe",
        "date": "2023-07-22",
        "tags": ["recommendations", "ML", "collaborative filtering"],
        "read_time": 12,
        "popularity": 0.91
    },
    {
        "id": 108,
        "title": "Data Visualization Best Practices",
        "content": "Effective data visualization makes complex data more accessible, understandable, and usable.",
        "author": "Lisa Chen",
        "date": "2023-08-30",
        "tags": ["visualization", "data", "design"],
        "read_time": 6,
        "popularity": 0.79
    }
]

print(f"Prepared {len(articles)} sample articles.\n")

# Step 5: Batch upload vectors
print("Step 5: Preparing batch upload...")
points = []

for article in articles:
    # Generate embedding vector for article content
    content_text = f"{article['title']}. {article['content']}"
    vector = model.encode(content_text)
    
    # Prepare payload
    payload = {
        "title": article["title"],
        "content": article["content"],
        "author": article["author"],
        "date": article["date"],
        "tags": article["tags"],
        "read_time": article["read_time"],
        "popularity": article["popularity"]
    }
    
    # Create point
    point = models.PointStruct(
        id=article["id"],
        vector=vector.tolist(),
        payload=payload
    )
    
    points.append(point)

# Batch upload all points at once
print(f"Uploading {len(points)} articles in a single batch...")
client.upsert(
    collection_name=collection_name,
    points=points
)

print("Batch upload complete.\n")

# Step 6: Complex filtering
print("Step 6: Complex Filtering Example...")
query = "artificial intelligence and machine learning"
query_vector = model.encode(query)

# Search for articles:
# - by Jane Smith OR John Doe
# - AND with read time less than 10 minutes
# - AND with popularity greater than 0.8
complex_results = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="read_time",
                range=models.Range(lt=10)  # Less than 10 minutes
            ),
            models.FieldCondition(
                key="popularity",
                range=models.Range(gt=0.8)  # Greater than 0.8
            )
        ],
        should=[
            models.FieldCondition(
                key="author",
                match=models.MatchValue(value="Jane Smith")
            ),
            models.FieldCondition(
                key="author",
                match=models.MatchValue(value="John Doe")
            )
        ],
        min_should=1  # At least one of the "should" conditions must be met
    ),
    limit=5
)

print(f"Query: '{query}' with complex filtering")
print("Results:")
for i, result in enumerate(complex_results, 1):
    print(f"  {i}. {result.payload['title']} by {result.payload['author']} (Score: {result.score:.4f})")
    print(f"     Read time: {result.payload['read_time']} min, Popularity: {result.payload['popularity']}")

# Step 7: Pagination example
print("\nStep 7: Pagination Example...")
query = "data"
query_vector = model.encode(query)

# First page (2 results)
page_1 = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=2,
    offset=0  # Start from the beginning
)

print(f"Query: '{query}' - Page 1 (2 results):")
for i, result in enumerate(page_1, 1):
    print(f"  {i}. {result.payload['title']} (Score: {result.score:.4f})")

# Second page (2 more results)
page_2 = client.search(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=2,
    offset=2  # Skip the first 2 results
)

print(f"\nQuery: '{query}' - Page 2 (2 results):")
for i, result in enumerate(page_2, 1):
    print(f"  {i}. {result.payload['title']} (Score: {result.score:.4f})")

# Step 8: Using the scroll API for iterating through results
print("\nStep 8: Scroll API Example...")
query = "vectors and databases"
query_vector = model.encode(query)

# Get the first batch with scroll_id
scroll_batch, scroll_id = client.scroll(
    collection_name=collection_name,
    query_vector=query_vector,
    limit=2,  # Get 2 results per batch
    with_payload=True,
    with_vectors=False  # We don't need the actual vectors
)

print(f"Query: '{query}' - Scroll batch 1:")
for i, result in enumerate(scroll_batch, 1):
    print(f"  {i}. {result.payload['title']}")

# Get the next batch using the scroll_id
if scroll_id:
    next_batch, next_scroll_id = client.scroll(
        collection_name=collection_name,
        scroll_id=scroll_id,  # Use the scroll_id from the previous request
        limit=2,
        with_payload=True,
        with_vectors=False
    )
    
    print(f"\nQuery: '{query}' - Scroll batch 2:")
    for i, result in enumerate(next_batch, 1):
        print(f"  {i}. {result.payload['title']}")

# Step 9: Demonstrate collection management operations
print("\nStep 9: Collection Management...")

# List all collections
collections = client.get_collections()
print(f"Available collections: {[collection.name for collection in collections.collections]}")

# Get detailed collection info
collection_info = client.get_collection(collection_name=collection_name)
print(f"\nCollection '{collection_name}' details:")
print(f"- Vector size: {collection_info.config.params.vectors.size}")
print(f"- Distance function: {collection_info.config.params.vectors.distance}")
print(f"- Number of vectors: {collection_info.vectors_count}")

# Step 10: Demonstrate deleting points
print("\nStep 10: Deleting Points...")
# Delete a specific point by ID
point_to_delete = 101
client.delete(
    collection_name=collection_name,
    points_selector=models.PointIdsList(
        points=[point_to_delete]
    )
)
print(f"Deleted point with ID: {point_to_delete}")

# Verify deletion
result = client.retrieve(
    collection_name=collection_name,
    ids=[point_to_delete]
)
if not result:
    print(f"Point {point_to_delete} was successfully deleted.")

# Step 11: Demonstrate conditional deletion
print("\nStep 11: Conditional Deletion...")
# Delete all articles by a specific author
author_to_delete = "Lisa Chen"
client.delete(
    collection_name=collection_name,
    points_selector=models.FilterSelector(
        filter=models.Filter(
            must=[
                models.FieldCondition(
                    key="author",
                    match=models.MatchValue(value=author_to_delete)
                )
            ]
        )
    )
)
print(f"Deleted all articles by author: {author_to_delete}")

# Step 12: Demonstrate updating points
print("\nStep 12: Updating Points...")
# Update the popularity of an article
point_to_update = 102
client.update_vectors(
    collection_name=collection_name,
    points=[
        models.PointVectors(
            id=point_to_update,
            vector=model.encode("Deep Learning Fundamentals - Updated with new information about transformer models.").tolist()
        )
    ]
)
print(f"Updated vector for point with ID: {point_to_update}")

# Update payload for a point
client.update_payload(
    collection_name=collection_name,
    payload={"popularity": 0.95, "read_time": 9},
    points=[point_to_update]
)
print(f"Updated payload for point with ID: {point_to_update}")

# Verify update
updated_point = client.retrieve(
    collection_name=collection_name,
    ids=[point_to_update]
)
if updated_point:
    print(f"Updated point details:")
    print(f"- Title: {updated_point[0].payload['title']}")
    print(f"- Popularity: {updated_point[0].payload['popularity']}")
    print(f"- Read time: {updated_point[0].payload['read_time']}")

print("\nAdvanced Qdrant tutorial completed successfully!")
