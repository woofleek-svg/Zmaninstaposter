import requests
import os
import yaml
from schedule import every, run_pending
import time
import logging
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any

# Import Google Cloud Storage and Gemini AI libraries
# TODO: Install these packages: pip install google-cloud-storage google-generativeai
try:
    from google.cloud import storage
    from google.oauth2 import service_account
    import google.generativeai as genai
    GOOGLE_LIBS_AVAILABLE = True
except ImportError:
    print("WARNING: Google Cloud libraries not installed. Install with:")
    print("pip install google-cloud-storage google-generativeai")
    GOOGLE_LIBS_AVAILABLE = False

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('zmaninstaposter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load configuration
try:
    with open("config/config.yaml", "r") as f:
        config = yaml.safe_load(f)
        logger.info("Configuration loaded successfully")
except FileNotFoundError:
    logger.error("Configuration file not found. Please create config/config.yaml from the template.")
    config = {}

class GoogleCloudStorageManager:
    """
    Manages Google Cloud Storage operations for image hosting.
    
    TODO: Set up Google Cloud Storage:
    1. Create a Google Cloud Project
    2. Enable Cloud Storage API
    3. Create a storage bucket
    4. Set up service account credentials
    5. Configure bucket permissions for public read access
    """
    
    def __init__(self):
        self.project_id = os.getenv('GOOGLE_CLOUD_PROJECT_ID') or config.get('cloud_storage', {}).get('project_id')
        self.bucket_name = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET') or config.get('cloud_storage', {}).get('bucket_name')
        self.credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or config.get('cloud_storage', {}).get('credentials_path')
        
        if not GOOGLE_LIBS_AVAILABLE:
            logger.warning("Google Cloud Storage libraries not available. Using placeholder implementation.")
            self.client = None
            self.bucket = None
            return
            
        try:
            # Initialize Google Cloud Storage client
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
                self.client = storage.Client(project=self.project_id, credentials=credentials)
            else:
                # Use default application credentials
                self.client = storage.Client(project=self.project_id)
            
            self.bucket = self.client.bucket(self.bucket_name) if self.bucket_name else None
            logger.info("Google Cloud Storage client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud Storage client: {e}")
            self.client = None
            self.bucket = None
    
    def list_images(self) -> List[str]:
        """
        List all image URLs from the Google Cloud Storage bucket.
        
        Returns:
            List of public image URLs
        """
        if not self.bucket:
            logger.warning("Using placeholder images from config")
            return config.get('images', [
                "https://via.placeholder.com/600x600/FF6B6B/FFFFFF?text=Sample+Image+1",
                "https://via.placeholder.com/600x600/4ECDC4/FFFFFF?text=Sample+Image+2"
            ])
        
        try:
            blobs = self.bucket.list_blobs()
            image_urls = []
            
            for blob in blobs:
                # Only include image files
                if blob.name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    # Use the recommended public_url attribute
                    image_urls.append(blob.public_url)
            
            logger.info(f"Found {len(image_urls)} images in cloud storage")
            return image_urls
            
        except Exception as e:
            logger.error(f"Failed to list images from cloud storage: {e}")
            return config.get('images', [])
    
    def upload_image(self, local_path: str, remote_name: str) -> Optional[str]:
        """
        Upload an image to Google Cloud Storage.
        
        Args:
            local_path: Path to local image file
            remote_name: Name for the file in cloud storage
            
        Returns:
            Public URL of uploaded image, or None if failed
        """
        if not self.bucket:
            logger.error("Google Cloud Storage not properly configured")
            return None
        
        try:
            blob = self.bucket.blob(remote_name)
            blob.upload_from_filename(local_path)
            
            # Make the blob publicly readable
            blob.make_public()
            
            public_url = blob.public_url
            logger.info(f"Successfully uploaded {local_path} to {public_url}")
            return public_url
            
        except Exception as e:
            logger.error(f"Failed to upload image {local_path}: {e}")
            return None


class GeminiCaptionGenerator:
    """
    Generates Instagram captions using Google's Gemini AI.
    
    TODO: Set up Gemini API:
    1. Go to Google AI Studio (https://ai.google.dev/)
    2. Create an API key
    3. Store the API key securely in .env file
    4. Test the API with sample prompts
    """
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY') or config.get('gemini', {}).get('api_key')
        self.model_name = config.get('gemini', {}).get('model', 'gemini-1.5-flash')
        self.max_tokens = config.get('gemini', {}).get('max_tokens', 150)
        
        if not GOOGLE_LIBS_AVAILABLE:
            logger.warning("Gemini AI libraries not available. Using placeholder implementation.")
            self.model = None
            return
            
        if not self.api_key or self.api_key == "YOUR_GEMINI_API_KEY_HERE":
            logger.warning("Gemini API key not configured. Using placeholder captions.")
            self.model = None
            return
        
        try:
            # Configure Gemini AI
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info("Gemini AI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI client: {e}")
            self.model = None
    
    def generate_caption(self, image_url: str, custom_prompt: str = None) -> str:
        """
        Generate an Instagram caption for the given image.
        
        Args:
            image_url: URL of the image to analyze
            custom_prompt: Optional custom prompt for caption generation
            
        Returns:
            Generated caption text
        """
        if not self.model:
            # Fallback to placeholder caption
            placeholder_captions = [
                "🌟 Another beautiful moment captured! ✨ #life #photography #moments",
                "📸 Living life one photo at a time! 💫 #blessed #grateful #joy",
                "🎨 Beauty is everywhere when you know where to look! 🌈 #art #inspiration #beautiful"
            ]
            import random
            caption = random.choice(placeholder_captions)
            logger.info(f"Using placeholder caption: {caption}")
            return caption
        
        try:
            # Default prompt for Instagram captions
            if not custom_prompt:
                prompt = f"""
                Generate a creative and engaging Instagram caption for this image: {image_url}
                
                Requirements:
                - Keep it under 150 characters
                - Make it engaging and authentic
                - Include 2-3 relevant hashtags
                - Match the mood and content of the image
                - Be creative but not overly promotional
                
                Return only the caption text, no additional formatting.
                """
            else:
                prompt = custom_prompt
            
            # For now, use text-only generation
            # TODO: Implement multimodal image analysis when image input is supported
            response = self.model.generate_content(prompt)
            caption = response.text.strip()
            
            logger.info(f"Generated caption: {caption}")
            return caption
            
        except Exception as e:
            logger.error(f"Failed to generate caption with Gemini AI: {e}")
            return "✨ Sharing a beautiful moment! 📸 #photography #life #moments"


# Initialize cloud storage and caption generator
storage_manager = GoogleCloudStorageManager()
caption_generator = GeminiCaptionGenerator()


def select_image() -> str:
    """
    Select the next image to post from cloud storage.
    
    TODO: Implement intelligent image selection logic:
    - Track previously posted images
    - Implement rotation strategies
    - Consider posting schedules and themes
    
    Returns:
        URL of selected image
    """
    try:
        available_images = storage_manager.list_images()
        
        if not available_images:
            logger.error("No images available for posting")
            return ""
        
        # Simple selection: return first image
        # TODO: Implement more sophisticated selection logic
        selected_image = available_images[0]
        logger.info(f"Selected image: {selected_image}")
        return selected_image
        
    except Exception as e:
        logger.error(f"Error selecting image: {e}")
        return ""


def generate_caption(image_url: str) -> str:
    """
    Generate a caption for the given image URL.
    
    Args:
        image_url: URL of the image to generate caption for
        
    Returns:
        Generated caption text
    """
    try:
        caption = caption_generator.generate_caption(image_url)
        logger.info(f"Generated caption for {image_url}: {caption}")
        return caption
        
    except Exception as e:
        logger.error(f"Error generating caption: {e}")
        return "✨ Beautiful moment captured! 📸 #life #photography"

def post_to_instagram(image_url: str, caption: str) -> Dict[str, Any]:
    """
    Post an image with caption to Instagram using the Graph API.
    
    TODO: Set up Instagram Graph API:
    1. Create a Meta App in the Meta Developer Console
    2. Add Instagram API product to your app
    3. Link Instagram Business/Creator account to a Facebook Page
    4. Generate long-lived access token
    5. Get Instagram User ID
    
    Args:
        image_url: Public URL of the image to post
        caption: Caption text for the post
        
    Returns:
        API response dictionary
    """
    # Get credentials from environment or config
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN') or config.get('instagram', {}).get('access_token')
    user_id = os.getenv('INSTAGRAM_USER_ID') or config.get('instagram', {}).get('user_id')
    api_version = config.get('instagram', {}).get('api_version', 'v19.0')
    
    if not access_token or access_token == "YOUR_INSTAGRAM_ACCESS_TOKEN_HERE":
        logger.error("Instagram access token not configured")
        return {"error": "Instagram access token not configured"}
    
    if not user_id or user_id == "YOUR_INSTAGRAM_USER_ID_HERE":
        logger.error("Instagram user ID not configured")
        return {"error": "Instagram user ID not configured"}
    
    try:
        # Step 1: Create media container
        logger.info(f"Creating media container for image: {image_url}")
        media_resp = requests.post(
            f"https://graph.facebook.com/{api_version}/{user_id}/media",
            data={
                "image_url": image_url,
                "caption": caption,
                "access_token": access_token
            }
        )
        
        if media_resp.status_code != 200:
            logger.error(f"Failed to create media container: {media_resp.text}")
            return {"error": f"Media container creation failed: {media_resp.text}"}
        
        media_data = media_resp.json()
        container_id = media_data.get("id")
        
        if not container_id:
            logger.error(f"No container ID in response: {media_data}")
            return {"error": "No container ID received"}
        
        logger.info(f"Media container created with ID: {container_id}")
        
        # Step 2: Publish the post
        logger.info(f"Publishing media container: {container_id}")
        publish_resp = requests.post(
            f"https://graph.facebook.com/{api_version}/{user_id}/media_publish",
            data={
                "creation_id": container_id,
                "access_token": access_token
            }
        )
        
        if publish_resp.status_code != 200:
            logger.error(f"Failed to publish post: {publish_resp.text}")
            return {"error": f"Post publishing failed: {publish_resp.text}"}
        
        publish_data = publish_resp.json()
        logger.info(f"Successfully published post: {publish_data}")
        
        return {
            "success": True,
            "media_id": publish_data.get("id"),
            "container_id": container_id,
            "image_url": image_url,
            "caption": caption
        }
        
    except requests.RequestException as e:
        logger.error(f"Network error posting to Instagram: {e}")
        return {"error": f"Network error: {str(e)}"}
    except Exception as e:
        logger.error(f"Unexpected error posting to Instagram: {e}")
        return {"error": f"Unexpected error: {str(e)}"}


def workflow() -> None:
    """
    Main workflow function that orchestrates the entire posting process.
    
    This function:
    1. Selects an image from cloud storage
    2. Generates a caption using Gemini AI
    3. Posts to Instagram using Graph API
    4. Handles errors and logging
    """
    logger.info("Starting Instagram posting workflow")
    
    try:
        # Step 1: Select image
        image_url = select_image()
        if not image_url:
            logger.error("No image selected, aborting workflow")
            return
        
        # Step 2: Generate caption
        caption = generate_caption(image_url)
        if not caption:
            logger.error("Failed to generate caption, aborting workflow")
            return
        
        # Step 3: Post to Instagram
        result = post_to_instagram(image_url, caption)
        
        if result.get("success"):
            logger.info(f"Successfully completed workflow - Posted: {result}")
        else:
            logger.error(f"Workflow failed - Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        logger.error(f"Unexpected error in workflow: {e}")


def test_configuration() -> bool:
    """
    Test the configuration and API connections.
    
    Returns:
        True if configuration is valid, False otherwise
    """
    logger.info("Testing configuration...")
    
    issues = []
    
    # Check Google Cloud Storage configuration
    if not storage_manager.bucket:
        issues.append("Google Cloud Storage not properly configured")
    
    # Check Gemini AI configuration
    if not caption_generator.model:
        issues.append("Gemini AI not properly configured")
    
    # Check Instagram API configuration
    access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN') or config.get('instagram', {}).get('access_token')
    user_id = os.getenv('INSTAGRAM_USER_ID') or config.get('instagram', {}).get('user_id')
    
    if not access_token or access_token == "YOUR_INSTAGRAM_ACCESS_TOKEN_HERE":
        issues.append("Instagram access token not configured")
    
    if not user_id or user_id == "YOUR_INSTAGRAM_USER_ID_HERE":
        issues.append("Instagram user ID not configured")
    
    if issues:
        logger.warning("Configuration issues found:")
        for issue in issues:
            logger.warning(f"  - {issue}")
        logger.warning("Please check .env file and config/config.yaml")
        return False
    else:
        logger.info("Configuration looks good!")
        return True

# Scheduling configuration
schedule_time = config.get('schedule', {}).get('time', '09:00')
every().day.at(schedule_time).do(workflow)

if __name__ == "__main__":
    logger.info("Starting Zmaninstaposter application")
    
    # Test configuration on startup
    if not test_configuration():
        logger.error("Configuration test failed. Please fix configuration issues before running.")
        logger.info("See .env.example and config/config.yaml for required settings")
        exit(1)
    
    logger.info(f"Scheduling daily posts at {schedule_time}")
    logger.info("Application is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
        exit(1)

def download_image_from_bucket(blob_name: str, local_path: str) -> bool:
    """
    Download an image from the configured Google Cloud Storage bucket.

    Args:
        blob_name: Name of the blob (file) in the bucket
        local_path: Local path to save the downloaded image

    Returns:
        True if download succeeds, False otherwise
    """
    if not storage_manager.bucket:
        logger.error("Google Cloud Storage not properly configured")
        return False

    try:
        blob = storage_manager.bucket.blob(blob_name)
        blob.download_to_filename(local_path)
        logger.info(f"Downloaded {blob_name} to {local_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to download {blob_name}: {e}")
        return False

# Example usage (uncomment to use):
# blobs = storage_manager.bucket.list_blobs()
# for blob in blobs:
#     print(blob.name)
#     # download_image_from_bucket(blob.name, f"./downloads/{blob.name}")