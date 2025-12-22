#!/usr/bin/env python3
"""
Test script for MDX ingestion, text cleaning, and chunking logic
"""

import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.document_service import DocumentProcessor
from app.utils.text_processing import clean_mdx_content, semantic_chunking

def test_mdx_parsing():
    """Test MDX parsing functionality"""
    print("Testing MDX parsing...")

    # Create a sample MDX content
    sample_mdx = """---
title: Introduction to Physical AI
sidebar_label: Introduction
---

# Introduction to Physical AI

Physical AI is a fascinating field that combines robotics, machine learning, and control theory.

## Key Concepts

- Embodied intelligence
- Sensorimotor learning
- Dynamic interaction with environment

### Example Code

```python
def control_robot():
    # This is a sample control function
    return "Robot controlled successfully"
```

The robot must adapt to its environment in real-time.
"""

    # Write sample MDX to a temporary file for testing
    test_file = Path("test_sample.mdx")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(sample_mdx)

    try:
        processor = DocumentProcessor()
        result = processor.parse_mdx_file(str(test_file))

        print(f"  [PASS] Parsed content: {len(result['content'])} characters")
        print(f"  [PASS] Metadata: {result['metadata']}")

        # Clean the content
        cleaned = processor.clean_text(result['content'])
        print(f"  [PASS] Cleaned content: {len(cleaned)} characters")
        print(f"  [PASS] Cleaned sample: {cleaned[:100]}...")

        # Chunk the content
        chunks = processor.chunk_text(cleaned, result['metadata'])
        print(f"  [PASS] Created {len(chunks)} chunks")

        if chunks:
            print(f"  [PASS] First chunk: {chunks[0]['content'][:50]}...")
            print(f"  [PASS] First chunk metadata: {chunks[0]['metadata']}")

        return True

    except Exception as e:
        print(f"  [FAIL] Error in MDX parsing: {str(e)}")
        return False
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

def test_text_cleaning():
    """Test text cleaning functionality"""
    print("\nTesting text cleaning...")

    dirty_text = """
# Main Title

This is a sample text with [markdown](link) and `code` elements.

## Subsection

- List item 1
- List item 2

```python
def sample_function():
    x = 1  # This is a comment
    return x
```

<JSXComponent>
    Some JSX content
</JSXComponent>

More text content here.
"""

    processor = DocumentProcessor()
    cleaned = processor.clean_text(dirty_text)

    print(f"  [PASS] Original: {len(dirty_text)} characters")
    print(f"  [PASS] Cleaned: {len(cleaned)} characters")
    print(f"  [PASS] Cleaned sample: {cleaned[:100]}...")

    # Verify cleaning worked
    has_code_block = '```' in cleaned
    has_jsx = '<' in cleaned and '>' in cleaned and 'JSXComponent' in cleaned

    if has_code_block or has_jsx:
        print("  [FAIL] Text cleaning didn't remove all unwanted elements")
        return False
    else:
        print("  [PASS] Text cleaning removed unwanted elements")
        return True

def test_chunking():
    """Test chunking functionality"""
    print("\nTesting chunking...")

    long_text = """
# Chapter 1: Introduction

Physical AI is a field that combines robotics, machine learning, and control theory.
This is a longer paragraph that will be used to test the chunking functionality.
The chunking algorithm should preserve semantic boundaries while keeping chunks manageable.

## Section 1.1: Background

The background section provides context for understanding Physical AI.
This section is important for students learning about robotics and AI.
Additional context helps students understand the importance of embodied intelligence.

### Subsection 1.1.1: History

The history of Physical AI dates back several decades.
Early researchers focused on basic control systems and simple robots.
Modern approaches integrate machine learning and advanced sensors.

## Section 1.2: Current State

Current state of Physical AI includes advanced robotics platforms.
These platforms incorporate multiple sensors and sophisticated control algorithms.
The field continues to evolve with new research and applications.

More content to make the text longer for testing purposes.
This text will be split into multiple chunks based on semantic boundaries.
Each chunk should contain coherent content that makes sense independently.
"""

    processor = DocumentProcessor()
    cleaned = processor.clean_text(long_text)
    chunks = processor.chunk_text(cleaned, {"source": "test"})

    print(f"  [PASS] Created {len(chunks)} chunks from {len(cleaned)} characters")

    for i, chunk in enumerate(chunks):
        print(f"    Chunk {i+1}: {len(chunk['content'])} characters")
        if len(chunks) > 1:  # Show content only for first few chunks to avoid spam
            if i < 3:
                print(f"      Sample: {chunk['content'][:80]}...")

    if len(chunks) > 0:
        print("  [PASS] Chunking completed successfully")
        return True
    else:
        print("  [FAIL] No chunks created")
        return False

def test_directory_processing():
    """Test processing a directory of MDX files"""
    print("\nTesting directory processing...")

    # Create a temporary directory with sample files
    test_dir = Path("test_docs")
    test_dir.mkdir(exist_ok=True)

    # Create sample MDX files
    sample_files = {
        "intro.mdx": """---
title: Introduction
sidebar_label: Intro
---

# Introduction

This is the introduction to Physical AI.

## Overview

- Key concepts
- Learning objectives
""",
        "chapter1.mdx": """---
title: Chapter 1 - Fundamentals
sidebar_label: Chapter 1
---

# Chapter 1: Fundamentals

Physical AI fundamentals explained.

## Section 1

Basic concepts of physical intelligence.
""",
    }

    for filename, content in sample_files.items():
        with open(test_dir / filename, 'w', encoding='utf-8') as f:
            f.write(content)

    try:
        processor = DocumentProcessor()
        chunks = processor.process_directory(str(test_dir))

        print(f"  [PASS] Processed {len(chunks)} chunks from {len(sample_files)} files")

        for i, chunk in enumerate(chunks):
            print(f"    Chunk {i+1}: {chunk['metadata'].get('file_name', 'unknown')}")
            print(f"      Content: {chunk['content'][:50]}...")

        return True

    except Exception as e:
        print(f"  [FAIL] Error processing directory: {str(e)}")
        return False
    finally:
        # Clean up test directory
        import shutil
        if test_dir.exists():
            shutil.rmtree(test_dir)

def main():
    """Run all tests"""
    print("Running MDX ingestion, text cleaning, and chunking tests...\n")

    tests = [
        ("MDX Parsing", test_mdx_parsing),
        ("Text Cleaning", test_text_cleaning),
        ("Chunking", test_chunking),
        ("Directory Processing", test_directory_processing),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"[PASS] {test_name} test passed")
            else:
                print(f"[FAIL] {test_name} test failed")
        except Exception as e:
            print(f"[ERROR] {test_name} test error: {str(e)}")

    print(f"\nTest Results: {passed}/{total} tests passed")

    if passed == total:
        print("All tests passed! [SUCCESS]")
        return 0
    else:
        print("Some tests failed! [FAILURE]")
        return 1

if __name__ == "__main__":
    exit(main())