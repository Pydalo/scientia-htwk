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

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let fullText = "";

        const div = document.createElement("div");
        div.classList.add("msg", "bot");
        chatContainer.appendChild(div);

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            fullText += chunk;

            const html = marked.parse(fullText);
            div.innerHTML = DOMPurify.sanitize(html);
        }

        history.push({ role: "assistant", content: fullText });

        chatContainer.scrollTop = chatContainer.scrollHeight;

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