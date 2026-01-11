from qdrant_client import QdrantClient
from cohere import Client as CohereClient

# Initialize Qdrant
client = QdrantClient(
    url="https://e67ea417-4c6c-41bc-8f20-b5b0f2023fb9.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="YOUR_QDRANT_API_KEY"
)

# Initialize Cohere
co = CohereClient(api_key="YOUR_COHERE_API_KEY")

# Your query
query_text = "Lucy"

# Get embedding for the query
query_embedding = co.embed(
    model="embed-english-v3.0",
    texts=[query_text]
).embeddings[0]

# Search in Qdrant collection
results = client.search(
    collection_name="documentation",
    query_vector=query_embedding,
    limit=5
)

print("Search results:", results)
