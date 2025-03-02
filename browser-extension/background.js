console.log("Background script loaded successfully.");

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "checkPhishing") {
        console.log("Received URL for checking:", request.url);

        fetch("http://127.0.0.1:5000/check_url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: request.url })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Phishing Check Result:", data);
            sendResponse({ result: data.phishing ? "⚠️ Phishing detected!" : "✅ Safe website" });
        })
        .catch(error => {
            console.error("Error checking URL:", error);
            sendResponse({ result: "❌ Error checking website" });
        });

        return true; // Keeps the message channel open for async response
    }
});