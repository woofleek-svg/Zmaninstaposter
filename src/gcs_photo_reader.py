from src.main import GoogleCloudStorageManager
from typing import List

def get_photos_from_gcs() -> List[str]:
    """
    Retrieves a list of photo URLs from Google Cloud Storage.

    This function initializes the GoogleCloudStorageManager and uses it to
    fetch the list of public URLs for all images in the configured GCS bucket.

    Returns:
        A list of strings, where each string is a public URL to a photo.
    """
    storage_manager = GoogleCloudStorageManager()
    return storage_manager.list_images()

if __name__ == '__main__':
    # Example of how to use the function
    # This will only work if you have your environment configured
    print("Attempting to retrieve photos from Google Cloud Storage...")
    photos = get_photos_from_gcs()
    if photos:
        print(f"Found {len(photos)} photos:")
        for photo_url in photos:
            print(f"- {photo_url}")
    else:
        print("No photos found or GCS not configured correctly.")
