const prompt = document.getElementById("prompt");
const promptInput = document.getElementById("prompt-input");
const chatContainer = document.getElementById("chat-container");

const history = [];

let isSending = false;

// ---------- Auto Resize ----------
function autoResize() {
    prompt.style.height = "auto";

    const maxHeight = 150;
    const height = Math.min(prompt.scrollHeight, maxHeight);

    prompt.style.height = height + "px";
    promptInput.style.minHeight = (height + 30) + "px";

    prompt.style.overflowY =
        prompt.scrollHeight > maxHeight ? "auto" : "hidden";
}

// ---------- Key Handling ----------
function onKey(e) {
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {
        e.preventDefault();
        send();
    }
}

// ---------- Message Rendering ----------
function renderMessage(role, text) {
    const div = document.createElement("div");

    div.classList.add("msg");
    div.classList.add(role === "user" ? "user" : "bot");

    if (role === "assistant") {
        const html = marked.parse(text);
        div.innerHTML = DOMPurify.sanitize(html);
    } else {
        div.textContent = text;
    }

    chatContainer.appendChild(div);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ---------- Send Message ----------
async function send() {
    if (isSending) return;

    const message = prompt.value.trim();
    if (!message) return;

    isSending = true;

    history.push({ role: "user", content: message });
    if (history.length > 30) history.shift();

    renderMessage("user", message);

    prompt.value = "";
    autoResize();

    try {
        petals.speed = 7;
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                messages: history
            })
        });

        if (!response.ok) {
            throw new Error(await response.text());
        }

        const data = await response.json();
        const answer = data?.answer;

        if (typeof answer !== "string") {
            throw new Error("Ungültige Antwort vom Backend.");
        }

        history.push({ role: "assistant", content: answer });
        if (history.length > 30) history.shift();

        renderMessage("assistant", answer);

    } catch (err) {
        console.error("Fehler:", err);
        renderMessage("assistant", "Fehler beim Senden.");
    } finally {
        petals.speed = 1;
        isSending = false;
    }
}

// ---------- Events ----------
prompt.addEventListener("input", autoResize);
prompt.addEventListener("keydown", onKey);