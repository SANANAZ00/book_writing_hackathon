import os
import asyncio
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
from dotenv import load_dotenv
import markdown
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            prefer_grpc=True
        )
        self.cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
        # Using a simple tokenizer instead of tiktoken since we're using Cohere
        self.embedding_model = "embed-english-v3.0"

        # Create collection if it doesn't exist
        self._create_collection()

    def _create_collection(self):
        """Create Qdrant collection for documentation"""
        try:
            self.qdrant_client.get_collection("documentation")
            print("Collection 'documentation' already exists")
        except:
            self.qdrant_client.create_collection(
                collection_name="documentation",
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embedding dimension
                    distance=models.Distance.COSINE
                )
            )
            print("Created collection 'documentation'")

    def extract_text_from_mdx(self, mdx_content: str) -> str:
        """Extract clean text from MDX content"""
        # Convert MDX to HTML first (basic conversion for headings and paragraphs)
        # This is a simplified approach - in a real implementation, you'd want a more robust parser
        html_content = markdown.markdown(mdx_content)

        # Remove HTML tags to get clean text
        soup = BeautifulSoup(html_content, 'html.parser')
        clean_text = soup.get_text(separator=' ')

        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()

        return clean_text

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks using character-based splitting"""
        chunks = []
        start_idx = 0

        while start_idx < len(text):
            end_idx = start_idx + chunk_size

            # Extract chunk
            chunk_text = text[start_idx:end_idx]
            chunks.append(chunk_text)

            # Move start index with overlap
            start_idx = end_idx - overlap

            # Handle the case where remaining text is less than overlap
            if len(text) - end_idx < overlap:
                break

        return chunks
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Cohere"""
        try:
            response = self.cohere_client.embed(
                texts=[text],
                model=self.embedding_model,
                input_type="search_document"  # Required for newer Cohere embedding models
            )
            return response.embeddings[0]
        except cohere.errors.TooManyRequestsError:
            print("Rate limit hit, waiting 60 seconds before retrying...")
            time.sleep(60)
            # Retry once after rate limit
            response = self.cohere_client.embed(
                texts=[text],
                model=self.embedding_model,
                input_type="search_document"
            )
            return response.embeddings[0]


    async def process_document(self, file_path: Path, source_url: str) -> List[Dict[str, Any]]:
        """Process a single document file and return embedding points"""
        print(f"Processing: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract clean text from MDX
        clean_content = self.extract_text_from_mdx(content)

        # Split into chunks
        chunks = self.chunk_text(clean_content)

        points = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) == 0:
                continue

            # Generate embedding
            embedding = self.generate_embedding(chunk)

            # Create unique ID for the chunk
            chunk_id = hashlib.md5(f"{source_url}_chunk_{i}".encode()).hexdigest()

            # Create metadata
            metadata = {
                "source": source_url,
                "title": file_path.stem,
                "content": chunk[:200] + "..." if len(chunk) > 200 else chunk,  # Preview
                "chunk_index": i,
                "total_chunks": len(chunks)
            }

            point = models.PointStruct(
                id=chunk_id,
                vector=embedding,
                payload=metadata
            )

            points.append(point)

        print(f"Generated {len(points)} embeddings for {file_path}")
        return points

    async def process_directory(self, directory_path: str):
        """Process all MDX files in a directory"""
        directory = Path(directory_path)
        all_points = []

        # Find all MDX files
        mdx_files = list(directory.rglob("*.mdx")) + list(directory.rglob("*.md"))

        for file_path in mdx_files:
            # Generate source URL based on file path
            relative_path = file_path.relative_to(Path(directory_path))
            source_url = f"/docs/{relative_path.with_suffix('')}"

            points = await self.process_document(file_path, source_url)
            all_points.extend(points)

        print(f"Total points to upload: {len(all_points)}")
        return all_points

    async def upload_embeddings(self, points: List[models.PointStruct], batch_size: int = 100):
        """Upload embeddings to Qdrant in batches"""
        print(f"Uploading {len(points)} embeddings to Qdrant...")

        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]

            try:
                self.qdrant_client.upsert(
                    collection_name="documentation",
                    points=batch
                )
                print(f"Uploaded batch {i//batch_size + 1}/{(len(points)-1)//batch_size + 1}")
            except Exception as e:
                print(f"Error uploading batch {i//batch_size + 1}: {str(e)}")
                # Continue with next batch instead of failing completely
                continue

        print("Embedding upload completed!")

async def main():
    # Initialize the embedding generator
    generator = EmbeddingGenerator()

    # Process all documentation files
    docs_path = Path(r"D:\hackathon_book\book-writing\docs")
    if docs_path.exists():
        print("Processing documentation files...")
        points = await generator.process_directory(r"D:\hackathon_book\book-writing\docs")

        if points:
            # Upload to Qdrant
            await generator.upload_embeddings(points)
        else:
            print("No documentation files found to process.")
    else:
        print(f"Documentation directory {docs_path} does not exist.")

    print("Embedding generation process completed!")

if __name__ == "__main__":
    asyncio.run(main())