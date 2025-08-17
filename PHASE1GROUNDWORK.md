
Zmaninstaposter: Phase 1 - Groundwork and Research
This document outlines the foundational research and planning for the Zmaninstaposter project. The goal of this phase is to establish all necessary API connections and choose a cloud hosting solution before starting to write the core application logic.
Instagram Graph API Research
The Instagram Graph API is used for publishing content. It requires specific account types and a multi-step authentication process to work.
Key Requirements:
 * Account Setup: Must be an Instagram Business or Creator account linked to a Facebook Page.
 * Authentication: Requires a long-lived access token for publishing. This token is valid for 60 days and can be refreshed to prevent your app from losing access.
 * Content Limits: The API supports JPEG images and MP4 videos. It has a limit of 25 API-published posts per 24 hours.
Micro-Tasks:
 * [ ] Create a Meta App: Go to the Meta App Dashboard and create a new app. Select the "Business" type.
 * [ ] Add Instagram Product: Add the "Instagram API" product to your newly created Meta App.
 * [ ] Link Accounts: Link your Instagram Professional account to a Facebook Page and ensure your user has the correct permissions on that page.
 * [ ] Obtain Access Token: Use the Graph API Explorer to generate a short-lived token and then exchange it for a long-lived access token. This token is secret and should be stored securely.
 * [ ] Configure Redirect URL: Set up a valid OAuth redirect URI in the "Instagram Basic Display" settings of your Meta App.
Gemini API Integration Research
The Gemini API will be used to generate creative and relevant captions for the images. The API supports a multimodal approach, allowing it to "see" the image and generate a text response.
Key Requirements:
 * API Key: An API key from Google is required for authentication. This key will be used in your application's requests.
 * Prompting: The effectiveness of the caption will depend on a well-crafted prompt that instructs the Gemini model on what kind of text to generate (e.g., "Write a funny caption for this picture," or "Provide a short, engaging caption for this photo of a dog").
Micro-Tasks:
 * [ ] Get an API Key: Go to Google AI Studio to generate a new API key.
 * [ ] Secure the Key: Store the Gemini API key in a .env file and add .env to your .gitignore file to prevent it from being committed to the repository.
 * [ ] Draft a Test Prompt: Write a few example prompts that you can use to test the Gemini API's ability to generate captions. For example, a prompt for a picture of Hunny might be, "Generate a funny and loving Instagram caption for a picture of a fawn-colored French bulldog named Hunny."
Cloud Storage Solution Research
Choosing a cloud storage solution is crucial for hosting your images so they can be accessed by the Instagram API. Google Cloud Storage is a great fit, especially since you'll be using other Google Cloud services like the Gemini API.
Key Requirements:
 * Public Access: Images must be publicly accessible via a URL for the Instagram API to retrieve and publish them.
 * Cost-Effectiveness: The solution should have a free tier that is sufficient for this project's needs.
 * Integration: It should be easy to integrate with your Python script and Google Cloud Function.
Micro-Tasks:
 * [ ] Create a Google Cloud Project: If you don't have one already, create a new project in the Google Cloud Console.
 * [ ] Create a Storage Bucket: In your project, create a new Google Cloud Storage bucket. Give it a unique name.
 * [ ] Set Permissions: Configure the bucket or individual images to be publicly readable. You can do this by setting a specific "allUsers" role on the bucket.
 * [ ] Upload a Test Image: Upload a sample image to your new bucket and confirm that you can access it via a public URL.
