document.addEventListener("DOMContentLoaded", function () {
    let checkButton = document.getElementById("check-url");

    if (!checkButton) {
        console.error("Button not found!");
        return;
    }

    checkButton.addEventListener("click", function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            let currentUrl = tabs[0].url;

            fetch("http://127.0.0.1:5000/check_url", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: currentUrl }),
            })
            .then(response => response.json())
            .then(data => {
                let resultText = data.phishing
                    ? "⚠️ Warning: This website may be a phishing site!"
                    : "✅ This website is safe!";
                document.getElementById("result").textContent = resultText;
            })
            .catch(error => {
                console.error("Error:", error);
                document.getElementById("result").textContent = "❌ Error checking URL.";
            });
        });
    });
});