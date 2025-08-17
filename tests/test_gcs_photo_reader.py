import unittest
from unittest.mock import patch, MagicMock

# Import the function to be tested
from src.gcs_photo_reader import get_photos_from_gcs

class TestGCSPhotoReader(unittest.TestCase):
    """
    Test suite for the GCS photo reader function.
    """

    @patch('src.gcs_photo_reader.GoogleCloudStorageManager')
    def test_get_photos_from_gcs_success(self, mock_gcs_manager):
        """
        Test that get_photos_from_gcs returns a list of photo URLs on success.
        """
        # Arrange
        # Create a mock instance of the GoogleCloudStorageManager
        mock_instance = MagicMock()
        # Configure the mock to return a specific list of URLs
        expected_photos = [
            "http://example.com/photo1.jpg",
            "http://example.com/photo2.png"
        ]
        mock_instance.list_images.return_value = expected_photos
        # Make the patched class return our mock instance
        mock_gcs_manager.return_value = mock_instance

        # Act
        # Call the function we are testing
        actual_photos = get_photos_from_gcs()

        # Assert
        # Check that the function returned the expected list of photos
        self.assertEqual(actual_photos, expected_photos)
        # Verify that the list_images method was called once
        mock_instance.list_images.assert_called_once()

    @patch('src.gcs_photo_reader.GoogleCloudStorageManager')
    def test_get_photos_from_gcs_no_images(self, mock_gcs_manager):
        """
        Test that get_photos_from_gcs returns an empty list when no images are found.
        """
        # Arrange
        mock_instance = MagicMock()
        mock_instance.list_images.return_value = []
        mock_gcs_manager.return_value = mock_instance

        # Act
        actual_photos = get_photos_from_gcs()

        # Assert
        self.assertEqual(actual_photos, [])
        mock_instance.list_images.assert_called_once()

if __name__ == '__main__':
    unittest.main()
