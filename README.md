# PDF Cover Page Generator

A professional web-based application for generating customizable A4 PDF cover pages. Built with Flask and ReportLab, this tool provides an intuitive interface for creating branded document covers with advanced customization options.

## Features

### Core Functionality
- **Web-based Interface**: Single-page application with responsive design
- **Real-time PDF Generation**: Server-side processing with instant download capability
- **Template System**: Pre-configured sample templates for quick start

### Customization Options
- **Header Section**: Company branding with logo upload and custom text
- **Content Area**: Primary title and multi-line subtitle configuration  
- **Footer Section**: Company and partner information with logo support
- **Visual Design**: Color picker integration for text, backgrounds, and decorative elements
- **Background Options**: Solid colors or linear gradient backgrounds
- **Image Support**: PNG, JPG, and GIF logo uploads with automatic processing

## Technology Stack

- **Backend**: Python 3.7+, Flask web framework
- **PDF Processing**: ReportLab library for document generation
- **Image Processing**: Pillow (PIL) for image manipulation
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript
- **File Handling**: Multipart upload support with validation

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SakibAhmedShuva/PDF-Cover-Generator-with-Python.git
   cd PDF-Cover-Generator-with-Python
   ```

2. **Create Virtual Environment**
   
   **Windows:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start Application**
   ```bash
   python app.py
   ```

5. **Access Interface**
   Navigate to `http://127.0.0.1:5000` in your web browser

## Usage Guide

### Basic Workflow
1. Access the web interface at the local server address
2. Complete the form fields for header, content, and footer sections
3. Upload logo files using the file selection buttons
4. Configure colors using the integrated color picker tools  
5. Select background style (gradient or solid color)
6. Generate PDF using the main action button
7. Download the generated file via the provided link

### Sample Configuration
Use the "Load Sample Config" feature to populate the form with example data and explore the application's capabilities.

## Project Structure

```
pdf-cover-generator/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Frontend interface
├── uploads/                 # User-uploaded images (auto-created)
├── output/                  # Generated PDF files (auto-created)
├── static/                  # Static assets (if applicable)
├── LICENSE                  # License file
└── README.md               # Documentation
```

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main application interface |
| `GET` | `/api/sample-config` | Sample configuration data |
| `POST` | `/api/upload` | File upload handler |
| `POST` | `/api/generate` | PDF generation endpoint |
| `GET` | `/api/download/<filename>` | File download service |

## Configuration

### Supported File Types
- **Images**: PNG, JPG, JPEG, GIF
- **Output**: PDF (A4 format)

### System Requirements
- **Memory**: Minimum 512MB RAM
- **Storage**: 100MB free space for temporary files
- **Network**: Local development server capability

## Development

### Contributing Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement-name`)
3. Implement changes with appropriate documentation
4. Commit changes (`git commit -m 'Add enhancement description'`)
5. Push to branch (`git push origin feature/enhancement-name`)
6. Submit a pull request

### Code Standards
- Follow PEP 8 Python style guidelines
- Include docstrings for all functions and classes
- Maintain backward compatibility when possible
- Add unit tests for new functionality

## License

This project is distributed under the MIT License. See `LICENSE` file for complete terms and conditions.

## Support

For issues, feature requests, or questions:
- Create an issue in the GitHub repository
- Review existing documentation and FAQ
- Check the project wiki for additional resources

## Acknowledgments

Built using open-source technologies including Flask web framework and ReportLab PDF toolkit. Special thanks to the Python community for continuous library development and support.
