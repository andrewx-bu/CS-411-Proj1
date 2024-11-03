import pytest
import requests

from unittest import mock
from meal_max.utils.random_utils import get_random

def test_get_random_success():
    """Test a successful random number retrieval."""
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.text = '0.42'  # Simulating a successful response
        mock_get.return_value.raise_for_status = mock.Mock()  # Simulating no error on status check

        result = get_random()
        
        assert result == 0.42
        mock_get.assert_called_once()


def test_get_random_invalid_response():
    """Test handling of invalid response."""
    with mock.patch('requests.get') as mock_get:
        mock_get.return_value.text = 'invalid'  # Simulating an invalid response
        mock_get.return_value.raise_for_status = mock.Mock()  # Simulating no error on status check

        with pytest.raises(ValueError, match="Invalid response from random.org: invalid"):
            get_random()


def test_get_random_timeout():
    """Test handling of request timeout."""
    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.Timeout  # Simulating a timeout

        with pytest.raises(RuntimeError, match="Request to random.org timed out."):
            get_random()


def test_get_random_request_exception():
    """Test handling of request exceptions."""
    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("Network error")  # Simulating a network error

        with pytest.raises(RuntimeError, match="Request to random.org failed: Network error"):
            get_random()