import re
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import markdown
from markdownify import markdownify
import frontmatter

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """
    Service for processing MDX files, cleaning text, and chunking content
    """

    def __init__(self):
        self.chunk_size = 1000  # characters
        self.chunk_overlap = 200  # characters

    def parse_mdx_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse an MDX file and extract content and metadata

        Args:
            file_path: Path to the MDX file

        Returns:
            Dictionary containing content and metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)

            content = post.content
            metadata = post.metadata

            # Extract title from metadata if not present
            if 'title' not in metadata:
                # Try to extract from first heading
                lines = content.split('\n')
                for line in lines:
                    if line.strip().startswith('# '):
                        metadata['title'] = line.strip()[2:]
                        break

            # Extract section information
            section = self._extract_section_info(content, metadata)
            metadata['section'] = section

            return {
                'content': content,
                'metadata': metadata,
                'file_path': file_path
            }
        except Exception as e:
            logger.error(f"Error parsing MDX file {file_path}: {str(e)}")
            raise

    def _extract_section_info(self, content: str, metadata: Dict[str, Any]) -> str:
        """
        Extract section information from content or metadata

        Args:
            content: The content string
            metadata: The metadata dictionary

        Returns:
            Section identifier
        """
        # Try to get section from metadata first
        if 'sidebar_label' in metadata:
            return metadata['sidebar_label']
        elif 'title' in metadata:
            return metadata['title']
        else:
            # Extract from content if no metadata available
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('# '):
                    return line.strip()[2:]

        return "Unknown Section"

    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text content

        Args:
            text: Raw text content

        Returns:
            Cleaned text
        """
        # Remove MDX-specific syntax and formatting
        cleaned = text

        # Remove import/export statements
        cleaned = re.sub(r'^\s*import\s+.*$\n?', '', cleaned, flags=re.MULTILINE)
        cleaned = re.sub(r'^\s*export\s+.*$\n?', '', cleaned, flags=re.MULTILINE)

        # Remove JSX components and their content
        cleaned = re.sub(r'<[^>]*>.*?</[^>]*>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<[^>]*/>', '', cleaned)

        # Remove code blocks (```...```)
        cleaned = re.sub(r'```.*?```', '', cleaned, flags=re.DOTALL)

        # Remove inline code (backticks)
        cleaned = re.sub(r'`[^`]*`', '', cleaned)

        # Remove HTML tags
        cleaned = re.sub(r'<[^>]*>', '', cleaned)

        # Convert markdown to plain text while preserving structure
        try:
            # Convert markdown to HTML first
            html_content = markdown.markdown(cleaned)
            # Then convert HTML to plain text
            cleaned = markdownify(html_content)
        except Exception as e:
            logger.warning(f"Error converting markdown to plain text: {str(e)}")
            # Fallback: just clean basic markdown
            cleaned = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned)  # Bold
            cleaned = re.sub(r'\*(.*?)\*', r'\1', cleaned)      # Italic
            cleaned = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', cleaned)  # Links
            cleaned = re.sub(r'!\[(.*?)\]\(.*?\)', r'\1', cleaned)  # Images
            cleaned = re.sub(r'^#+\s+', '', cleaned, flags=re.MULTILINE)  # Headers

        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        cleaned = cleaned.strip()

        # Remove excessive newlines and normalize
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)

        return cleaned

    def chunk_text(self, text: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk text into semantic sections

        Args:
            text: Cleaned text content
            metadata: Document metadata

        Returns:
            List of document chunks with metadata
        """
        chunks = []

        # Split by paragraphs and major sections
        paragraphs = self._split_by_paragraphs(text)

        # Process each paragraph and create chunks
        for i, paragraph in enumerate(paragraphs):
            if len(paragraph.strip()) > 50:  # Only create chunks for substantial content
                chunk = {
                    'content': paragraph.strip(),
                    'metadata': {
                        **metadata,
                        'chunk_index': i,
                        'total_chunks': len(paragraphs)
                    }
                }
                chunks.append(chunk)

        # If paragraphs are too large, further split them
        refined_chunks = []
        for chunk in chunks:
            if len(chunk['content']) > self.chunk_size:
                sub_chunks = self._split_large_chunk(chunk['content'], chunk['metadata'])
                refined_chunks.extend(sub_chunks)
            else:
                refined_chunks.append(chunk)

        return refined_chunks

    def _split_by_paragraphs(self, text: str) -> List[str]:
        """
        Split text by paragraphs and semantic boundaries

        Args:
            text: Input text

        Returns:
            List of paragraphs
        """
        # Split by double newlines (paragraph boundaries)
        paragraphs = text.split('\n\n')

        # Further refine by section headers
        refined_paragraphs = []
        for paragraph in paragraphs:
            # Split by section headers (single newlines followed by content that looks like headers)
            sub_parts = re.split(r'\n(?=\S.*\n[-=]+\s*\n)', paragraph)
            for part in sub_parts:
                if part.strip():
                    refined_paragraphs.append(part.strip())

        # Remove empty paragraphs and clean up
        refined_paragraphs = [p for p in refined_paragraphs if p.strip()]

        return refined_paragraphs

    def _split_large_chunk(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split a large chunk into smaller semantic pieces

        Args:
            content: Large content string
            metadata: Original metadata

        Returns:
            List of smaller chunks
        """
        chunks = []

        # If content is still too large, split by sentences while respecting semantic boundaries
        if len(content) > self.chunk_size:
            sentences = re.split(r'[.!?]+\s+', content)
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk + " " + sentence) <= self.chunk_size:
                    if current_chunk:
                        current_chunk += " " + sentence
                    else:
                        current_chunk = sentence
                else:
                    if current_chunk:
                        chunks.append({
                            'content': current_chunk.strip(),
                            'metadata': {**metadata}
                        })
                    current_chunk = sentence

            # Add the last chunk if it exists
            if current_chunk.strip():
                chunks.append({
                    'content': current_chunk.strip(),
                    'metadata': {**metadata}
                })
        else:
            chunks.append({
                'content': content,
                'metadata': {**metadata}
            })

        return chunks

    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Process all MDX files in a directory

        Args:
            directory_path: Path to directory containing MDX files

        Returns:
            List of processed document chunks
        """
        all_chunks = []
        mdx_files = Path(directory_path).rglob("*.mdx")

        for mdx_file in mdx_files:
            try:
                logger.info(f"Processing file: {mdx_file}")

                # Parse the MDX file
                doc_data = self.parse_mdx_file(str(mdx_file))

                # Clean the content
                cleaned_content = self.clean_text(doc_data['content'])

                # Create metadata for chunks
                chunk_metadata = {
                    **doc_data['metadata'],
                    'source_file': str(mdx_file),
                    'original_file_path': doc_data['file_path']
                }

                # Chunk the content
                chunks = self.chunk_text(cleaned_content, chunk_metadata)

                # Add document-level metadata to each chunk
                for chunk in chunks:
                    chunk['metadata']['document_id'] = str(mdx_file)
                    chunk['metadata']['file_name'] = mdx_file.name
                    chunk['metadata']['relative_path'] = str(mdx_file.relative_to(directory_path))

                all_chunks.extend(chunks)

            except Exception as e:
                logger.error(f"Error processing file {mdx_file}: {str(e)}")
                continue

        return all_chunks


# Example usage
if __name__ == "__main__":
    processor = DocumentProcessor()

    # Example of how to use the processor
    # chunks = processor.process_directory("path/to/mdx/files")
    # for chunk in chunks:
    #     print(f"Chunk: {chunk['content'][:100]}...")
    #     print(f"Metadata: {chunk['metadata']}")
    #     print("---")