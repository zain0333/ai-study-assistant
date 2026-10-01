import json
import os
import uuid
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

import boto3


# =========================
# AWS SETTINGS
# =========================

AWS_REGION = "eu-north-1"

S3_BUCKET = "ai-study-assistant-zain-2026"
DYNAMODB_TABLE = "StudyAssistantHistory"

s3 = boto3.client("s3", region_name=AWS_REGION)
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

table = dynamodb.Table(DYNAMODB_TABLE)


# =========================
# OPENROUTER SETTINGS
# =========================

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

OPENROUTER_MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"


# =========================
# RESPONSE HELPER
# =========================

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }


# =========================
# GET STUDY MATERIAL
# =========================

def get_study_material():

    result = s3.get_object(
        Bucket=S3_BUCKET,
        Key="global_warming.txt"
    )

    content = result["Body"].read().decode("utf-8")

    return content


# =========================
# ASK AI
# =========================

def ask_ai(question, study_material):

    if not OPENROUTER_API_KEY:
        raise Exception("OPENROUTER_API_KEY is not configured.")


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


    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }


    request = Request(
        OPENROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )


    try:

        with urlopen(request, timeout=60) as result:

            data = json.loads(
                result.read().decode("utf-8")
            )

    except HTTPError as error:

        error_body = error.read().decode("utf-8")

        raise Exception(
            f"OpenRouter error: {error_body}"
        )

    except URLError as error:

        raise Exception(
            f"Connection error: {error}"
        )


    if "choices" not in data:

        raise Exception(
            f"AI response did not contain choices: {data}"
        )


    return data["choices"][0]["message"]["content"]


# =========================
# SAVE HISTORY
# =========================

def save_history(question, answer):

    item = {
        "id": str(uuid.uuid4()),
        "question": question,
        "answer": answer,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat()
    }

    table.put_item(Item=item)


# =========================
# GET HISTORY
# =========================

def get_history():

    result = table.scan()

    history = result.get("Items", [])

    history.sort(
        key=lambda item: item.get(
            "created_at",
            ""
        ),
        reverse=True
    )

    return history


# =========================
# LAMBDA HANDLER
# =========================

def lambda_handler(event, context):

    try:

        method = event.get(
            "requestContext",
            {}
        ).get(
            "http",
            {}
        ).get(
            "method"
        )

        path = event.get(
            "rawPath",
            "/"
        )


        # -------------------------
        # HOME
        # -------------------------

        if method == "GET" and path == "/":

            return response(
                200,
                {
                    "message":
                    "AI Study Assistant Lambda is running!"
                }
            )


        # -------------------------
        # HISTORY
        # -------------------------

        if method == "GET" and path == "/history":

            history = get_history()

            return response(
                200,
                history
            )


        # -------------------------
        # ASK QUESTION
        # -------------------------

        if method == "POST" and path == "/ask":

            body = event.get("body", "{}")

            if event.get("isBase64Encoded"):

                import base64

                body = base64.b64decode(
                    body
                ).decode("utf-8")


            data = json.loads(body)

            question = data.get("question")


            if not question:

                return response(
                    400,
                    {
                        "error":
                        "Please provide a question."
                    }
                )


            study_material = get_study_material()

            answer = ask_ai(
                question,
                study_material
            )

            save_history(
                question,
                answer
            )


            return response(
                200,
                {
                    "question": question,
                    "answer": answer
                }
            )


        # -------------------------
        # DOCUMENT UPLOAD
        # -------------------------

        if method == "POST" and path == "/documents":

            body = event.get("body", "{}")

            if event.get("isBase64Encoded"):

                import base64

                body = base64.b64decode(
                    body
                ).decode("utf-8")


            data = json.loads(body)

            filename = data.get("filename")
            content = data.get("content")


            if not filename or content is None:

                return response(
                    400,
                    {
                        "error":
                        "Please provide filename and content."
                    }
                )


            s3.put_object(
                Bucket=S3_BUCKET,
                Key=filename,
                Body=content.encode("utf-8")
            )


            return response(
                200,
                {
                    "message":
                    "Document uploaded successfully!",
                    "filename":
                    filename,
                    "s3_bucket":
                    S3_BUCKET
                }
            )


        # -------------------------
        # ROUTE NOT FOUND
        # -------------------------

        return response(
            404,
            {
                "error":
                "Route not found."
            }
        )


    except Exception as error:

        return response(
            500,
            {
                "error":
                "Internal server error.",
                "details":
                str(error)
            }
        )