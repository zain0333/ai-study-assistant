import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("ERROR: OPENROUTER_API_KEY was not found.")
    exit()

# Read study material
document_path = "study_material/global_warming.txt"

with open(document_path, "r", encoding="utf-8") as file:
    study_material = file.read()

print("Study material loaded successfully!")

# History file
history_file = "history.json"

if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as file:
        history = json.load(file)
else:
    history = []


# Function to show history
def show_history():
    if not history:
        print("\nNo Q&A history found.")
        return

    print("\n========== Q&A HISTORY ==========")

    for number, item in enumerate(history, start=1):
        print(f"\nQuestion {number}:")
        print(item["question"])

        print("\nAnswer:")
        print(item["answer"])

        print("---------------------------------")


# OpenRouter API
url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}


# Main program
while True:

    print("\n========== AI STUDY ASSISTANT ==========")
    print("1. Ask a question")
    print("2. View Q&A history")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    # Ask question
    if choice == "1":

        question = input("\nAsk a question about the study material: ")

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

        data = {
            "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        print("\nAsking AI...\n")

        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60
            )

            result = response.json()

            if response.status_code == 200 and "choices" in result:

                answer = result["choices"][0]["message"]["content"]

                print("AI Answer:")
                print(answer)

                # Save history
                history.append({
                    "question": question,
                    "answer": answer
                })

                with open(history_file, "w", encoding="utf-8") as file:
                    json.dump(history, file, indent=4)

                print("\nQ&A saved successfully!")

            else:
                print("\nAPI Error:")
                print("Status Code:", response.status_code)
                print(result)

        except requests.exceptions.RequestException as error:
            print("\nConnection Error:")
            print(error)

    # View history
    elif choice == "2":
        show_history()

    # Exit
    elif choice == "3":
        print("\nThank you for using AI Study Assistant!")
        break

    else:
        print("\nInvalid option. Please choose 1, 2, or 3.")