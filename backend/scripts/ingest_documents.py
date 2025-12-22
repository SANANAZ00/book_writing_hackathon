#!/usr/bin/env python3
"""
Document ingestion script for RAG chatbot
Parses MDX files, cleans text, and chunks content for vector storage
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Any

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.document_service import DocumentProcessor
from app.utils.text_processing import clean_mdx_content, semantic_chunking

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Ingest MDX documents for RAG chatbot')
    parser.add_argument('--input-dir', required=True, help='Directory containing MDX files')
    parser.add_argument('--output-dir', help='Directory to save processed chunks (optional)')
    parser.add_argument('--chunk-size', type=int, default=1000, help='Maximum chunk size in characters')
    parser.add_argument('--overlap', type=int, default=200, help='Overlap between chunks in characters')
    parser.add_argument('--dry-run', action='store_true', help='Process but don\'t save chunks')

    args = parser.parse_args()

    # Validate input directory
    input_path = Path(args.input_dir)
    if not input_path.exists() or not input_path.is_dir():
        logger.error(f"Input directory does not exist: {args.input_dir}")
        sys.exit(1)

    # Set up document processor
    processor = DocumentProcessor()
    processor.chunk_size = args.chunk_size
    processor.overlap = args.overlap

    logger.info(f"Starting document ingestion from: {input_path}")
    logger.info(f"Chunk size: {args.chunk_size}, Overlap: {args.overlap}")

    try:
        # Process all documents
        chunks = processor.process_directory(str(input_path))

        logger.info(f"Processed {len(chunks)} document chunks")

        if args.dry_run:
            logger.info("Dry run completed. No files were saved.")
            # Print sample of chunks for verification
            if chunks:
                logger.info(f"Sample chunk (first 200 chars): {chunks[0]['content'][:200]}...")
        else:
            # Save chunks if output directory is specified
            if args.output_dir:
                output_path = Path(args.output_dir)
                output_path.mkdir(parents=True, exist_ok=True)

                # Save chunks to JSON file
                import json
                output_file = output_path / "document_chunks.json"

                # Prepare chunks for JSON serialization (remove non-serializable objects)
                serializable_chunks = []
                for chunk in chunks:
                    serializable_chunk = {
                        'content': chunk['content'],
                        'metadata': {k: str(v) for k, v in chunk['metadata'].items()}
                    }
                    serializable_chunks.append(serializable_chunk)

                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(serializable_chunks, f, indent=2, ensure_ascii=False)

                logger.info(f"Saved {len(chunks)} chunks to {output_file}")

            # Print summary
            logger.info("Document ingestion completed successfully!")
            logger.info(f"Total chunks created: {len(chunks)}")

            # Print some statistics
            if chunks:
                avg_chunk_size = sum(len(chunk['content']) for chunk in chunks) / len(chunks)
                logger.info(f"Average chunk size: {avg_chunk_size:.2f} characters")

                # Count by source
                sources = {}
                for chunk in chunks:
                    source = chunk['metadata'].get('relative_path', 'unknown')
                    sources[source] = sources.get(source, 0) + 1

                logger.info(f"Chunks by source:")
                for source, count in sources.items():
                    logger.info(f"  {source}: {count} chunks")

    except Exception as e:
        logger.error(f"Error during document ingestion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()