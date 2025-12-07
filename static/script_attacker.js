const API_BASE = "http://127.0.0.1:5000";

async function postJSON(path, body) {
    const res = await fetch(API_BASE + path, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    });
    return res.json();
}

function show(msg) {
    const el = document.getElementById("result");
    el.textContent = new Date().toLocaleTimeString() + " - " + msg + "\n" + el.textContent;
}

document.getElementById("btn-send").addEventListener("click", async () => {
    const idx = parseInt(document.getElementById("sample-idx").value) || 0;
    show("Sending sample " + idx + " to victim...");
    const res = await postJSON("/send-sample", { idx });
    show("Packet sent: " + JSON.stringify(res.packet));
});