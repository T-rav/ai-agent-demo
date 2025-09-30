"""
Generates test data for various scenarios.
"""

from typing import Any, Dict, List, Optional

from ..builders import a_document_chunk


class TestDataGenerator:
    """Generates test data for various scenarios."""

    @staticmethod
    def generate_markdown_sections(num_sections: int = 3) -> str:
        """Generate markdown content with multiple sections."""
        sections = []
        for i in range(num_sections):
            sections.append("# Section {i + 1}")
            sections.append("This is the content for section {i + 1}.")
            sections.append("")  # Empty line
        return "\n".join(sections)

    @staticmethod
    def generate_pdf_pages(num_pages: int = 2) -> str:
        """Generate PDF content with multiple pages."""
        pages = []
        for i in range(num_pages):
            pages.append("--- Page {i + 1} ---")
            pages.append("Content for page {i + 1} of the document.")
            pages.append("")  # Empty line
        return "\n".join(pages)

    @staticmethod
    def generate_long_text(num_sentences: int = 50) -> str:
        """Generate long text content."""
        sentences = ["This is sentence number {i + 1} in a long document." for i in range(num_sentences)]
        return " ".join(sentences)

    @staticmethod
    def generate_chunk_list(num_chunks: int = 3, document_title: str = "Test Document") -> List:
        """Generate a list of document chunks."""
        chunks = []
        for i in range(num_chunks):
            chunk = (
                a_document_chunk()
                .with_id("chunk-{i}")
                .with_chunk_index(i)
                .with_document_title(document_title)
                .with_content("Content for chunk {i}")
                .build()
            )
            chunks.append(chunk)
        return chunks

    @staticmethod
    def generate_config_dict(override_values: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Generate a configuration dictionary."""
        base_config = {
            "openai_api_key": "test - key",
            "pinecone_api_key": "test - key",
            "pinecone_environment": "test - env",
            "index_name": "test - index",
            "model": "text - embedding - 3-small",
            "dimensions": 1536,
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "min_chunk_size": 100,
            "max_chunk_size": 2000,
            "embedding_batch_size": 100,
            "upsert_batch_size": 100,
            "corpus_path": "data / corpus",
            "level": "INFO",
            "show_progress": True,
        }

        if override_values:
            base_config.update(override_values)

        return base_config
