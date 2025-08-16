# API Setup Guide

## Cerebras Cloud API Setup

This project uses the Cerebras Cloud API for AI-powered text processing. Follow these steps to set up your API access.

### 1. Create Cerebras Cloud Account

1. Visit [https://cloud.cerebras.ai](https://cloud.cerebras.ai)
2. Sign up for a new account or log in if you already have one
3. Complete the account verification process

### 2. Get Your API Key

1. Navigate to your dashboard
2. Go to API Keys section
3. Create a new API key
4. Copy the API key (it will look like `csk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)

### 3. Set Up Environment Variable

#### Option 1: Command Line (Temporary)
```bash
export CEREBRAS_API_KEY="your_api_key_here"
```

#### Option 2: .env File (Recommended)
Create a `.env` file in the project root:
```bash
echo "CEREBRAS_API_KEY=your_api_key_here" > .env
```

#### Option 3: Configuration File
Copy `config.example.py` to `config.py` and update:
```python
CEREBRAS_API_KEY = "your_api_key_here"
```

### 4. Verify Setup

Run the test script to verify your API setup:
```bash
python tests/test_api_connection.py
```

## API Configuration Options

### Model Selection
The default model is `llama-4-scout-17b-16e-instruct`. You can change this in the configuration:

```python
MODEL_NAME = "llama-4-scout-17b-16e-instruct"  # Default
# MODEL_NAME = "other-model-name"  # Alternative
```

### Rate Limiting
To avoid hitting API limits, the tool includes rate limiting:

```python
RATE_LIMIT_DELAY = 0.3  # Seconds between requests
```

### API Parameters
You can adjust these parameters for different results:

```python
MAX_TOKENS = 2000      # Maximum response length
TEMPERATURE = 0.1      # Response consistency (0.0-1.0)
MAX_RETRIES = 3        # Retry failed requests
TIMEOUT = 30           # Request timeout in seconds
```

## Troubleshooting

### Common Issues

1. **Invalid API Key**
   ```
   Error: API call failed: Invalid API key
   ```
   - Verify your API key is correct
   - Check if the key has expired
   - Ensure proper environment variable setup

2. **Rate Limiting**
   ```
   Error: Rate limit exceeded
   ```
   - Increase `RATE_LIMIT_DELAY`
   - Check your account's rate limits
   - Consider upgrading your plan

3. **Model Not Available**
   ```
   Error: Model not found
   ```
   - Verify the model name is correct
   - Check if your account has access to the model
   - Try a different model

4. **Network Issues**
   ```
   Error: Connection timeout
   ```
   - Check your internet connection
   - Increase `TIMEOUT` value
   - Try again later

### Debug Mode

Enable debug logging to see detailed API interactions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### API Limits

Be aware of your account's limits:
- **Requests per minute**: Varies by plan
- **Tokens per request**: Usually 2000-4000
- **Monthly usage**: Check your dashboard

## Alternative APIs

If you need to use a different API provider, you can modify the `ResumeProcessor` class:

### OpenAI GPT
```python
from openai import OpenAI

class ResumeProcessor:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4"
```

### Azure OpenAI
```python
from openai import AzureOpenAI

class ResumeProcessor:
    def __init__(self, api_key: str, endpoint: str):
        self.client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version="2024-02-01"
        )
```

## Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Rotate API keys** regularly
4. **Monitor usage** to detect unauthorized access
5. **Set up billing alerts** to avoid unexpected charges

## Cost Optimization

1. **Adjust token limits** based on your needs
2. **Use checkpoints** to avoid reprocessing data
3. **Filter input data** to process only necessary records
4. **Monitor usage** in your dashboard
5. **Consider batch processing** for large datasets

