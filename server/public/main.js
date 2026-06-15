const prompt = document.getElementById("prompt");

const promptInput = document.getElementById("prompt-input");
function autoResize() {
    prompt.style.height = "auto";

    const maxHeight = 150;
    const height = Math.min(prompt.scrollHeight, maxHeight);

    prompt.style.height = height + "px";

    promptInput.style.minHeight =
        (height + 30) + "px";

    prompt.style.overflowY =
        prompt.scrollHeight > maxHeight
            ? "auto"
            : "hidden";
}

prompt.addEventListener("input", autoResize);
