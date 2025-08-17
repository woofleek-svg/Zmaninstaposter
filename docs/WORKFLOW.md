# Zmaninstaposter Workflow

## Step-by-Step Process

1. **Image Selection**
    - Images stored in cloud storage.
    - Main script selects the next image to post.

2. **Caption Generation**
    - Selected image URL sent to Gemini API.
    - API returns a creative caption.

3. **Instagram Posting**
    - Create a media container via Instagram Graph API.
    - Publish the container to the Instagram account.

## Configuration

- Store all credentials and image URLs in `config/config.yaml`.

## Scheduler

- Default: Daily at 09:00 (can be adjusted in `src/main.py`).

## Extensibility

- Add more images to the config.
- Refine Gemini API prompts for better captions.
- Integrate with other cloud storage providers.
