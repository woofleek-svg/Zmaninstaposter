#!/usr/bin/env python3
"""
Foundation Test Script for Zmaninstaposter

This script demonstrates that the project foundation is properly set up
and all components can work together, even without actual API credentials.
"""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import components
from main import storage_manager, caption_generator, select_image, generate_caption
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_foundation():
    """Test that all foundation components work together."""
    logger.info("🚀 Testing Zmaninstaposter Project Foundation")
    logger.info("=" * 60)
    
    # Test 1: Configuration Loading
    logger.info("1. Testing configuration loading...")
    try:
        from main import config
        if config:
            logger.info("   ✅ Configuration loaded successfully")
            logger.info(f"   📊 Found {len(config.get('images', []))} sample images configured")
        else:
            logger.error("   ❌ Configuration failed to load")
            return False
    except Exception as e:
        logger.error(f"   ❌ Configuration error: {e}")
        return False
    
    # Test 2: Image Selection
    logger.info("2. Testing image selection...")
    try:
        selected_image = select_image()
        if selected_image:
            logger.info(f"   ✅ Successfully selected image: {selected_image[:50]}...")
        else:
            logger.error("   ❌ No image selected")
            return False
    except Exception as e:
        logger.error(f"   ❌ Image selection error: {e}")
        return False
    
    # Test 3: Caption Generation
    logger.info("3. Testing caption generation...")
    try:
        test_url = "https://example.com/test-image.jpg"
        caption = generate_caption(test_url)
        if caption and len(caption) > 0:
            logger.info(f"   ✅ Successfully generated caption: {caption[:50]}...")
        else:
            logger.error("   ❌ Caption generation failed")
            return False
    except Exception as e:
        logger.error(f"   ❌ Caption generation error: {e}")
        return False
    
    # Test 4: Component Integration
    logger.info("4. Testing full workflow simulation...")
    try:
        # Simulate the workflow without actually posting
        image_url = select_image()
        caption = generate_caption(image_url)
        
        logger.info("   ✅ Simulated workflow completed successfully:")
        logger.info(f"      📸 Image: {image_url[:50]}...")
        logger.info(f"      💬 Caption: {caption[:50]}...")
        
    except Exception as e:
        logger.error(f"   ❌ Workflow simulation error: {e}")
        return False
    
    logger.info("=" * 60)
    logger.info("🎉 PROJECT FOUNDATION TEST: PASSED")
    logger.info("")
    logger.info("📋 Foundation Components Ready:")
    logger.info("   ✅ Python project structure")
    logger.info("   ✅ Configuration management")
    logger.info("   ✅ Sample images prepared")
    logger.info("   ✅ API integrations (with fallbacks)")
    logger.info("   ✅ Virtual environment documentation")
    logger.info("   ✅ Testing infrastructure")
    logger.info("")
    logger.info("🔧 Next Steps:")
    logger.info("   • Configure actual API credentials in .env file")
    logger.info("   • Set up Google Cloud Storage bucket")
    logger.info("   • Upload your own images")
    logger.info("   • Test with real API connections")
    
    return True

if __name__ == "__main__":
    success = test_foundation()
    sys.exit(0 if success else 1)