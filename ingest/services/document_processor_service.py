"""
Document processing service that orchestrates content extraction and title extraction.
Implements the Single Responsibility Principle and Dependency Injection.
"""

from pathlib import Path
from typing import Optional

from ..models import FileType, ProcessedDocument, ProcessingError
from ..utils import DocumentContentExtractor, DocumentTitleExtractor, TextCleaner, TiktokenEncoder


class DocumentProcessorService:
    """
    Main document processing service.

    Orchestrates content extraction, title extraction, and text cleaning.
    Follows the Dependency Injection principle.
    """

    def __init__(
        self,
        content_extractor: Optional[DocumentContentExtractor] = None,
        title_extractor: Optional[DocumentTitleExtractor] = None,
        token_encoder: Optional[TiktokenEncoder] = None,
        text_cleaner: Optional[TextCleaner] = None,
    ) -> None:
        """
        Initialize the document processor service.

        Args:
            content_extractor: Service for extracting content from files
            title_extractor: Service for extracting titles from documents
            token_encoder: Service for encoding text to tokens
            text_cleaner: Service for cleaning text content
        """
        self._content_extractor = content_extractor or DocumentContentExtractor()
        self._title_extractor = title_extractor or DocumentTitleExtractor()
        self._token_encoder = token_encoder or TiktokenEncoder()
        self._text_cleaner = text_cleaner or TextCleaner()

    def process_file(self, file_path: Path) -> Optional[ProcessedDocument]:
        """
        Process a single file and extract its content with enhanced metadata.

        Args:
            file_path: Path to the file to process

        Returns:
            ProcessedDocument containing file metadata, content, and extracted title
            None if processing fails
        """
        try:
            # Extract raw content
            raw_content = self._content_extractor.extract_content(file_path)

            # Clean the content
            cleaned_content = self._text_cleaner.clean_text(raw_content)

            # Extract title
            title = self._title_extractor.extract_title(file_path, cleaned_content)

            # Count tokens
            token_count = self._token_encoder.count_tokens(cleaned_content)

            return ProcessedDocument(
                file_path=str(file_path),
                file_name=file_path.name,
                file_type=FileType(file_path.suffix.lower()),
                title=title,
                content=cleaned_content,
                token_count=token_count,
                char_count=len(cleaned_content),
            )

        except ProcessingError as e:
            print(f"Processing error for {file_path}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error processing {file_path}: {e}")
            return None
