# Fund Manager Resume Processor

An AI-powered tool for extracting and structuring information from fund manager resumes in Excel format using the Cerebras Cloud API.

## Overview

This project automates the process of extracting structured information from Chinese fund manager resumes stored in Excel files. It uses AI to parse resume text and organize the data into standardized formats for education history, work experience, and other professional features.

## Features

- **AI-Powered Extraction**: Uses Cerebras Cloud API for intelligent text processing
- **Structured Output**: Organizes resume data into standardized categories
- **Progress Tracking**: Real-time processing status with ETA estimates
- **Checkpoint System**: Automatic saving to prevent data loss
- **Error Handling**: Robust error management for API failures
- **Batch Processing**: Handles large Excel files efficiently

## Data Structure

The tool processes resumes and extracts:

### Basic Information
- Gender (性别)
- Education level (学历) - highest degree
- Graduate school (毕业院校) - from highest degree

### Education History (教育经历)
- Bachelor's degree information
- Master's degree information
- Doctoral degree information
- Other educational qualifications

Format: `University|Major|Degree|Start_Date|End_Date`

### Work Experience (工作经历)
- Up to 5 work positions
- Company name, position, start/end dates

Format: `Company|Position|Start_Date|End_Date`

### Other Features (其他特征)
- **Certification**: Professional certificates and qualifications
- **Charity**: Charitable activities participation
- **Prize**: Awards and recognitions
- **Hobby**: Personal interests
- **Expert-in**: Areas of expertise and specialization
- **Writings**: Publications, articles, books
- **Part-time-job**: Other company positions and organization roles
- **Social-activities**: Social and community activities

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/fund-manager-resume-processor.git
cd fund-manager-resume-processor
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Cerebras API key:
- Sign up for a Cerebras Cloud account
- Get your API key
- Update the `api_key` variable in the main script

## Usage

### Basic Usage

1. Prepare your Excel file with the required columns (see `example_data/` for format)
2. Update the file paths in `resume_processor.py`:
   ```python
   input_file = "path/to/your/input.xlsx"
   output_file = "path/to/your/output.xlsx"
   ```
3. Run the processor:
   ```bash
   python resume_processor.py
   ```

### Advanced Usage

Process specific row ranges:
```python
processor = ResumeProcessor(api_key)
processed_df = processor.process_dataframe(df, start_idx=0, end_idx=100)
```

Adjust checkpoint frequency:
```python
processed_df = processor.process_dataframe(df, checkpoint_interval=50)
```

## Input Format

Your Excel file should contain these columns:
- `user_id`: Unique identifier
- `user_name`: Person's name
- `gender`: Gender (optional, will be extracted if missing)
- `education`: Education level (optional, will be extracted if missing)
- `graduate_school`: Graduate school (optional, will be extracted if missing)
- `resume_minfo`: Main resume information
- `resume_pinfo`: Additional resume information

See `example_data/manager_cv.xlsx` for a sample format.

## Output Format

The processed Excel file will include all original columns plus:
- Structured education history (教育1, 教育2, 教育3)
- Structured work history (工作1-工作5)
- Extracted features (certification, charity, prize, etc.)
- `CD_change`: Flag indicating if basic info was updated
- `OTHER`: Additional resume information not categorized elsewhere

## Configuration

### API Settings
- **Model**: `llama-4-scout-17b-16e-instruct` (configurable)
- **Max Tokens**: 2000
- **Temperature**: 0.1 (for consistent outputs)
- **Rate Limiting**: 0.3 seconds between requests

### Processing Settings
- **Checkpoint Interval**: Save progress every 50 records (configurable)
- **Batch Size**: Processes entire dataset (configurable ranges available)

## Performance

- **Processing Speed**: ~0.3 seconds per record (API dependent)
- **Memory Usage**: Optimized for large Excel files
- **Error Recovery**: Automatic retry mechanism for failed API calls

## Error Handling

The tool handles various error scenarios:
- Missing or invalid resume data
- API rate limiting and failures
- Malformed JSON responses
- File I/O errors

Failed records are logged and skipped, allowing processing to continue.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions or support, please:
1. Check the documentation in `docs/`
2. Review example usage in `example_data/`
3. Open an issue on GitHub

## Changelog

### v1.0.0 (2024-06-21)
- Initial release
- Basic resume processing functionality
- Cerebras API integration
- Checkpoint system implementation

## Acknowledgments

- Cerebras Cloud for AI processing capabilities
- Contributors and testers who helped improve the tool

## Disclaimer

This tool is designed for processing Chinese fund manager resumes. Results may vary depending on resume format and content quality. Always review processed data for accuracy.

