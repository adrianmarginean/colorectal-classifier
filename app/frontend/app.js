const form = document.getElementById("upload-form");
const resultDiv = document.getElementById("result");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    console.log("Form submitted");

    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
        resultDiv.textContent = "Please select an image file.";
        console.log("No file selected");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);
    console.log("File appended to formData");

    try {
        console.log("Sending POST request to /api/predict");
        const response = await fetch("http://127.0.0.1:8000/api/predict", {
            method: "POST",
            body: formData,
        });

        console.log("Response received");
        const data = await response.json();
        console.log("Response data:", data);

        if (data.error) {
            resultDiv.textContent = `Error: ${data.error}`;
            console.log("Error:", data.error);
        } else {
            resultDiv.textContent = `Predicted Class: ${data.class_index}, Confidence: ${data.confidence ? data.confidence.toFixed(2) : 'N/A'}`;
            console.log("Predicted Class:", data.class_index, "Confidence:", data.confidence);
        }
    } catch (err) {
        resultDiv.textContent = `Error: ${err.message}`;
        console.log("Fetch error:", err.message);
    }
});