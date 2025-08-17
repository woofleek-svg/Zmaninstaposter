# Zmaninstaposter

An automated Instagram posting tool that uses Google Cloud Storage for image hosting and Google's Gemini AI for caption generation.
Updated Plan:
The project will now post older pictures from a designated Google Drive folder to your dad’s art business Instagram account on a configurable schedule.
When new pictures are uploaded to the Google Drive folder, the system will automatically post them to Instagram as well.
The system will ensure no duplicate postings and can be configured for posting frequency and other options.

## Features

- 📸 **Automated Image Selection**: Pulls images from Google Cloud Storage
- 🤖 **AI-Generated Captions**: Uses Google Gemini AI to create engaging captions
- 📱 **Instagram Integration**: Posts directly to Instagram using Graph API
- ⏰ **Scheduled Posting**: Configurable daily posting schedule
- 🔒 **Secure Configuration**: Environment-based credential management
- 📊 **Comprehensive Logging**: Detailed logging for monitoring and debugging



## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure APIs** (see [SETUP.md](SETUP.md) for detailed instructions):
   - Set up Instagram Graph API access
   - Create Google Cloud Storage bucket
   - Get Gemini AI API key

3. **Set Environment Variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials
   ```

4. **Test Configuration**:
   ```bash
   python test_config.py
   ```

5. **Run the Application**:
   ```bash
   python src/main.py
   ```

## Project Structure

```
Zmaninstaposter/
├── src/
│   └── main.py              # Main application logic
├── config/
│   └── config.yaml          # Configuration template
├── docs/
│   └── WORKFLOW.md          # Workflow documentation
├── .env.example             # Environment variables template
├── SETUP.md                 # Detailed setup guide
├── test_config.py           # Configuration test script
└── requirements.txt         # Python dependencies
```

## API Integration Status

### ✅ Google Cloud Storage
- **Purpose**: Host images with public URLs for Instagram API
- **Status**: Integrated with placeholder implementation
- **Setup Required**: Create bucket, configure permissions, set credentials

### ✅ Google Gemini AI  
- **Purpose**: Generate creative Instagram captions
- **Status**: Integrated with placeholder fallbacks
- **Setup Required**: Get API key from Google AI Studio

### ✅ Instagram Graph API
- **Purpose**: Post images and captions to Instagram
- **Status**: Integrated with error handling
- **Setup Required**: Create Meta app, get access token and user ID

## Configuration

The application uses two configuration methods:

1. **Environment Variables** (`.env` file):
   - API keys and sensitive credentials
   - See `.env.example` for required variables

2. **YAML Configuration** (`config/config.yaml`):
   - Application settings and preferences
   - Posting schedule and behavior

## Security Notes

- 🔒 **Never commit `.env` files** - they contain sensitive API keys
- 🔑 **Rotate API keys regularly** for security
- 👤 **Use least-privilege access** for service accounts
- 📊 **Monitor API usage** to avoid unexpected costs

## Development

### Testing Configuration
```bash
python test_config.py
```

### Manual Workflow Test
```bash
python -c "from src.main import workflow; workflow()"
```

### View Logs
```bash
tail -f zmaninstaposter.log
```

## Troubleshooting

Common issues and solutions:

- **Configuration errors**: Run `python test_config.py` to diagnose
- **API failures**: Check logs for detailed error messages
- **Missing images**: Verify Google Cloud Storage bucket setup
- **Caption generation fails**: Verify Gemini API key and quota

See [SETUP.md](SETUP.md) for detailed troubleshooting guide.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Roadmap

- [ ] Web dashboard for monitoring and configuration
- [ ] Multiple image selection strategies
- [ ] Advanced caption customization
- [ ] Multi-account support
- [ ] Analytics and insights
- [ ] Webhook notifications
