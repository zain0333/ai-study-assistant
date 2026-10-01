\# AI Study Assistant



AI Study Assistant is a small AI-powered study application built with Python, AWS, and OpenRouter.



\## Project Objective



The project helps students ask questions about their study material and receive AI-generated answers.



\## Technologies Used



\* Python

\* OpenRouter API

\* AWS Lambda

\* Amazon S3

\* Amazon DynamoDB

\* Amazon API Gateway

\* Amazon CloudWatch

\* HTML, CSS, JavaScript

\* Git and GitHub



\## Architecture



User / Web UI

↓

API Gateway

↓

AWS Lambda

↓

OpenRouter AI



AWS Lambda also connects to:



\* Amazon S3 — stores study documents

\* Amazon DynamoDB — stores question and answer history

\* Amazon CloudWatch — logs and monitoring



\## Main Features



\* Ask study questions

\* Generate AI answers using OpenRouter

\* Read study material from Amazon S3

\* Upload study documents

\* Store question and answer history in DynamoDB

\* View request logs in CloudWatch

\* Simple web frontend



\## API Endpoints



\### GET /



Checks whether the API is running.



\### POST /ask



Asks a question and returns an AI-generated answer.



Example:



```json

{

&#x20; "question": "What is global warming?"

}

```



\### POST /documents



Uploads a study document to Amazon S3.



\### GET /history



Returns previous study questions and answers stored in DynamoDB.



\## Local Setup



Create and activate a Python virtual environment:



```powershell

python -m venv .venv

.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



Copy `.env.example` to `.env` and add the required configuration.



Never upload the real `.env` file to GitHub.



\## Security



\* API keys must never be written directly in source code.

\* AWS credentials must never be committed to GitHub.

\* The real `.env` file is ignored by Git.

\* `.env.example` contains only example configuration.

\* Local test and deployment files are ignored by Git.



\## AWS Region



The project is currently deployed in:



`eu-north-1` (Europe/Stockholm)



\## Project Status



The project is deployed using:



\* API Gateway

\* AWS Lambda

\* OpenRouter

\* Amazon S3

\* Amazon DynamoDB

\* Amazon CloudWatch



The project is also maintained in GitHub.



\## License



This project is for educational purposes.



