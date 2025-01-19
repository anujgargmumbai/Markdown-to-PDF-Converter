# Markdown to PDF Converter

This project is a web application built with **Streamlit** that allows users to convert Markdown text into professionally formatted PDF documents. It supports Unicode fonts, checkboxes, and other Markdown features.

## Features

- Convert Markdown to PDF.
- Supports custom page sizes (Letter, A4).
- Interactive checkbox rendering.
- Upload Markdown files for conversion.
- Live preview of Markdown text.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.8 or later
- Pip package manager

## Installation

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
- **Windows**:
  ```bash
  .\venv\Scripts\activate
  ```
- **Mac/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Install Additional Fonts
Download and install the DejaVuSans font from [DejaVu Fonts](https://dejavu-fonts.github.io/), then place the `DejaVuSans.ttf` file in the project directory.

## Running the Application

### Start the Streamlit Server
```bash
streamlit run app.py
```

### Access the Application
Once the server is running, open your browser and navigate to:
```
http://localhost:8501
```

## Usage

1. Open the application in your browser.
2. Enter Markdown text in the "Enter Text" tab or upload a Markdown file in the "Upload File" tab.
3. Select your desired page size (Letter or A4).
4. Click the "Convert to PDF" button to generate the PDF.
5. Download the generated PDF using the download button.

## File Structure

```
project-folder/
├── app.py                 # Main Streamlit application file
├── requirements.txt       # Python dependencies
├── DejaVuSans.ttf         # Font file for Unicode support
├── README.md              # Project documentation
```

## Requirements File
Ensure the following dependencies are listed in your `requirements.txt` file:

```
streamlit
markdown
reportlab
beautifulsoup4
```

## Customization

- **Adding New Fonts:**
  - Place the new font file in the project directory.
  - Register the font in the `app.py` file using `pdfmetrics.registerFont`.

- **Styling Markdown Elements:**
  - Modify the styles in the `MarkdownToPDFConverter` class in `app.py`.

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add a new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy converting your Markdown to PDF effortlessly!

