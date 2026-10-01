from flask import Flask, jsonify, request
import os
import requests
import boto3
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# OpenRouter
API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Study material
STUDY_FOLDER = "study_material"
STUDY_FILE = os.path.join(STUDY_FOLDER, "uploaded_document.txt")

# AWS region
AWS_REGION = "eu-north-1"

# DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table("StudyAssistantHistory")

# S3
S3_BUCKET = "ai-study-assistant-zain-2026"

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION
)


@app.route("/")
def home():
    return jsonify({
        "message": "AI Study Assistant API is running!"
    })


@app.route("/history", methods=["GET"])
def get_history():
    try:
        response = table.scan()

        history = response.get("Items", [])

        # Newest questions first
        history.sort(
            key=lambda item: item.get("created_at", ""),
            reverse=True
        )

        return jsonify(history)

    except Exception as error:
        return jsonify({
            "error": "Could not get history.",
            "details": str(error)
        }), 500


@app.route("/documents", methods=["POST"])
def upload_document():

    if "file" not in request.files:
        return jsonify({
            "error": "Please upload a file."
        }), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400

    os.makedirs(STUDY_FOLDER, exist_ok=True)

    # Save document locally
    file.save(STUDY_FILE)

    # Upload document to S3
    try:
        s3.upload_file(
            STUDY_FILE,
            S3_BUCKET,
            file.filename
        )

    except Exception as error:
        return jsonify({
            "error": "Document was saved locally but S3 upload failed.",
            "details": str(error)
        }), 500

    return jsonify({
        "message": "Document uploaded successfully!",
        "filename": file.filename,
        "s3_bucket": S3_BUCKET
    })


@app.route("/ask", methods=["POST"])
def ask_question():

    if not API_KEY:
        return jsonify({
            "error": "OPENROUTER_API_KEY was not found."
        }), 500

    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({
            "error": "Please provide a question."
        }), 400

    question = data["question"]

    if not os.path.exists(STUDY_FILE):
        return jsonify({
            "error": "Study material not found. Please upload a document first."
        }), 404

    with open(STUDY_FILE, "r", encoding="utf-8") as file:
        study_material = file.read()

    prompt = f"""
You are a study assistant.

Answer the user's question using the study material below.

If the answer is not found in the study material, say:
"That information is not available in the study material."

Study Material:
{study_material}

Question:
{question}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        result = response.json()

        if response.status_code != 200 or "choices" not in result:
            return jsonify({
                "error": "AI request failed.",
                "details": result
            }), 500

        answer = result["choices"][0]["message"]["content"]

        # Save Q&A to DynamoDB
        item = {
            "id": str(uuid.uuid4()),
            "question": question,
            "answer": answer,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item=item)

        return jsonify({
            "question": question,
            "answer": answer
        })

    except requests.exceptions.RequestException as error:
        return jsonify({
            "error": "Connection error.",
            "details": str(error)
        }), 500

    except Exception as error:
        return jsonify({
            "error": "Could not save history.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)