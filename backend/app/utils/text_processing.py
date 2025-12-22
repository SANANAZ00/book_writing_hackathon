import re
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

def clean_mdx_content(content: str) -> str:
    """
    Clean MDX content by removing code blocks, JSX components, and other non-text elements

    Args:
        content: Raw MDX content

    Returns:
        Cleaned text content
    """
    # Remove import/export statements
    content = re.sub(r'^\s*import\s+.*?;\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^\s*export\s+.*?;\s*$', '', content, flags=re.MULTILINE)

    # Remove JSX components and their content (handles both self-closing and paired tags)
    content = re.sub(r'<[^>]*>\s*{[^}]*}\s*</[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]*>\s*</[^>]*>', '', content, flags=re.DOTALL)
    content = re.sub(r'<[^>]*/>', '', content)

    # Remove code blocks (```...```)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)

    # Remove inline code (backticks)
    content = re.sub(r'`[^`]*`', '', content)

    # Remove HTML entities and tags
    content = re.sub(r'<[^>]*>', '', content)

    # Normalize whitespace
    content = re.sub(r'\s+', ' ', content)
    content = content.strip()

    # Remove excessive newlines
    content = re.sub(r'\n\s*\n', '\n\n', content)

    return content

def semantic_chunking(content: str, max_chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Perform semantic chunking of content based on natural boundaries

    Args:
        content: Text content to chunk
        max_chunk_size: Maximum size of each chunk
        overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    if not content.strip():
        return []

    # Split content into paragraphs
    paragraphs = content.split('\n\n')

    # Further split large paragraphs by sentences
    refined_paragraphs = []
    for para in paragraphs:
        if len(para) > max_chunk_size:
            # Split by sentences if paragraph is too large
            sentences = re.split(r'(?<=[.!?])\s+', para)
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk + " " + sentence) <= max_chunk_size:
                    if current_chunk:
                        current_chunk += " " + sentence
                    else:
                        current_chunk = sentence
                else:
                    if current_chunk.strip():
                        refined_paragraphs.append(current_chunk.strip())
                    current_chunk = sentence

            # Add the last chunk if it exists
            if current_chunk.strip():
                refined_paragraphs.append(current_chunk.strip())
        else:
            refined_paragraphs.append(para.strip())

    # Create chunks with overlap
    chunks = []
    current_chunk = ""

    for paragraph in refined_paragraphs:
        if not paragraph.strip():
            continue

        # If adding this paragraph would exceed max size
        if len(current_chunk + " " + paragraph) > max_chunk_size and current_chunk:
            chunks.append(current_chunk.strip())

            # Add overlap by taking the last part of the previous chunk
            if overlap > 0:
                words = current_chunk.split()
                overlap_start = max(0, len(words) - overlap)
                current_chunk = " ".join(words[overlap_start:])
            else:
                current_chunk = ""

        if current_chunk:
            current_chunk += " " + paragraph
        else:
            current_chunk = paragraph

    # Add the final chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def extract_semantic_boundaries(content: str) -> List[Tuple[int, int, str]]:
    """
    Extract semantic boundaries in the content (headers, sections, etc.)

    Args:
        content: Text content to analyze

    Returns:
        List of tuples (start_pos, end_pos, boundary_type)
    """
    boundaries = []

    # Find markdown headers
    header_pattern = r'^(#{1,6})\s+(.+)$'
    for match in re.finditer(header_pattern, content, flags=re.MULTILINE):
        header_level = len(match.group(1))
        header_text = match.group(2)
        boundaries.append((
            match.start(),
            match.end(),
            f'header_{header_level}'
        ))

    # Find list items
    list_pattern = r'^\s*[\*\-\+]\s+(.+)$'
    for match in re.finditer(list_pattern, content, flags=re.MULTILINE):
        boundaries.append((
            match.start(),
            match.end(),
            'list_item'
        ))

    return boundaries

def normalize_text(content: str) -> str:
    """
    Normalize text by standardizing formatting and removing inconsistencies

    Args:
        content: Text content to normalize

    Returns:
        Normalized text
    """
    # Replace various types of quotes with standard quotes
    content = re.sub(r'[\'`]', "'", content)  # Replace different single quotes
    content = re.sub(r'["`]', '"', content)   # Replace different double quotes

    # Remove extra whitespace
    content = re.sub(r'\s+', ' ', content)

    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Remove leading/trailing whitespace
    content = content.strip()

    return content