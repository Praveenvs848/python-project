

# PDF Query AI Assistant

This project is a FastAPI-based web application that allows users to upload PDF files, extract their text, and query the extracted content using an AI model. The AI responds to user queries in Markdown format, providing well-structured answers.

## Features

- **PDF Upload and Text Extraction**: Upload PDF files, and the application extracts text using `pdfplumber`.
- **AI Query Response**: Query the extracted text using an AI model powered by OpenAI's GPT-3.5.
- **Streaming Responses**: Get real-time streaming responses from the AI.
- **Markdown Support**: The AI responds with answers in Markdown format, including headings, lists, and other elements for better readability.

## Requirements

- Python 3.9 or higher
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Add `.env` File for API Keys

1. Create a file named `.env` in the root directory of the project.
2. Add the required API key (e.g., OpenAI API key) to the `.env` file in the following format:
   ```
   OPENAI_API_KEY=sk-your-openai-api-key
   ```

3. Update the code to load the API key using `python-dotenv`. For example:
   ```python
   from dotenv import load_dotenv
   import os

   # Load environment variables from .env file
   load_dotenv()

   # Access the API key
   openai_api_key = os.getenv("OPENAI_API_KEY")
   ```

4. Ensure the `.env` file is included in `.gitignore` to prevent accidental exposure of sensitive information:
   ```
   .env
   ```

## Usage

1. Run the FastAPI application:
   ```bash
   uvicorn app:app --reload
   ```

2. Access the application at:
   ```
   http://127.0.0.1:8000
   ```

3. Use the following endpoints:

   - **Upload PDF**:
     ```
     POST /upload
     ```
     Upload a PDF file and extract its text.

   - **Stream Query**:
     ```
     POST /stream
     ```
     Send a query to the AI assistant and receive a streaming response.

## API Endpoints

### Upload PDF
- **URL**: `/upload`
- **Method**: `POST`
- **Request**: Upload a file using a form.
- **Response**:
  ```json
  {
    "message": "File uploaded successfully!",
    "text": "Extracted text from the PDF."
  }
  ```

### Stream Query
- **URL**: `/stream`
- **Method**: `POST`
- **Request**:
  ```json
  {
    "query": "What is the summary of the document?"
  }
  ```
- **Response**: Streaming AI responses with two agents:
  - `answer_agent`: Provides detailed answers.
  - `usermessage_agent`: Provides user-friendly summaries.

## Technologies Used

- **FastAPI**: For building the web application.
- **pdfplumber**: For extracting text from PDF files.
- **LangChain**: For building and managing the AI workflow.
- **OpenAI GPT-3.5**: For AI-powered query responses.

## Example Workflow

1. **Upload a PDF**: Use the `/upload` endpoint to upload a PDF file.
2. **Ask a Question**: Use the `/stream` endpoint with your query.
3. **Receive a Response**: The AI streams back answers and user-friendly summaries.

## Project Structure

```
.
├── app.py                # Main FastAPI application
├── agent.py              # AI workflow and graph definitions
├── uploads/              # Directory for uploaded files
├── requirements.txt      # Project dependencies
├── .env                  # Environment variables (not included in version control)
└── README.md             # Project documentation
```

## Future Enhancements

- Add support for multiple file types (e.g., DOCX, TXT).
- Implement authentication and authorization for secure access.
- Optimize streaming response handling for larger documents.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the powerful web framework.
- [OpenAI](https://openai.com/) for the GPT model.
- [LangChain](https://langchain.com/) for the AI workflow integration.

---


```