
# Signature, Stamp, and Meterai Analysis

This project provides an API to analyze documents for signatures, company stamps, and duty stamps (meterai) using the Gemini model.

## Project Structure
```plaintext
project/
├── images
├── __init__.py
├── main.py
├── api.py
├── config.py
├── utils.py
├── pdf_processor.py
└── .env
```

## Setup and Installation

Follow these steps to set up the project:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-repo/signature-stamp-analysis.git
    ```

2. **Navigate to the project directory**:
    ```sh
    cd signature-stamp-analysis
    ```

3. **Create a virtual environment and activate it**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Create a `.env` file with your project credentials**:
    ```plaintext
    PROJECT_ID=your-project-id
    CREDENTIALS_FILE_PATH=/path/to/your/credentials.json
    GEMINI_MODEL=name-of-gemini-model
    ```

## Running the Application

To start the FastAPI application, run:

```sh
uvicorn main:app --host 0.0.0.0 --port 2224
```

The application will be available at [http://34.101.213.23:2224](http://34.101.213.23:2224)

The API documentation will be available at [http://34.101.213.23:2224/docs](http://34.101.213.23:2224/docs)

## API Endpoints

### Analyze Document

- **Endpoint**: `POST /analyze`
- **Description**: Analyze a document for signatures, stamps, and duty stamps (meterai).
- **Parameters**:
  - `file`: Upload a document file (PDF, PNG, JPEG)
  - `url`: Provide a URL to the document file

**Example usage with URL**:

```python
import requests

url = 'http://34.101.213.23:2224/analyze'
file_url = 'https://example.com/yourfile.pdf'

data = {
    'url': file_url
}

response = requests.post(url, data=data)

print(response.status_code)
print(response.json())
```

**Example usage with FILE_PATH**:

```python
import requests

url = 'http://34.101.213.23:2224/analyze'
file_path = 'path/to/yourfile.pdf'

files = {'file': open(file_path, 'rb')}

response = requests.post(url, files=files)  

print(response.status_code)
print(response.json())
```

## Environment Variables

The project uses a `.env` file to manage environment variables. Ensure you have the following variables set:

- `PROJECT_ID`: Your Google Cloud project ID
- `CREDENTIALS_FILE_PATH`: Path to your Google Cloud service account credentials file
- `GEMINI_MODEL`: Model Name for Gemini API

## Directory Structure

Explanation of the project directory structure:

- `__init__.py`: Initializes the project module
- `main.py`: Defines the FastAPI app and includes routing
- `api.py`: Contains API endpoint definitions
- `config.py`: Handles project configuration and Vertex AI initialization
- `utils.py`: Utility functions for content analysis and PDF processing
- `pdf_processor.py`: Handles PDF processing and conversion to images
- `.env`: Environment variables file

## Notes

*Ensure that the images for sample duty stamp and company stamp are located in the `images` directory.*
```

Markdown ini akan memberikan format yang bersih dan mudah dibaca untuk README proyek Anda. Anda bisa menambahkan file ini sebagai `README.md` di root direktori proyek Anda sehingga akan tampil otomatis di halaman utama repository GitHub Anda.
