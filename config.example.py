# Configuration Example
# Copy this file to config.py and update with your settings

# Cerebras API Configuration
CEREBRAS_API_KEY = "your_api_key_here"  # Get from https://cloud.cerebras.ai
MODEL_NAME = "llama-4-scout-17b-16e-instruct"

# File Paths
INPUT_FILE = "example_data/manager_cv.xlsx"
OUTPUT_FILE = "output/processed_manager_cv.xlsx"

# Processing Settings
CHECKPOINT_INTERVAL = 50  # Save checkpoint every N records
RATE_LIMIT_DELAY = 0.3    # Seconds between API calls
MAX_TOKENS = 2000         # Maximum tokens for API response
TEMPERATURE = 0.1         # Lower = more consistent, higher = more creative

# API Settings
MAX_RETRIES = 3
TIMEOUT = 30  # seconds

