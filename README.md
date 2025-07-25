PDF Cover Page Generator 🎨
A web-based application built with Flask and ReportLab to dynamically generate professional A4 PDF cover pages. Customize everything from text and logos to backgrounds and colors through an intuitive user interface.

✨ Features
Intuitive Web UI: Easy-to-use single-page interface for creating cover pages.

Deep Customization:

Header: Set exclusive text, company name, and upload a logo.

Main Content: Define a main title and a multi-line subtitle.

Footer: Include company and partner information with logos and taglines.

Colors: Use color pickers to customize text, decorative elements, and backgrounds.

Dynamic Backgrounds: Choose between a solid color or a two-color linear gradient background.

Image Uploads: Easily upload and embed PNG, JPG, or GIF logos.

Instant Generation: Generate the PDF on the server and receive a direct download link.

Sample Configuration: Load a pre-defined sample configuration with a single click to see the generator in action.

🛠️ Technology Stack
Backend: Python, Flask

PDF Generation: ReportLab

Image Processing: Pillow

Frontend: HTML, CSS, Vanilla JavaScript

🚀 Getting Started
Follow these instructions to get a copy of the project up and running on your local machine.

Prerequisites
Python 3.7+

pip package manager

Installation
Clone the repository:

Bash

git clone https://github.com/SakibAhmedShuva/PDF-Cover-Generator-with-Python.git
cd PDF-Cover-Generator-with-Python
Create and activate a virtual environment (recommended):

On Windows:

Bash

python -m venv venv
.\venv\Scripts\activate
On macOS/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
Install the required dependencies:

Bash

pip install -r requirements.txt
Run the Flask application:

Bash

python app.py
Access the application:
Open your web browser and navigate to http://127.0.0.1:5000.

📝 How to Use
Open the Web Interface: Navigate to http://127.0.0.1:5000 in your browser.

Fill the Form: Input your desired text into the fields for the header, main content, and footer sections.

Upload Logos: Click the "Choose File" buttons to upload logos for the header, company info, and partner sections.

Select Colors: Use the color pickers to customize the colors for various elements.

Choose Background: Select either a "Gradient" or "Solid Color" background and configure it.

Generate: Click the 🚀 Generate Cover Page button. The application will process your inputs, generate the PDF, and provide a download link.

(Optional) Load a Sample: Click the 📋 Load Sample Config button to auto-fill the form with default data and see how it works.

📁 Project Structure
.
├── app.py                  # Main Flask application logic
├── requirements.txt        # Python package dependencies
├── templates/
│   └── index.html          # Frontend HTML, CSS, and JS
├── uploads/                # Directory for user-uploaded images (created automatically)
├── output/                 # Directory for generated PDFs (created automatically)
└── README.md               # This file
📄 API Endpoints
The application exposes a few simple API endpoints to handle frontend requests.

Method	Endpoint	Description
GET	/	Serves the main index.html page.
GET	/api/sample-config	Returns a sample JSON configuration object.
POST	/api/upload	Handles multipart file uploads for logos.
POST	/api/generate	Receives a JSON config and generates the PDF.
GET	/api/download/<filename>	Serves a generated PDF file for download.

Export to Sheets
📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

🤝 Contributing
Contributions are welcome! If you have suggestions for improvements or want to fix a bug, please feel free to:

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request
