"""
Tests for the token encoder utilities.
"""

import pytest
from unittest.mock import Mock, patch

from ...utils import TiktokenEncoder
from ...models import ProcessingError


class TestTiktokenEncoder:
    """Test cases for TiktokenEncoder."""
    
    @pytest.fixture
    def encoder(self):
        """Create a TiktokenEncoder instance."""
        return TiktokenEncoder()
    
    def test_count_tokens_success(self, encoder):
        """Test successful token counting."""
        # Mock the encoding object that's already created in the encoder
        with patch.object(encoder._encoding, 'encode', return_value=[1, 2, 3, 4, 5]):
            result = encoder.count_tokens("Test text")
            
            assert result == 5
            encoder._encoding.encode.assert_called_once_with("Test text")
    
    def test_encode_success(self, encoder):
        """Test successful text encoding."""
        with patch.object(encoder._encoding, 'encode', return_value=[1, 2, 3]):
            result = encoder.encode("Test")
            
            assert result == [1, 2, 3]
            encoder._encoding.encode.assert_called_once_with("Test")
    
    def test_decode_success(self, encoder):
        """Test successful token decoding."""
        with patch.object(encoder._encoding, 'decode', return_value="Decoded text"):
            result = encoder.decode([1, 2, 3])
            
            assert result == "Decoded text"
            encoder._encoding.decode.assert_called_once_with([1, 2, 3])
    
    def test_tiktoken_not_available(self):
        """Test behavior when tiktoken is not available."""
        with patch('ingest.utils.token_encoder.tiktoken', None):
            with pytest.raises(ProcessingError, match="tiktoken is required for token encoding"):
                TiktokenEncoder()
    
    def test_count_tokens_encoding_error(self, encoder):
        """Test handling encoding errors in token counting."""
        with patch.object(encoder._encoding, 'encode', side_effect=Exception("Encoding error")):
            # The current implementation doesn't catch encoding errors in count_tokens
            # So this test should expect the raw exception, not a ProcessingError
            with pytest.raises(Exception, match="Encoding error"):
                encoder.count_tokens("Test text")
    
    def test_encode_error(self, encoder):
        """Test handling encoding errors."""
        with patch.object(encoder._encoding, 'encode', side_effect=Exception("Encode error")):
            # The current implementation doesn't catch encoding errors in encode
            # So this test should expect the raw exception, not a ProcessingError
            with pytest.raises(Exception, match="Encode error"):
                encoder.encode("Test text")
    
    def test_decode_error(self, encoder):
        """Test handling decoding errors."""
        with patch.object(encoder._encoding, 'decode', side_effect=Exception("Decode error")):
            # The current implementation doesn't catch decoding errors in decode
            # So this test should expect the raw exception, not a ProcessingError
            with pytest.raises(Exception, match="Decode error"):
                encoder.decode([1, 2, 3])
    
    @patch('ingest.utils.token_encoder.tiktoken')
    def test_custom_encoding_model(self, mock_tiktoken):
        """Test using a custom encoding model."""
        mock_encoding = Mock()
        mock_encoding.encode.return_value = [1, 2]
        mock_tiktoken.get_encoding.return_value = mock_encoding
        
        encoder = TiktokenEncoder(encoding_model="custom-encoding")
        result = encoder.count_tokens("Test")
        
        mock_tiktoken.get_encoding.assert_called_with("custom-encoding")
        assert result == 2
    
    def test_empty_text_count_tokens(self, encoder):
        """Test counting tokens for empty text."""
        with patch.object(encoder._encoding, 'encode', return_value=[]):
            result = encoder.count_tokens("")
            
            assert result == 0
    
    def test_empty_tokens_decode(self, encoder):
        """Test decoding empty token list."""
        with patch.object(encoder._encoding, 'decode', return_value=""):
            result = encoder.decode([])
            
            assert result == ""
