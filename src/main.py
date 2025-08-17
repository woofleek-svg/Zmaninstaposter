import requests
import os
import yaml
from schedule import every, run_pending
import time

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

def select_image():
    # Placeholder: Select image URL from cloud storage
    return config["images"][0]  # Example: List of image URLs in config

def generate_caption(image_url):
    # Placeholder: Gemini API request
    prompt = f"Generate a creative and engaging Instagram caption for this image: {image_url}"
    # Example Gemini API call (replace with actual endpoint and auth)
    response = requests.post(
        config["gemini_api_url"],
        json={"prompt": prompt, "image_url": image_url},
        headers={"Authorization": f"Bearer {config['gemini_api_key']}"}
    )
    return response.json().get("caption", "")

def post_to_instagram(image_url, caption):
    # Step 1: Create media container
    media_resp = requests.post(
        f"https://graph.facebook.com/v19.0/{config['instagram_user_id']}/media",
        data={
            "image_url": image_url,
            "caption": caption,
            "access_token": config["instagram_access_token"]
        }
    )
    container_id = media_resp.json().get("id")

    # Step 2: Publish the post
    publish_resp = requests.post(
        f"https://graph.facebook.com/v19.0/{config['instagram_user_id']}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": config["instagram_access_token"]
        }
    )
    return publish_resp.json()

def workflow():
    image_url = select_image()
    caption = generate_caption(image_url)
    result = post_to_instagram(image_url, caption)
    print(f"Posted: {result}")

# Scheduling (example: once daily)
every().day.at("09:00").do(workflow)

if __name__ == "__main__":
    while True:
        run_pending()
        time.sleep(60)