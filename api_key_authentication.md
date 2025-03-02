# Qdrant API Key Authentication Guide

This guide explains how to set up and use API key authentication with Qdrant vector database.

## API Key Types

Qdrant supports two types of API keys:

1. **Admin API Key**: Full access to all operations (read and write)
2. **Read-Only API Key**: Limited to read operations only

## Setting Up API Keys

### Option 1: Using Docker Environment Variables

```bash
docker run -d --name qdrant-secured \
  -p 6333:6333 -p 6334:6334 \
  -v /path/to/storage:/qdrant/storage \
  -e QDRANT__SERVICE__API_KEY=my-secure-admin-key-123 \
  -e QDRANT__SERVICE__READ_ONLY_API_KEY=my-secure-readonly-key-456 \
  qdrant/qdrant
```

### Option 2: Using Configuration File (qdrant_config.yaml)

```yaml
service:
  # Admin API key with full access
  api_key: my-secure-admin-key-123
  
  # Read-only API key
  read_only_api_key: my-secure-readonly-key-456
```

## Connecting with API Keys in Python

### Admin Key (Full Access)

```python
from qdrant_client import QdrantClient

admin_client = QdrantClient(
    host="localhost",
    port=6333,
    api_key="my-secure-admin-key-123",
    https=False  # Set to True if using HTTPS
)
```

### Read-Only Key (Read Access Only)

```python
from qdrant_client import QdrantClient

readonly_client = QdrantClient(
    host="localhost",
    port=6333,
    api_key="my-secure-readonly-key-456",
    https=False  # Set to True if using HTTPS
)
```

## API Key Access Levels

| Operation | Admin Key | Read-Only Key |
|-----------|-----------|---------------|
| List collections | ✅ | ✅ |
| Get collection info | ✅ | ✅ |
| Search vectors | ✅ | ✅ |
| Retrieve points | ✅ | ✅ |
| Create collection | ✅ | ❌ |
| Delete collection | ✅ | ❌ |
| Add vectors | ✅ | ❌ |
| Update vectors | ✅ | ❌ |
| Delete vectors | ✅ | ❌ |

## Best Practices

1. **Use Strong, Random API Keys**: Generate secure, random strings for your API keys.
2. **Use HTTPS in Production**: Always use HTTPS in production environments.
3. **Least Privilege Access**: Use read-only keys for applications that only need to search.
4. **Rotate Keys Regularly**: Change your API keys periodically for better security.
5. **Environment Variables**: Store API keys in environment variables, not in code.
6. **Different Keys for Different Services**: Use different API keys for different services or applications.

## Testing API Key Authentication

Use the `test_api_keys.py` script to test your API key configuration:

```bash
python test_api_keys.py
```

## Example: Admin vs Read-Only Keys

The `admin_vs_readonly.py` script demonstrates the difference between admin and read-only keys:

```bash
python admin_vs_readonly.py
```

## Troubleshooting

- **401 Unauthorized**: Invalid API key
- **403 Forbidden**: Valid API key but insufficient permissions
- **Warning about insecure connection**: Set `https=True` if using HTTPS

## Security Considerations

- API keys should be treated as sensitive credentials
- Never commit API keys to version control
- Use environment variables or secure secret management
- For production, consider using HTTPS and additional security measures
