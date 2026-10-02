# AI Study Assistant

AI Study Assistant is a small AI-powered study application built with Python, AWS, and OpenRouter.

## Project Objective

The project helps students ask questions about their study material and receive AI-generated answers.

## Technologies Used

- Python
- OpenRouter API
- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- Amazon API Gateway
- Amazon CloudWatch
- HTML
- CSS
- JavaScript
- Git
- GitHub

## Architecture

```text
User / Web UI
      ↓
API Gateway
      ↓
AWS Lambda
      ↓
OpenRouter AI
```

AWS Lambda also connects to:

- **Amazon S3** — stores study documents
- **Amazon DynamoDB** — stores question and answer history
- **Amazon CloudWatch** — provides logs and monitoring

## Main Features

- Ask study questions
- Generate AI answers using OpenRouter
- Read study material from Amazon S3
- Upload `.txt` study documents
- Store question and answer history in DynamoDB
- View Lambda request logs in CloudWatch
- Simple web frontend
- API-based architecture

## API Endpoints

### GET `/`

Checks whether the API is running.

### POST `/ask`

Asks a question and returns an AI-generated answer.

Example request:

```json
{
  "question": "What is global warming?"
}
```

### POST `/documents`

Uploads a `.txt` study document to Amazon S3.

### GET `/history`

Returns previous study questions and answers stored in DynamoDB.

## Local Setup

Create a Python virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your required configuration.

**Never upload the real `.env` file to GitHub.**

## Running the Frontend Locally

From the project folder, run:

```powershell
python -m http.server 8000 --directory frontend
```

Then open:

```text
http://localhost:8000
```

## Security

- API keys must never be written directly in source code.
- AWS credentials must never be committed to GitHub.
- The real `.env` file is ignored by Git.
- `.env.example` contains only example configuration.
- Local test and deployment files are ignored by Git.

## AWS Region

The project is currently deployed in:

```text
eu-north-1 (Europe/Stockholm)
```

## Project Status

The project is deployed using:

- API Gateway
- AWS Lambda
- OpenRouter
- Amazon S3
- Amazon DynamoDB
- Amazon CloudWatch

The project is also maintained in GitHub.

## License

This project is for educational purposes.
