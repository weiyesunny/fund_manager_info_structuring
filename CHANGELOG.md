# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-06-21

### Added
- Initial release of Fund Manager Resume Processor
- AI-powered resume information extraction using Cerebras Cloud API
- Support for Chinese fund manager resume processing
- Structured data extraction for:
  - Basic information (gender, education, graduate school)
  - Education history (bachelor, master, doctoral degrees)
  - Work experience (up to 5 positions)
  - Professional features (certifications, awards, expertise, etc.)
- Progress tracking with ETA estimates
- Checkpoint system for data recovery
- Comprehensive error handling and logging
- Excel file input/output support
- Rate limiting for API compliance
- Batch processing capabilities

### Documentation
- Comprehensive README with setup and usage instructions
- API setup guide with troubleshooting
- Data format documentation
- Example data files
- Test suite for API validation

### Configuration
- Environment variable support for API keys
- Configurable processing parameters
- Example configuration files
- Support for different AI models

### Features
- Automatic backup and checkpoint creation
- Progress visualization with emoji indicators
- Flexible row range processing
- Detailed processing summaries
- Support for missing data handling

## [Unreleased]

### Planned
- Support for additional AI providers (OpenAI, Azure)
- Enhanced error recovery mechanisms
- Batch size optimization
- Performance monitoring and metrics
- Web interface for easier usage
- Docker containerization
- Automated testing pipeline

