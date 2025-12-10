#!/usr/bin/env python3
"""
Script to generate and upload embeddings for all book content to Qdrant
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to the path so we can import from the app
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_embeddings import main as generate_embeddings_main

async def run_embeddings():
    """
    Run the embedding generation process
    """
    print("Starting RAG embedding generation process...")
    print("=" * 50)

    try:
        # Run the main embedding generation process
        await generate_embeddings_main()

        print("=" * 50)
        print("RAG embedding generation completed successfully!")

    except Exception as e:
        print(f"Error during embedding generation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Change to the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Run the embedding generation
    asyncio.run(run_embeddings())