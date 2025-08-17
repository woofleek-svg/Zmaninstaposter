# Zmaninstaposter Setup Guide

## Overview
Zmaninstaposter is an automated Instagram posting tool that:
- Stores images in Google Cloud Storage
- Generates captions using Google's Gemini AI
- Posts to Instagram using the Graph API

## Prerequisites
1. Python 3.8 or higher
2. Instagram Business or Creator account
3. Facebook Page linked to your Instagram account
4. Google Cloud Platform account
5. Google AI Studio access

## Setup Instructions

### 0. Python Virtual Environment Setup (Recommended)

1. **Create Virtual Environment**:
   ```bash
   python -m venv zmaninstaposter-env
   ```

2. **Activate Virtual Environment**:
   ```bash
   # On Linux/macOS:
   source zmaninstaposter-env/bin/activate
   
   # On Windows:
   zmaninstaposter-env\Scripts\activate
   ```

3. **Verify Activation**:
   ```bash
   which python  # Should point to virtual environment
   python --version  # Should show Python 3.8+
   ```

### 1. Instagram Graph API Setup
**REQUIRED**: Follow these steps to enable Instagram posting:

1. **Create Meta App**:
   - Go to [Meta for Developers](https://developers.facebook.com/)
   - Create a new app, select "Business" type
   - Add "Instagram API" product to your app

2. **Link Accounts**:
   - Link your Instagram Business/Creator account to a Facebook Page
   - Ensure you have admin permissions on the Facebook Page

3. **Get Access Token**:
   - Use the [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
   - Generate a short-lived token
   - Exchange it for a long-lived access token (60 days)
   - Store in `.env` file as `INSTAGRAM_ACCESS_TOKEN`

4. **Get User ID**:
   - Use Graph API Explorer to get your Instagram account ID
   - Store in `.env` file as `INSTAGRAM_USER_ID`

### 2. Google Cloud Storage Setup
**REQUIRED**: Follow these steps to store and serve images:

1. **Create Google Cloud Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Note the Project ID

2. **Enable Cloud Storage API**:
   - In your project, enable the Cloud Storage API
   - Go to APIs & Services > Library > search for "Cloud Storage"

3. **Create Storage Bucket**:
   - Go to Cloud Storage > Buckets
   - Create a new bucket with a unique name
   - Choose appropriate region and storage class

4. **Set Public Access**:
   - Configure bucket or individual images for public read access
   - Add `allUsers` with `Storage Object Viewer` role

5. **Set Up Authentication**:
   - Create a service account with Storage Admin role
   - Download the JSON key file
   - Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

### 3. Google Gemini AI Setup
**REQUIRED**: Follow these steps to generate captions:

1. **Get API Key**:
   - Go to [Google AI Studio](https://ai.google.dev/)
   - Create a new API key
   - Store in `.env` file as `GEMINI_API_KEY`

2. **Test API Access**:
   - Run the test script to verify API connectivity
   - Adjust prompts in config for better caption generation

### 4. Environment Configuration

1. **Copy Environment Template**:
   ```bash
   cp .env.example .env
   ```

2. **Fill in Your Values**:
   Edit `.env` with your actual API keys and credentials:
   ```
   INSTAGRAM_ACCESS_TOKEN=your_actual_token_here
   INSTAGRAM_USER_ID=your_actual_user_id_here
   GEMINI_API_KEY=your_actual_gemini_key_here
   GOOGLE_CLOUD_PROJECT_ID=your_actual_project_id_here
   GOOGLE_CLOUD_STORAGE_BUCKET=your_actual_bucket_name_here
   ```

3. **Update Configuration**:
   Edit `config/config.yaml` with your specific settings

### 5. Install Dependencies
```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

**Note**: If you encounter permission errors, ensure your virtual environment is activated or use `pip install --user -r requirements.txt`

### 6. Test Configuration
```bash
python src/main.py
```

## Security Notes
- **NEVER** commit `.env` file to version control
- Keep API keys secure and rotate them regularly
- Use least-privilege access for service accounts
- Monitor API usage and costs

## Troubleshooting

### Common Issues:

1. **"Configuration test failed"**:
   - Check that all required environment variables are set
   - Verify API keys are valid and not expired

2. **"Google Cloud Storage not properly configured"**:
   - Ensure service account has proper permissions
   - Check that bucket exists and is accessible

3. **"Instagram access token not configured"**:
   - Verify token is long-lived and not expired
   - Check that Instagram account is Business/Creator type

4. **"Failed to generate caption"**:
   - Verify Gemini API key is valid
   - Check API quota and usage limits

### Getting Help:
- Check the logs in `zmaninstaposter.log`
- Review the PHASE1GROUNDWORK.md for detailed API setup
- Verify all credentials and permissions

## Next Steps
- Upload your images to the Google Cloud Storage bucket
- Test the posting workflow manually
- Adjust caption generation prompts
- Set up monitoring and alerting