const API_URL = "https://1tmaugenzc.execute-api.eu-north-1.amazonaws.com/prod";

const questionInput = document.getElementById("question");
const askButton = document.getElementById("askButton");
const answerDiv = document.getElementById("answer");
const loadingDiv = document.getElementById("loading");

const documentFile = document.getElementById("documentFile");
const uploadButton = document.getElementById("uploadButton");
const uploadMessage = document.getElementById("uploadMessage");

const historyButton = document.getElementById("historyButton");
const historyDiv = document.getElementById("history");

// Ask AI
askButton.addEventListener("click", async () => {
const question = questionInput.value.trim();

```
if (!question) {
    answerDiv.textContent = "Please enter a question.";
    return;
}

loadingDiv.classList.remove("hidden");
answerDiv.textContent = "";
askButton.disabled = true;

try {
    const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            question: question
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Request failed.");
    }

    answerDiv.textContent = data.answer || "No answer received.";

} catch (error) {
    answerDiv.textContent = `Error: ${error.message}`;
} finally {
    loadingDiv.classList.add("hidden");
    askButton.disabled = false;
}
```

});

// Upload document
uploadButton.addEventListener("click", async () => {
const file = documentFile.files[0];

```
if (!file) {
    uploadMessage.textContent = "Please select a .txt file.";
    return;
}

if (!file.name.toLowerCase().endsWith(".txt")) {
    uploadMessage.textContent = "Only .txt files are supported.";
    return;
}

uploadMessage.textContent = "Uploading...";
uploadButton.disabled = true;

try {
    const content = await file.text();

    const response = await fetch(`${API_URL}/documents`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            filename: file.name,
            content: content
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Upload failed.");
    }

    uploadMessage.textContent =
        data.message || "Document uploaded successfully.";

    documentFile.value = "";

} catch (error) {
    uploadMessage.textContent = `Error: ${error.message}`;
} finally {
    uploadButton.disabled = false;
}
```

});

// Load history
historyButton.addEventListener("click", async () => {
historyDiv.textContent = "Loading history...";
historyButton.disabled = true;

```
try {
    const response = await fetch(`${API_URL}/history`);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Could not load history.");
    }

    if (!data.history || data.history.length === 0) {
        historyDiv.textContent = "No study history found.";
        return;
    }

    historyDiv.innerHTML = "";

    data.history.forEach((item) => {
        const historyItem = document.createElement("div");
        historyItem.className = "history-item";

        const question = document.createElement("p");
        question.innerHTML = `<strong>Question:</strong> ${escapeHtml(
            item.question || ""
        )}`;

        const answer = document.createElement("p");
        answer.innerHTML = `<strong>Answer:</strong> ${escapeHtml(
            item.answer || ""
        )}`;

        historyItem.appendChild(question);
        historyItem.appendChild(answer);

        historyDiv.appendChild(historyItem);
    });

} catch (error) {
    historyDiv.textContent = `Error: ${error.message}`;
} finally {
    historyButton.disabled = false;
}
```

});

// Prevent HTML from being inserted into the page
function escapeHtml(text) {
const div = document.createElement("div");
div.textContent = text;
return div.innerHTML;
}
