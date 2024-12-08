# Document Assistant

The **Document Assistant** is an innovative application designed to streamline document management and processing. By integrating a user-friendly interface, efficient data storage, and advanced text processing capabilities, this application enables users to effortlessly handle PDF and DOCX files for various tasks, including classification, summarization, translation, and OCR enhancement.

## Features

- **Document Upload:** Easily upload PDF and DOCX files through a user-friendly Streamlit interface.
- **Text Extraction:** Extract text from uploaded documents using libraries like `pdfplumber` and `python-docx`.
- **Document Classification:** Automatically classify documents into predefined categories using the Groq API.
- **Summarization:** Generate concise summaries of document content to quickly retrieve key information.
- **Translation:** Translate document summaries or extracted details into multiple languages.
- **OCR Enhancement:** Improve readability and accuracy of text extracted via OCR.
- **Cache Results:** Store processed data in SQLite for quick retrieval and reduced redundant processing.
- **Error Handling:** Robust mechanisms to ensure smooth operation and user-friendly error messages.

## Technologies Used

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** SQLite
- **Text Processing:** Groq API
- **File Handling:** pdfplumber, python-docx

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/smart-document-scan-assistant.git
   cd smart-document-scan-assistant
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables for the Groq API key.

5. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Usage

1. Navigate to the application in your web browser (default is `http://localhost:8501`).
2. Upload a PDF or DOCX document.
3. The application will automatically extract the text, classify the document, and provide options for summarization, translation, and OCR enhancement.
4. View the results directly in the interface and download processed documents as needed.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##Contributors

-Tanisha Samant -Rithika Malve

