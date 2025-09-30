"""
Pre - configured test scenarios for common use cases.
"""

from ..builders import a_markdown_document, a_pdf_document, a_text_document
from .test_data_generator import TestDataGenerator


class TestScenarios:
    """Pre - configured test scenarios for common use cases."""

    @staticmethod
    def create_markdown_processing_scenario():
        """Create a complete markdown processing test scenario."""
        document = (
            a_markdown_document()
            .with_title("AI Research Paper")
            .with_content(TestDataGenerator.generate_markdown_sections(3))
            .build()
        )

        chunks = TestDataGenerator.generate_chunk_list(3, "AI Research Paper")

        return {"document": document, "chunks": chunks, "expected_chunk_count": 3, "file_type": "markdown"}

    @staticmethod
    def create_pdf_processing_scenario():
        """Create a complete PDF processing test scenario."""
        document = (
            a_pdf_document()
            .with_title("Technical Manual")
            .with_content(TestDataGenerator.generate_pdf_pages(2))
            .build()
        )

        chunks = TestDataGenerator.generate_chunk_list(2, "Technical Manual")

        return {"document": document, "chunks": chunks, "expected_chunk_count": 2, "file_type": "pdf"}

    @staticmethod
    def create_config_loading_scenario(config_type: str = "default"):
        """Create a configuration loading test scenario."""
        scenarios = {
            "default": TestDataGenerator.generate_config_dict(),
            "production": TestDataGenerator.generate_config_dict(
                {"model": "text - embedding - 3-large", "dimensions": 3072, "chunk_size": 1500, "level": "WARNING"}
            ),
            "development": TestDataGenerator.generate_config_dict(
                {"chunk_size": 500, "level": "DEBUG", "show_progress": True}
            ),
        }

        return scenarios.get(config_type, scenarios["default"])

    @staticmethod
    def create_chunking_scenario(strategy_type: str = "text"):
        """Create a chunking strategy test scenario."""
        if strategy_type == "markdown":
            return TestScenarios.create_markdown_processing_scenario()
        elif strategy_type == "pdf":
            return TestScenarios.create_pdf_processing_scenario()
        else:  # text
            document = (
                a_text_document().with_title("NLP Guide").with_content(TestDataGenerator.generate_long_text(30)).build()
            )

            chunks = TestDataGenerator.generate_chunk_list(5, "NLP Guide")

            return {"document": document, "chunks": chunks, "expected_chunk_count": 5, "file_type": "text"}
