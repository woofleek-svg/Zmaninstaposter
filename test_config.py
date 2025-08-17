#!/usr/bin/env python3
"""
Test script for Zmaninstaposter configuration and API connectivity.

This script helps verify that all APIs are properly configured
without actually posting to Instagram.
"""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Now import from main module
from main import storage_manager, caption_generator, test_configuration
import logging

# Set up logging for testing
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_google_cloud_storage():
    """Test Google Cloud Storage connectivity and image listing."""
    logger.info("Testing Google Cloud Storage...")
    
    try:
        images = storage_manager.list_images()
        logger.info(f"Found {len(images)} images in storage")
        
        if images:
            logger.info("Sample images:")
            for i, img in enumerate(images[:3]):  # Show first 3
                logger.info(f"  {i+1}. {img}")
        else:
            logger.warning("No images found in storage")
            
        return len(images) > 0
        
    except Exception as e:
        logger.error(f"Google Cloud Storage test failed: {e}")
        return False

def test_gemini_ai():
    """Test Gemini AI caption generation."""
    logger.info("Testing Gemini AI caption generation...")
    
    try:
        test_image_url = "https://via.placeholder.com/600x600/FF6B6B/FFFFFF?text=Test+Image"
        caption = caption_generator.generate_caption(test_image_url)
        
        logger.info(f"Generated test caption: {caption}")
        return len(caption) > 0
        
    except Exception as e:
        logger.error(f"Gemini AI test failed: {e}")
        return False

def main():
    """Run all configuration tests."""
    logger.info("Starting Zmaninstaposter configuration tests...")
    logger.info("=" * 50)
    
    # Test overall configuration
    config_ok = test_configuration()
    
    # Test individual components
    storage_ok = test_google_cloud_storage()
    ai_ok = test_gemini_ai()
    
    logger.info("=" * 50)
    logger.info("Test Results Summary:")
    logger.info(f"  Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    logger.info(f"  Cloud Storage: {'✅ PASS' if storage_ok else '❌ FAIL'}")
    logger.info(f"  Gemini AI:     {'✅ PASS' if ai_ok else '❌ FAIL'}")
    
    if config_ok and storage_ok and ai_ok:
        logger.info("\n🎉 All tests passed! Your configuration is ready.")
        logger.info("You can now run the main application with: python src/main.py")
    else:
        logger.error("\n❌ Some tests failed. Please check your configuration.")
        logger.error("See SETUP.md for detailed setup instructions.")
        sys.exit(1)

if __name__ == "__main__":
    main()